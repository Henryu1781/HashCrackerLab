"""
Gerador de Hashes
Cria hashes sintéticos para testes
"""

import json
import hashlib
import secrets
import random
import logging
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# Imports para algoritmos modernos
import bcrypt
from argon2 import PasswordHasher
from argon2.low_level import hash_secret, Type
from passlib.hash import scrypt, pbkdf2_sha256


class HashGenerator:
    """Gerador de hashes para testes"""
    
    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.hash_config = config['experiment']['hash_generation']
        self.seed = config['experiment'].get('seed')
        self.deterministic_salts = config['experiment'].get('deterministic_salts', False)
        self._rng = random.Random(self.seed) if self.seed is not None else random.Random()
    
    def generate_hashes(self, output_file: Path) -> List[Dict]:
        """Gerar todos os hashes configurados"""
        hashes = []
        count = self.hash_config['count']
        algorithms = self.hash_config['algorithms']
        
        self.logger.info(f"Gerando {count} hashes para {len(algorithms)} algoritmos...")
        
        for i in range(count):
            # Gerar password sintética
            password = self._generate_password(i)
            
            # Gerar hash para cada algoritmo
            for algo_config in algorithms:
                algo_name = algo_config['name']
                
                try:
                    hash_data = self._generate_hash(password, algo_config, i)
                    hashes.append(hash_data)
                except Exception as e:
                    self.logger.error(f"Erro ao gerar hash {algo_name}: {e}")
        
        # Salvar hashes
        self._save_hashes(hashes, output_file)
        self.logger.info(f"{len(hashes)} hashes salvos em {output_file}")
        
        return hashes
    
    def _generate_password(self, index: int) -> str:
        """Gerar password sintética baseada em padrões"""
        patterns = self.hash_config.get('password_patterns', ["password{:03d}"])
        pattern = patterns[index % len(patterns)]
        return pattern.format(index)
    
    def _generate_hash(self, password: str, algo_config: Dict, uid: int) -> Dict:
        """Gerar hash individual"""
        algo = algo_config['name']
        
        # Validar algoritmo
        valid_algos = ['argon2', 'bcrypt', 'scrypt', 'pbkdf2_sha256', 'sha256', 'sha1', 'md5']
        if algo not in valid_algos:
            raise ValueError(f"Algoritmo não suportado: {algo}. Suportados: {valid_algos}")
        
        hash_data = {
            'uid': uid,
            'algorithm': algo,
            'password': password,  # Guardado para verificacao ([WARNING] NAO fazer em producao! Dados sensiveis!)
            'timestamp': datetime.now().isoformat(),
        }
        
        if algo == 'argon2':
            cost = algo_config.get('cost', 16)
            iterations = algo_config.get('iterations', 3)
            salt = self._get_salt_bytes(16)
            
            # Use hash_secret to get PHC string (needed for hashcat mode 19600)
            hash_bytes = hash_secret(
                secret=password.encode(),
                salt=salt,
                time_cost=iterations,
                memory_cost=cost * 1024,
                parallelism=1,
                hash_len=32,
                type=Type.ID
            )
            
            hash_data.update({
                'hash': hash_bytes.decode('utf-8'),
                'salt': salt.hex(),
                'cost': cost,
                'iterations': iterations,
                'mode': 'argon2id'
            })
        
        elif algo == 'bcrypt':
            cost = algo_config.get('cost', 12)
            hash_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=cost))
            
            hash_data.update({
                'hash': hash_bytes.decode(),
                'cost': cost
            })
        
        elif algo == 'scrypt':
            n = algo_config.get('n', 16384)
            r = algo_config.get('r', 8)
            p = algo_config.get('p', 1)
            
            hash_str = scrypt.using(salt_size=16, rounds=n, block_size=r, parallelism=p).hash(password)
            
            hash_data.update({
                'hash': hash_str,
                'n': n,
                'r': r,
                'p': p
            })
        
        elif algo == 'pbkdf2_sha256':
            iterations = algo_config.get('iterations', 100000)
            hash_str = pbkdf2_sha256.using(rounds=iterations).hash(password)
            
            hash_data.update({
                'hash': hash_str,
                'iterations': iterations
            })
        
        elif algo == 'sha256':
            salt_enabled = algo_config.get('salt', True)
            if salt_enabled:
                salt = self._get_salt_hex(16)
                hash_input = (salt + password).encode()
            else:
                salt = None
                hash_input = password.encode()
            
            hash_hex = hashlib.sha256(hash_input).hexdigest()
            
            hash_data.update({
                'hash': hash_hex,
                'salt': salt
            })
        
        elif algo == 'sha1':
            salt_enabled = algo_config.get('salt', False)
            if salt_enabled:
                salt = self._get_salt_hex(16)
                hash_input = (salt + password).encode()
            else:
                salt = None
                hash_input = password.encode()
            
            hash_hex = hashlib.sha1(hash_input).hexdigest()
            
            hash_data.update({
                'hash': hash_hex,
                'salt': salt
            })
        
        elif algo == 'md5':
            salt_enabled = algo_config.get('salt', False)
            if salt_enabled:
                salt = self._get_salt_hex(16)
                hash_input = (salt + password).encode()
            else:
                salt = None
                hash_input = password.encode()
            
            hash_hex = hashlib.md5(hash_input).hexdigest()
            
            hash_data.update({
                'hash': hash_hex,
                'salt': salt
            })
        
        else:
            raise ValueError(f"Algoritmo não suportado: {algo}")
        
        return hash_data

    def _get_salt_bytes(self, length: int) -> bytes:
        """Obter salt em bytes (determinístico se configurado)"""
        if self.deterministic_salts and self.seed is not None:
            return self._rng.getrandbits(length * 8).to_bytes(length, 'big')
        return secrets.token_bytes(length)

    def _get_salt_hex(self, length_bytes: int) -> str:
        """Obter salt em hex (determinístico se configurado)"""
        return self._get_salt_bytes(length_bytes).hex()
    
    def _save_hashes(self, hashes: List[Dict], output_file: Path):
        """Salvar hashes em formato JSON"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(hashes, f, indent=2)
        
        # Criar também ficheiros separados por algoritmo (para hashcat)
        by_algo = {}
        for h in hashes:
            algo = h['algorithm']
            if algo not in by_algo:
                by_algo[algo] = []
            by_algo[algo].append(h)
        
        for algo, algo_hashes in by_algo.items():
            algo_file = output_file.parent / f"{algo}_hashes.txt"
            with open(algo_file, 'w') as f:
                for h in algo_hashes:
                    # Formato: hash ou salt:hash
                    if h.get('salt'):
                        f.write(f"{h['salt']}:{h['hash']}\n")
                    else:
                        f.write(f"{h['hash']}\n")
