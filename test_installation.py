#!/usr/bin/env python3
"""
Script de Validação do Ambiente
Verifica se todas as dependências estão instaladas
"""

import sys
import importlib
import subprocess
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

def check_python_packages():
    """Verificar pacotes Python"""
    print(f"\n{Fore.CYAN}[1/4] Verificando pacotes Python...{Style.RESET_ALL}")
    
    packages = [
        'yaml',
        'passlib',
        'argon2',
        'bcrypt',
        'cryptography',
        'psutil',
        'colorama',
        'tabulate',
        'tqdm'
    ]
    
    missing = []
    for package in packages:
        try:
            importlib.import_module(package)
            print(f"{Fore.GREEN}  ✓ {package}{Style.RESET_ALL}")
        except ImportError:
            print(f"{Fore.RED}  ✗ {package}{Style.RESET_ALL}")
            missing.append(package)
    
    if missing:
        print(f"\n{Fore.YELLOW}Instalar com: pip install -r requirements.txt{Style.RESET_ALL}")
        return False
    
    return True

def check_system_tools():
    """Verificar ferramentas do sistema"""
    print(f"\n{Fore.CYAN}[2/4] Verificando ferramentas do sistema...{Style.RESET_ALL}")
    
    tools = {
        'hashcat': 'hashcat --version',
        'aircrack-ng': 'aircrack-ng --help',
        'ip': 'ip -V'
    }
    
    available = {}
    for tool, cmd in tools.items():
        try:
            result = subprocess.run(
                cmd.split(),
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0 or tool == 'aircrack-ng':  # aircrack retorna erro em --help
                print(f"{Fore.GREEN}  ✓ {tool}{Style.RESET_ALL}")
                available[tool] = True
            else:
                print(f"{Fore.YELLOW}  ~ {tool} (não obrigatório){Style.RESET_ALL}")
                available[tool] = False
        except:
            print(f"{Fore.YELLOW}  ~ {tool} (não instalado){Style.RESET_ALL}")
            available[tool] = False
    
    return True  # Não é crítico

def check_project_structure():
    """Verificar estrutura do projeto"""
    print(f"\n{Fore.CYAN}[3/4] Verificando estrutura do projeto...{Style.RESET_ALL}")
    
    required_paths = [
        'src/__init__.py',
        'src/hash_generator.py',
        'src/cracking_manager.py',
        'src/metrics_collector.py',
        'src/network_manager.py',
        'src/cleanup_manager.py',
        'config/quick_test.yaml',
        'orchestrator.py',
        'requirements.txt'
    ]
    
    base_dir = Path(__file__).parent
    missing = []
    
    for path in required_paths:
        full_path = base_dir / path
        if full_path.exists():
            print(f"{Fore.GREEN}  ✓ {path}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}  ✗ {path}{Style.RESET_ALL}")
            missing.append(path)
    
    if missing:
        return False
    
    return True

def check_configurations():
    """Verificar configurações"""
    print(f"\n{Fore.CYAN}[4/4] Verificando configurações...{Style.RESET_ALL}")
    
    base_dir = Path(__file__).parent
    config_files = list((base_dir / 'config').glob('*.yaml'))
    
    if not config_files:
        print(f"{Fore.RED}  ✗ Nenhum ficheiro de configuração encontrado{Style.RESET_ALL}")
        return False
    
    for config in config_files:
        print(f"{Fore.GREEN}  ✓ {config.name}{Style.RESET_ALL}")
    
    # Verificar wordlist
    wordlist = base_dir / 'wordlists' / 'rockyou-small.txt'
    if wordlist.exists():
        print(f"{Fore.GREEN}  ✓ wordlist de teste{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}  ~ wordlist de teste (criando...){Style.RESET_ALL}")
    
    return True

def main():
    """Executar todas as verificações"""
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Hash Cracker Lab - Validação de Instalação{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    results = []
    results.append(("Pacotes Python", check_python_packages()))
    results.append(("Ferramentas Sistema", check_system_tools()))
    results.append(("Estrutura Projeto", check_project_structure()))
    results.append(("Configurações", check_configurations()))
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}RESUMO{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    all_ok = True
    for check_name, result in results:
        status = f"{Fore.GREEN}PASS{Style.RESET_ALL}" if result else f"{Fore.RED}FAIL{Style.RESET_ALL}"
        print(f"  {check_name:.<40} {status}")
        all_ok = all_ok and result
    
    print()
    
    if all_ok:
        print(f"{Fore.GREEN}✓ Sistema pronto para uso!{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Próximos passos:{Style.RESET_ALL}")
        print(f"  1. python orchestrator.py --config config/quick_test.yaml")
        print(f"  2. Consultar: QUICKSTART.md\n")
        return 0
    else:
        print(f"{Fore.RED}✗ Alguns componentes falharam{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Consultar: README.md para instalação{Style.RESET_ALL}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
