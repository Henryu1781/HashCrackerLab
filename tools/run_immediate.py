#!/usr/bin/env python3
"""
Execução imediata do Hash Cracker Lab (LAB isolado)
- Garante diretórios mínimos
- Garante wordlist mínima
- Valida ambiente (opcional)
- Executa orquestrador (quick_test por default)
"""

import argparse
import subprocess
import sys
from pathlib import Path

DEFAULT_CONFIG = "config/quick_test.yaml"
MIN_WORDLIST = "wordlists/rockyou-small.txt"


def ensure_dirs():
    required_dirs = [
        "wordlists",
        "rules",
        "captures",
        "results",
        "logs",
        "hashes",
        "temp",
    ]
    for d in required_dirs:
        Path(d).mkdir(parents=True, exist_ok=True)


def ensure_wordlist():
    wl = Path(MIN_WORDLIST)
    if wl.exists():
        return
    wl.parent.mkdir(parents=True, exist_ok=True)
    sample = [
        "password\n",
        "Password123\n",
        "test123\n",
        "test001\n",
        "test002\n",
        "test003\n",
        "test004\n",
        "test005\n",
        "admin\n",
        "admin123\n",
        "qwerty\n",
        "letmein\n",
        "abc123\n",
        "password123\n",
        "123456\n",
        "monkey\n",
        "dragon\n",
        "master\n",
        "sunshine\n",
        "princess\n",
    ]
    wl.write_text("".join(sample), encoding="utf-8")
    print(f"⚠️  Wordlist mínima criada com {len(sample)} senhas (modo teste apenas)")


def has_hashcat() -> bool:
    try:
        subprocess.run(
            ["hashcat", "--help"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2,
            check=False,
        )
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def run_validate_environment():
    cmd = [sys.executable, "tools/validate_environment.py"]
    return subprocess.run(cmd).returncode


def run_orchestrator(config_path: str, dry_run: bool):
    cmd = [sys.executable, "orchestrator.py", "--config", config_path]
    if dry_run:
        cmd.append("--dry-run")
    return subprocess.run(cmd).returncode


def main():
    parser = argparse.ArgumentParser(description="Execução imediata do Hash Cracker Lab")
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="Config YAML a usar")
    parser.add_argument("--skip-validation", action="store_true", help="Ignorar validação do ambiente")
    parser.add_argument("--dry-run", action="store_true", help="Executar sem cracking (validação)")
    )
    args = parser.parse_args()

    ensure_dirs()
    ensure_wordlist()

    if not args.skip_validation:
        run_validate_environment()

    dry_run = args.dry_run
    if not has_hashcat() and not dry_run:
        print("⚠ Hashcat não encontrado. A executar em modo --dry-run.")
        dry_run = True

    return run_orchestrator(args.config, dry_run)


if __name__ == "__main__":
    sys.exit(main())
