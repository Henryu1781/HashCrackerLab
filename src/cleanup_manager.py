"""
Gestor de Limpeza
Remove dados sensíveis após testes
"""

import os
import shutil
import hashlib
import logging
import time
import threading
from pathlib import Path
from typing import Dict
from datetime import datetime


class CleanupManager:
    """Gestor de limpeza e segurança de dados"""
    
    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.cleanup_log = []
    
    def schedule_cleanup(self, target_dir: Path, delay: int = 0):
        """Agendar limpeza após delay (segundos)"""
        if delay > 0:
            self.logger.info(f"Limpeza agendada para {delay}s")
            timer = threading.Timer(delay, self.cleanup, args=[target_dir])
            timer.daemon = True
            timer.start()
        else:
            self.cleanup(target_dir)
    
    def cleanup(self, target_dir: Path):
        """Executar limpeza de dados sensíveis"""
        self.logger.info(f"Iniciando limpeza: {target_dir}")
        
        cleanup_report = {
            'timestamp': datetime.now().isoformat(),
            'target_dir': str(target_dir),
            'actions': [],
            'checksums_before': {},
            'checksums_after': {}
        }
        
        try:
            # 1. Calcular checksums antes
            cleanup_report['checksums_before'] = self._calculate_checksums(target_dir)
            
            # 2. Remover ficheiros sensíveis
            sensitive_patterns = [
                '*/hashes/generated_hashes.json',  # Hashes com passwords
                '*/cracked/*.pot',  # Resultados de cracking
                '**/temp/*'  # Temporários
            ]
            
            for pattern in sensitive_patterns:
                for file_path in target_dir.glob(pattern):
                    if file_path.is_file():
                        self._secure_delete(file_path)
                        cleanup_report['actions'].append({
                            'action': 'deleted',
                            'file': str(file_path)
                        })
            
            # 3. Anonimizar logs
            log_files = list(target_dir.glob('**/logs/*.log'))
            for log_file in log_files:
                self._anonymize_log(log_file)
                cleanup_report['actions'].append({
                    'action': 'anonymized',
                    'file': str(log_file)
                })
            
            # 4. Calcular checksums depois
            cleanup_report['checksums_after'] = self._calculate_checksums(target_dir)
            
            # 5. Salvar relatório de limpeza
            report_file = target_dir / "CLEANUP_REPORT.json"
            import json
            with open(report_file, 'w') as f:
                json.dump(cleanup_report, f, indent=2)
            
            self.logger.info(f"✓ Limpeza concluída: {len(cleanup_report['actions'])} ações")
        
        except Exception as e:
            self.logger.error(f"Erro durante limpeza: {e}")
    
    def _secure_delete(self, file_path: Path):
        """Deletar ficheiro de forma segura (sobrescrever antes)"""
        try:
            # Sobrescrever com dados aleatórios
            if file_path.exists() and file_path.is_file():
                file_size = file_path.stat().st_size
                
                with open(file_path, 'wb') as f:
                    # Passar 1: zeros
                    f.write(b'\x00' * file_size)
                    f.flush()
                    os.fsync(f.fileno())
                    
                    # Passar 2: uns
                    f.seek(0)
                    f.write(b'\xff' * file_size)
                    f.flush()
                    os.fsync(f.fileno())
                    
                    # Passar 3: aleatório
                    f.seek(0)
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
                
                # Remover ficheiro
                file_path.unlink()
                self.logger.debug(f"Deletado: {file_path}")
        
        except Exception as e:
            self.logger.error(f"Erro ao deletar {file_path}: {e}")
    
    def _anonymize_log(self, log_file: Path):
        """Remover informações sensíveis de logs"""
        try:
            with open(log_file, 'r') as f:
                content = f.read()
            
            # Remover padrões sensíveis
            import re
            
            # IPs privados
            content = re.sub(r'\b192\.168\.\d{1,3}\.\d{1,3}\b', 'IP.REDACTED', content)
            content = re.sub(r'\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', 'IP.REDACTED', content)
            
            # MACs
            content = re.sub(r'\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b', 'MAC.REDACTED', content)
            
            # Possíveis passwords em logs
            content = re.sub(r'password["\']?\s*[:=]\s*["\']?[\w!@#$%^&*]+["\']?', 'password=REDACTED', content, flags=re.IGNORECASE)
            
            # Sobrescrever log
            with open(log_file, 'w') as f:
                f.write(content)
            
            self.logger.debug(f"Anonimizado: {log_file}")
        
        except Exception as e:
            self.logger.error(f"Erro ao anonimizar {log_file}: {e}")
    
    def _calculate_checksums(self, directory: Path) -> Dict[str, str]:
        """Calcular checksums de todos os ficheiros"""
        checksums = {}
        
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                try:
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()
                    
                    rel_path = file_path.relative_to(directory)
                    checksums[str(rel_path)] = file_hash
                except:
                    pass
        
        return checksums
    
    def verify_cleanup(self, cleanup_report_file: Path) -> bool:
        """Verificar se limpeza foi realizada corretamente"""
        import json
        
        try:
            with open(cleanup_report_file, 'r') as f:
                report = json.load(f)
            
            # Verificar se ficheiros sensíveis foram removidos
            for action in report['actions']:
                if action['action'] == 'deleted':
                    file_path = Path(action['file'])
                    if file_path.exists():
                        self.logger.error(f"Ficheiro ainda existe: {file_path}")
                        return False
            
            self.logger.info("✓ Limpeza verificada com sucesso")
            return True
        
        except Exception as e:
            self.logger.error(f"Erro ao verificar limpeza: {e}")
            return False
