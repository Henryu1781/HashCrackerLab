#!/usr/bin/env python3
"""
Script de Teste Simples
Executa um teste básico sem hashcat para verificar a infraestrutura
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from colorama import init, Fore, Style

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.hash_generator import HashGenerator
import logging

init(autoreset=True)

def simple_test():
    """Teste simples de geração de hashes"""
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Hash Cracker Lab - Teste Simples{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    # Configuração mínima
    config = {
        'experiment': {
            'name': 'simple_test',
            'hash_generation': {
                'count': 5,
                'algorithms': [
                    {'name': 'md5', 'salt': False},
                    {'name': 'sha256', 'salt': True},
                ],
                'password_patterns': ['test{}', 'password{}']
            }
        }
    }
    
    # Setup logging
    logger = logging.getLogger('SimpleTest')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(handler)
    
    # Criar output dir
    output_dir = Path('results') / f'simple_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Teste 1: Geração de hashes
        print(f"{Fore.YELLOW}[1/3] Gerando hashes...{Style.RESET_ALL}")
        generator = HashGenerator(config, logger)
        hashes_file = output_dir / 'hashes.json'
        hashes = generator.generate_hashes(hashes_file)
        print(f"{Fore.GREEN}✓ {len(hashes)} hashes gerados{Style.RESET_ALL}\n")
        
        # Teste 2: Verificar ficheiro
        print(f"{Fore.YELLOW}[2/3] Verificando ficheiro...{Style.RESET_ALL}")
        with open(hashes_file, 'r') as f:
            data = json.load(f)
        print(f"{Fore.GREEN}✓ Ficheiro JSON válido{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Contém {len(data)} entradas{Style.RESET_ALL}\n")
        
        # Teste 3: Exibir amostra
        print(f"{Fore.YELLOW}[3/3] Amostra de hashes gerados:{Style.RESET_ALL}")
        for i, h in enumerate(data[:3]):
            print(f"\n  Hash {i+1}:")
            print(f"    Algoritmo: {h['algorithm']}")
            print(f"    Password:  {h['password']}")
            print(f"    Hash:      {h['hash'][:40]}...")
        
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Teste concluído com sucesso!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Resultados em: {output_dir}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
        
        return 0
    
    except Exception as e:
        print(f"\n{Fore.RED}✗ Erro: {e}{Style.RESET_ALL}\n")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(simple_test())
