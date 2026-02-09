"""
Gestor de Cracking
Coordena execução de hashcat/john e distribuição de trabalho
"""

import os
import sys
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
        self._hashcat_cmd = None
        self._hashcat_cwd = None

    def _resolve_hashcat_command(self):
        if self._hashcat_cmd is not None:
            return

        self._hashcat_cmd = 'hashcat'
        self._hashcat_cwd = None

        if sys.platform != "win32":
            return

        candidates = []
        env_path = os.environ.get("HASHCAT_PATH")
        if env_path:
            env_path = Path(env_path)
            if env_path.is_dir():
                candidates.extend([
                    env_path / "hashcat64.exe",
                    env_path / "hashcat.exe",
                ])
            else:
                candidates.append(env_path)

        tools_root = os.environ.get("ChocolateyToolsLocation", r"C:\tools")
        tools_root = Path(tools_root)
        if tools_root.exists():
            for p in tools_root.glob("hashcat*"):
                if p.is_dir():
                    candidates.extend([
                        p / "hashcat64.exe",
                        p / "hashcat.exe",
                    ])

        candidates.extend([
            Path(r"C:\hashcat\hashcat.exe"),
            Path(r"C:\hashcat\hashcat64.exe"),
            Path(r"C:\tools\hashcat\hashcat.exe"),
            Path(r"C:\tools\hashcat\hashcat64.exe"),
        ])

        for candidate in candidates:
            if candidate.exists():
                self._hashcat_cmd = str(candidate)
                self._hashcat_cwd = str(candidate.parent)
                break

        if self._hashcat_cwd:
            self.logger.info(f"Hashcat path resolvido: {self._hashcat_cmd}")

    def _hashcat_command(self):
        self._resolve_hashcat_command()
        return self._hashcat_cmd, self._hashcat_cwd
    
    def run_cracking(self, hashes_file: Path, output_dir: Path) -> Dict:
        """Executar cracking de todos os hashes"""
        workers_config = self.config.get('experiment', {}).get('cracking', {}).get('workers', {})
        gpu_enabled = workers_config.get('gpu', {}).get('enabled', True)
        cpu_enabled = workers_config.get('cpu', {}).get('enabled', False)
        
        # Determinar quais dispositivos testar
        devices = []
        if gpu_enabled:
            devices.append(('gpu', '2'))  # OpenCL device type 2 = GPU
        if cpu_enabled:
            devices.append(('cpu', '1'))  # OpenCL device type 1 = CPU
        
        if not devices:
            devices = [('gpu', '2')]  # Default: GPU
        
        results = {
            'total_hashes': 0,
            'cracked': 0,
            'by_algorithm': {},
            'by_mode': {},
            'by_device': {},
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
        
        # Processar cada algoritmo em cada dispositivo
        for device_name, device_type in devices:
            self.logger.info(f"\n{'='*50}")
            self.logger.info(f"Dispositivo: {device_name.upper()}")
            self.logger.info(f"{'='*50}")
            
            device_results = {
                'total_hashes': len(all_hashes),
                'cracked': 0,
                'by_algorithm': {}
            }
            
            for algo, hashes in by_algo.items():
                self.logger.info(f"[{device_name.upper()}] Processando {len(hashes)} hashes {algo}...")
                
                algo_dir = output_dir / f"{algo}_{device_name}"
                algo_results = self._crack_algorithm(
                    algo, 
                    hashes, 
                    algo_dir,
                    device_type=device_type
                )
                
                # Tag results with device
                for exec_r in algo_results['executions']:
                    exec_r['device'] = device_name
                
                algo_key = f"{algo}_{device_name}" if len(devices) > 1 else algo
                results['by_algorithm'][algo_key] = algo_results
                device_results['by_algorithm'][algo] = algo_results
                device_results['cracked'] += algo_results['cracked']
                results['executions'].extend(algo_results['executions'])
            
            results['by_device'][device_name] = device_results
            results['cracked'] = max(results['cracked'], device_results['cracked'])
        
        # Salvar resultados
        results_file = output_dir / "cracking_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        return results
    
    def _crack_algorithm(self, algo: str, hashes: List[Dict], output_dir: Path, device_type: str = None) -> Dict:
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
        
        hash_type = self._get_hashcat_type(algo, hashes)

        # Executar cada modo de cracking configurado
        for mode_config in self.cracking_config['modes']:
            mode_type = mode_config['type']
            
            self.logger.info(f"  Modo: {mode_type}")
            
            exec_result = self._execute_cracking_mode(
                algo,
                hash_file,
                mode_config,
                output_dir,
                hash_type,
                device_type=device_type
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
                                mode_config: Dict, output_dir: Path,
                                hash_type: int, device_type: str = None) -> Dict:
        """Executar um modo de cracking específico"""
        mode_type = mode_config['type']
        # Usar potfile único por algoritmo E modo
        potfile = output_dir / f"cracked_{algo}_{mode_type}.pot"
        self._current_device_type = device_type
        
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
                    algo, hash_file, mode_config, potfile, hash_type
                ))
            elif mode_type == 'brute-force':
                result.update(self._run_bruteforce_attack(
                    algo, hash_file, mode_config, potfile, hash_type
                ))
            elif mode_type == 'combinator':
                result.update(self._run_combinator_attack(
                    algo, hash_file, mode_config, potfile, hash_type
                ))
            elif mode_type == 'hybrid':
                result.update(self._run_hybrid_attack(
                    algo, hash_file, mode_config, potfile, hash_type
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
                                config: Dict, potfile: Path,
                                hash_type: int) -> Dict:
        """Executar ataque de dicionário"""
        wordlist = Path(config['wordlist'])
        rules = config.get('rules')
        
        if not wordlist.exists():
            raise FileNotFoundError(f"Wordlist não encontrada: {wordlist}")
        
        hash_file = hash_file.resolve()
        wordlist = wordlist.resolve()
        potfile = potfile.resolve()
        
        # Construir comando hashcat
        hashcat_cmd, hashcat_cwd = self._hashcat_command()
        cmd = [
            hashcat_cmd,
            '-m', str(hash_type),
            '-a', '0',  # Dictionary attack
            '--potfile-path', str(potfile),
            '--quiet',
            '--force',
            str(hash_file),
            str(wordlist)
        ]
        
        # Adicionar filtro de dispositivo (CPU=1, GPU=2)
        if getattr(self, '_current_device_type', None):
            cmd.extend(['-D', self._current_device_type])
        
        if rules:
            cmd.extend(['-r', str(rules)])
        
        # Executar
        self.logger.debug(f"Comando: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=config.get('max_time', 600),
                cwd=hashcat_cwd
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
                                config: Dict, potfile: Path,
                                hash_type: int) -> Dict:
        """Executar ataque brute-force"""
        mask = config.get('mask', '?l?l?l?l')
        max_time = config.get('max_time', 300)
        
        hashcat_cmd, hashcat_cwd = self._hashcat_command()
        hash_file = hash_file.resolve()
        potfile = potfile.resolve()

        cmd = [
            hashcat_cmd,
            '-m', str(hash_type),
            '-a', '3',  # Brute-force
            '--potfile-path', str(potfile),
            '--quiet',
            '--force',
            str(hash_file),
            mask
        ]
        
        # Adicionar filtro de dispositivo (CPU=1, GPU=2)
        if getattr(self, '_current_device_type', None):
            cmd.extend(['-D', self._current_device_type])
        
        self.logger.debug(f"Comando: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=max_time,
                cwd=hashcat_cwd
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
            
    def _run_combinator_attack(self, algo: str, hash_file: Path,
                               config: Dict, potfile: Path,
                               hash_type: int) -> Dict:
        """Executar ataque Combinator (-a 1)"""
        max_time = config.get('max_time', 300)
        hashcat_cmd, hashcat_cwd = self._hashcat_command()
        hash_file = hash_file.resolve()
        potfile = potfile.resolve()
        
        # Combinator requer 2 wordlists ou 2x a mesma
        wl_left = Path(config.get('wordlist_left', config.get('wordlist')))
        wl_right = Path(config.get('wordlist_right', config.get('wordlist')))

        cmd = [
            hashcat_cmd, '-m', str(hash_type), '-a', '1',
            '--potfile-path', str(potfile), '--quiet', '--force',
            str(hash_file), str(wl_left), str(wl_right)
        ]
        
        # Adicionar filtro de dispositivo (CPU=1, GPU=2)
        if getattr(self, '_current_device_type', None):
            cmd.extend(['-D', self._current_device_type])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=max_time, cwd=hashcat_cwd)
            return {'command': ' '.join(cmd), 'cracked': self._count_cracked(potfile), 'returncode': result.returncode}
        except subprocess.TimeoutExpired:
            return {'command': ' '.join(cmd), 'cracked': self._count_cracked(potfile), 'timeout': True}

    def _run_hybrid_attack(self, algo: str, hash_file: Path,
                           config: Dict, potfile: Path,
                           hash_type: int) -> Dict:
        """Executar ataque Híbrido (-a 6 ou -a 7)"""
        max_time = config.get('max_time', 300)
        hashcat_cmd, hashcat_cwd = self._hashcat_command()
        hash_file = hash_file.resolve()
        potfile = potfile.resolve()
        
        mode = '6'  # Wordlist + Mask (default)
        if config.get('reverse', False):
            mode = '7'  # Mask + Wordlist

        wordlist = Path(config.get('wordlist')).resolve()
        mask = config.get('mask', '?d?d?d?d')
        
        # Ordem dos args: hash wordlist mask OU hash mask wordlist
        args = [str(hash_file), str(wordlist), mask] if mode == '6' else [str(hash_file), mask, str(wordlist)]

        cmd = [
            hashcat_cmd, '-m', str(hash_type), '-a', mode,
            '--potfile-path', str(potfile), '--quiet', '--force'
        ] + args
        
        # Adicionar filtro de dispositivo (CPU=1, GPU=2)
        if getattr(self, '_current_device_type', None):
            cmd.extend(['-D', self._current_device_type])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=max_time, cwd=hashcat_cwd)
            return {'command': ' '.join(cmd), 'cracked': self._count_cracked(potfile), 'returncode': result.returncode}
        except subprocess.TimeoutExpired:
            return {'command': ' '.join(cmd), 'cracked': self._count_cracked(potfile), 'timeout': True}
    
    def _get_hashcat_type(self, algo: str, hashes: List[Dict] = None) -> int:
        """Mapear algoritmo para hash-type do hashcat"""
        
        # Check for salted variants
        if hashes:
            has_salt = any(h.get('salt') for h in hashes)
            if has_salt:
                if algo == 'md5':
                    # mode 10 = md5($pass.$salt), mode 20 = md5($salt.$pass)
                    # src/hash_generator.py lines 167-172: salt + password
                    # So it's md5($salt.$pass) which is mode 20
                    return 20 
                elif algo == 'sha256':
                    # mode 1410 = sha256($pass.$salt), mode 1420 = sha256($salt.$pass)
                    # generator: salt + password -> mode 1420
                    return 1420
                elif algo == 'sha1':
                    # mode 110 = sha1($pass.$salt), mode 120 = sha1($salt.$pass)
                    # generator: salt + password -> mode 120
                    return 120

        mapping = {
            'md5': 0,
            'sha1': 100,
            'sha256': 1400,
            'bcrypt': 3200,
            'scrypt': 8900,
            'pbkdf2_sha256': 10900,
            'argon2': 34000  # argon2id
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
