"""
Gestor de Cracking
Coordena execução de hashcat/john e distribuição de trabalho
"""

import os
import subprocess
import json
import time
import logging
from pathlib import Path
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed


class CrackingManager:
    """Gestor de operações de cracking"""
    
    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.cracking_config = config['experiment']['cracking']
    
    def run_cracking(self, hashes_file: Path, output_dir: Path) -> Dict:
        """Executar cracking de todos os hashes"""
        results = {
            'total_hashes': 0,
            'cracked': 0,
            'by_algorithm': {},
            'by_mode': {},
            'executions': []
        }
        
        # Carregar hashes
        with open(hashes_file, 'r') as f:
            all_hashes = json.load(f)
        
        results['total_hashes'] = len(all_hashes)
        
        # Agrupar por algoritmo
        by_algo = {}
        for h in all_hashes:
            algo = h['algorithm']
            if algo not in by_algo:
                by_algo[algo] = []
            by_algo[algo].append(h)
        
        # Processar cada algoritmo
        for algo, hashes in by_algo.items():
            self.logger.info(f"Processando {len(hashes)} hashes {algo}...")
            
            algo_results = self._crack_algorithm(
                algo, 
                hashes, 
                output_dir / algo
            )
            
            results['by_algorithm'][algo] = algo_results
            results['cracked'] += algo_results['cracked']
            results['executions'].extend(algo_results['executions'])
        
        # Salvar resultados
        results_file = output_dir / "cracking_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        return results
    
    def _crack_algorithm(self, algo: str, hashes: List[Dict], output_dir: Path) -> Dict:
        """Executar cracking para um algoritmo específico"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = {
            'algorithm': algo,
            'total': len(hashes),
            'cracked': 0,
            'executions': []
        }
        
        # Preparar ficheiro de hashes para hashcat
        hash_file = output_dir / "hashes.txt"
        self._prepare_hashcat_file(hashes, hash_file, algo)
        
        # Executar cada modo de cracking configurado
        for mode_config in self.cracking_config['modes']:
            mode_type = mode_config['type']
            
            self.logger.info(f"  Modo: {mode_type}")
            
            exec_result = self._execute_cracking_mode(
                algo,
                hash_file,
                mode_config,
                output_dir
            )
            
            results['executions'].append(exec_result)
            results['cracked'] = max(results['cracked'], exec_result.get('cracked', 0))
        
        return results
    
    def _prepare_hashcat_file(self, hashes: List[Dict], output_file: Path, algo: str):
        """Preparar ficheiro de hashes no formato hashcat"""
        with open(output_file, 'w') as f:
            for h in hashes:
                hash_val = h['hash']
                salt = h.get('salt', '')
                
                # Formato varia por algoritmo
                if algo in ['md5', 'sha1', 'sha256'] and salt:
                    f.write(f"{hash_val}:{salt}\n")
                else:
                    f.write(f"{hash_val}\n")
    
    def _execute_cracking_mode(self, algo: str, hash_file: Path, 
                                mode_config: Dict, output_dir: Path) -> Dict:
        """Executar um modo de cracking específico"""
        mode_type = mode_config['type']
        # Usar potfile único por algoritmo E modo
        potfile = output_dir / f"cracked_{algo}_{mode_type}.pot"
        
        start_time = time.time()
        
        result = {
            'mode': mode_type,
            'algorithm': algo,
            'start_time': start_time,
            'cracked': 0,
            'command': None
        }
        
        try:
            if mode_type == 'dictionary':
                result.update(self._run_dictionary_attack(
                    algo, hash_file, mode_config, potfile
                ))
            elif mode_type == 'brute-force':
                result.update(self._run_bruteforce_attack(
                    algo, hash_file, mode_config, potfile
                ))
            else:
                self.logger.warning(f"Modo não suportado: {mode_type}")
        
        except Exception as e:
            self.logger.error(f"Erro no cracking: {e}")
            result['error'] = str(e)
        
        result['duration'] = time.time() - start_time
        result['end_time'] = time.time()
        
        return result
    
    def _run_dictionary_attack(self, algo: str, hash_file: Path, 
                                config: Dict, potfile: Path) -> Dict:
        """Executar ataque de dicionário"""
        wordlist = Path(config['wordlist'])
        rules = config.get('rules')
        
        if not wordlist.exists():
            raise FileNotFoundError(f"Wordlist não encontrada: {wordlist}")
        
        # Determinar hash-type para hashcat
        hash_type = self._get_hashcat_type(algo)
        
        # Construir comando hashcat
        cmd = [
            'hashcat',
            '-m', str(hash_type),
            '-a', '0',  # Dictionary attack
            '--potfile-path', str(potfile),
            '--quiet',
            '--force',
            str(hash_file),
            str(wordlist)
        ]
        
        if rules:
            cmd.extend(['-r', str(rules)])
        
        # Executar
        self.logger.debug(f"Comando: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=config.get('max_time', 600)
            )
            
            # Contar crackeados
            cracked_count = self._count_cracked(potfile)
            
            return {
                'command': ' '.join(cmd),
                'cracked': cracked_count,
                'returncode': result.returncode,
                'stdout': result.stdout[:500],  # Limitar output
                'stderr': result.stderr[:500]
            }
        
        except subprocess.TimeoutExpired:
            self.logger.warning("Timeout atingido")
            return {
                'command': ' '.join(cmd),
                'cracked': self._count_cracked(potfile),
                'timeout': True
            }
    
    def _run_bruteforce_attack(self, algo: str, hash_file: Path,
                                config: Dict, potfile: Path) -> Dict:
        """Executar ataque brute-force"""
        mask = config.get('mask', '?l?l?l?l')
        max_time = config.get('max_time', 300)
        
        hash_type = self._get_hashcat_type(algo)
        
        cmd = [
            'hashcat',
            '-m', str(hash_type),
            '-a', '3',  # Brute-force
            '--potfile-path', str(potfile),
            '--quiet',
            '--force',
            str(hash_file),
            mask
        ]
        
        self.logger.debug(f"Comando: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=max_time
            )
            
            return {
                'command': ' '.join(cmd),
                'cracked': self._count_cracked(potfile),
                'returncode': result.returncode,
                'mask': mask
            }
        
        except subprocess.TimeoutExpired:
            return {
                'command': ' '.join(cmd),
                'cracked': self._count_cracked(potfile),
                'timeout': True,
                'mask': mask
            }
    
    def _get_hashcat_type(self, algo: str) -> int:
        """Mapear algoritmo para hash-type do hashcat"""
        mapping = {
            'md5': 0,
            'sha1': 100,
            'sha256': 1400,
            'bcrypt': 3200,
            'scrypt': 8900,
            'pbkdf2_sha256': 10900,
            'argon2': 19600  # argon2id
        }
        
        return mapping.get(algo, 0)
    
    def _count_cracked(self, potfile: Path) -> int:
        """Contar número de hashes crackeados"""
        if not potfile.exists():
            return 0
        
        try:
            with open(potfile, 'r') as f:
                return sum(1 for _ in f)
        except:
            return 0
