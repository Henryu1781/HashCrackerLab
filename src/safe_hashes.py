"""
Gestor Seguro de Hashes
Remove passwords sensíveis e fornece versão "safe" do JSON
"""

import json
from pathlib import Path
from typing import List, Dict, Any


class SafeHashesManager:
    """Gestor de hashes com modo seguro (sem passwords)"""
    
    @staticmethod
    def create_safe_version(hashes: List[Dict], output_file: Path):
        """
        Criar versão "segura" de hashes sem passwords em plaintext
        
        Args:
            hashes: Lista de hashes gerados
            output_file: Caminho para guardar versão segura
        """
        safe_hashes = []
        
        for h in hashes:
            safe_hash = {
                'uid': h['uid'],
                'algorithm': h['algorithm'],
                'hash': h['hash'],
                'timestamp': h['timestamp'],
                # Metadata sem password
            }
            
            # Incluir salt se existir (é derivado, não é secreto)
            if 'salt' in h:
                safe_hash['salt'] = h['salt']
            
            # Incluir parâmetros (custo, iterações, etc.)
            for key in ['cost', 'iterations', 'n', 'r', 'p', 'mode']:
                if key in h:
                    safe_hash[key] = h[key]
            
            safe_hashes.append(safe_hash)
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(safe_hashes, f, indent=2)
        
        return len(safe_hashes)
    
    @staticmethod
    def create_password_file(hashes: List[Dict], output_file: Path, 
                            encrypt: bool = False, encryption_key: str = None):
        """
        Criar ficheiro separado com passwords (para validação apenas)
        
        ⚠️  AVISO: Este ficheiro contém dados MUITO sensíveis!
        Deve ser:
        - Guardado em locação segura
        - Deletado imediatamente após validação
        - Nunca commitado em git
        - Criptografado se em armazenamento
        
        Args:
            hashes: Lista de hashes
            output_file: Caminho para guardar
            encrypt: Se True, criptografar com encryption_key
            encryption_key: Chave de criptografia (se encrypt=True)
        """
        password_data = []
        
        for h in hashes:
            password_data.append({
                'uid': h['uid'],
                'algorithm': h['algorithm'],
                'password': h['password'],  # ⚠️ SENSÍVEL!
                'hash': h['hash']
            })
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if encrypt:
            if not encryption_key:
                raise ValueError("encryption_key é obrigatório para encriptação")
            
            try:
                from cryptography.fernet import Fernet
                import base64
                import hashlib
                
                # Derivar chave de encriptação da password
                key = base64.urlsafe_b64encode(
                    hashlib.sha256(encryption_key.encode()).digest()
                )
                cipher = Fernet(key)
                
                plaintext = json.dumps(password_data)
                ciphertext = cipher.encrypt(plaintext.encode())
                
                with open(output_file, 'wb') as f:
                    f.write(ciphertext)
            except ImportError:
                raise ImportError("Instale 'cryptography' para encriptação: pip install cryptography")
        else:
            # Escrever em plaintext COM AVISO
            with open(output_file, 'w') as f:
                f.write("# ⚠️  FICHEIRO MUITO SENSÍVEL! CONTÉM PASSWORDS!\n")
                f.write("# DELETE APÓS USAR\n")
                f.write("# NUNCA COMMITAR EM GIT\n\n")
                json.dump(password_data, f, indent=2)
        
        # Avisar utilizador
        import os
        os.chmod(output_file, 0o600)  # read/write owner only
        
        return len(password_data)
