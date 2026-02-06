#!/usr/bin/env python3
"""
Script para validar ambiente e dependências
"""

import sys
import subprocess
import importlib
from pathlib import Path


def check_python_version():
    """Verificar versão Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} (requerido >= 3.8)")
        return False


def check_python_packages():
    """Verificar pacotes Python"""
    required = [
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
    
    for package in required:
        try:
            importlib.import_module(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package}")
            missing.append(package)
    
    if missing:
        print(f"\nInstalar: pip install {' '.join(missing)}")
        return False
    
    return True


def check_system_tools():
    """Verificar ferramentas do sistema"""
    import os
    import glob
    
    # Caminhos comuns no Windows para adicionar ao PATH temporariamente
    common_paths = [
        r"C:\hashcat",
        r"C:\tools",
        r"C:\tools\hashcat",
        r"C:\Program Files\Wireshark",
        r"C:\aircrack-ng\aircrack-ng-1.7-win\bin",
        r"C:\Program Files\Aircrack-ng-1.7\bin"
    ]
    
    # Procurar versoes do hashcat em C:\tools (ex: hashcat-6.2.6)
    for p in glob.glob(r"C:\tools\hashcat-*"):
        if os.path.isdir(p):
            common_paths.append(p)
    
    for p in common_paths:
        if os.path.exists(p) and p not in os.environ["PATH"]:
            os.environ["PATH"] += os.pathsep + p

    tools = {
        'hashcat': 'Hashcat',
        'aircrack-ng': 'Aircrack-ng',
        'airodump-ng': 'Airodump-ng',
        'aireplay-ng': 'Aireplay-ng',
        'tshark': 'Wireshark/tshark'
    }
    
    missing = []
    
    for cmd, name in tools.items():
        found = False
        # Tentar executar comando direto
        try:
            subprocess.run([cmd, '--help'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL,
                         timeout=5)
            print(f"✓ {name}")
            found = True
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
             # Se falhar, tentar verificar existencia do executavel nos caminhos comuns manualmente
             # (Fallback caso subprocess falhe por permissoes mas arquivo exista)
             exe_name = cmd + ".exe" if sys.platform == "win32" else cmd
             for path in common_paths:
                 full_path = os.path.join(path, exe_name)
                 if os.path.exists(full_path):
                     print(f"✓ {name} (encontrado em {path})")
                     found = True
                     # Adicionar ao PATH para o resto do script
                     if path not in os.environ["PATH"]:
                         os.environ["PATH"] += os.pathsep + path
                     break
        
        if not found:
            print(f"✗ {name}")
            missing.append(name)
    
    if missing:
        print(f"\nFerramentas faltando: {', '.join(missing)}")
        return False
    
    return True


def check_gpu_support():
    """Verificar suporte GPU"""
    try:
        result = subprocess.run(
            ['hashcat', '-I'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        output = result.stdout + result.stderr
        
        if 'CUDA' in output or 'OpenCL' in output:
            print("✓ GPU detectada pelo Hashcat")
            return True
        else:
            print("⚠ Nenhuma GPU detectada (CPU apenas)")
            return True  # Não é crítico
    except:
        print("⚠ Não foi possível verificar GPU")
        return True


def check_directories():
    """Verificar estrutura de diretórios"""
    required_dirs = [
        'wordlists',
        'rules',
        'captures',
        'results',
        'logs',
        'hashes',
        'temp',
        'src',
        'config'
    ]
    
    missing = []
    
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✓ {dir_name}/")
        else:
            print(f"✗ {dir_name}/")
            missing.append(dir_name)
    
    if missing:
        print(f"\nCriar: mkdir -p {' '.join(missing)}")
        return False
    
    return True


def main():
    """Executar todas as verificações"""
    print("="*50)
    print("Hash Cracker Lab - Validação de Ambiente")
    print("="*50)
    
    checks = [
        ("Versão Python", check_python_version),
        ("Pacotes Python", check_python_packages),
        ("Ferramentas do Sistema", check_system_tools),
        ("Suporte GPU", check_gpu_support),
        ("Estrutura de Diretórios", check_directories)
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 50)
        result = check_func()
        results.append((name, result))
    
    print("\n" + "="*50)
    print("RESUMO")
    print("="*50)
    
    all_passed = True
    for name, result in results:
        status = "✓ OK" if result else "✗ FALHOU"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("="*50)
    
    if all_passed:
        print("\n✓ Ambiente pronto para uso!")
        return 0
    else:
        print("\n✗ Corrija os problemas antes de prosseguir")
        return 1


if __name__ == "__main__":
    sys.exit(main())
