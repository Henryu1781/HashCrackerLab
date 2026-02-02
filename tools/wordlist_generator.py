#!/usr/bin/env python3
"""
Script auxiliar para criar wordlists customizadas
"""

import argparse
import sys
from pathlib import Path


def generate_patterns(output_file: Path, pattern: str, count: int):
    """Gerar wordlist baseada em padrão"""
    print(f"Gerando {count} passwords com padrão: {pattern}")
    
    with open(output_file, 'w') as f:
        for i in range(count):
            password = pattern.format(i)
            f.write(f"{password}\n")
    
    print(f"✓ Wordlist criada: {output_file}")


def combine_wordlists(output_file: Path, input_files: list):
    """Combinar múltiplas wordlists"""
    print(f"Combinando {len(input_files)} wordlists...")
    
    passwords = set()
    
    for input_file in input_files:
        try:
            with open(input_file, 'r') as f:
                for line in f:
                    passwords.add(line.strip())
        except Exception as e:
            print(f"Erro ao ler {input_file}: {e}")
    
    with open(output_file, 'w') as f:
        for pwd in sorted(passwords):
            f.write(f"{pwd}\n")
    
    print(f"✓ {len(passwords)} passwords únicos salvos em {output_file}")


def apply_rules(wordlist: Path, output_file: Path, rules: list):
    """Aplicar regras de mutação manualmente"""
    print(f"Aplicando {len(rules)} regras em {wordlist}...")
    
    with open(wordlist, 'r') as f:
        base_passwords = [line.strip() for line in f]
    
    mutated = set(base_passwords)
    
    for pwd in base_passwords:
        for rule in rules:
            if rule == 'upper':
                mutated.add(pwd.upper())
            elif rule == 'lower':
                mutated.add(pwd.lower())
            elif rule == 'capitalize':
                mutated.add(pwd.capitalize())
            elif rule == 'append_123':
                mutated.add(f"{pwd}123")
            elif rule == 'append_!':
                mutated.add(f"{pwd}!")
            elif rule == 'prepend_@':
                mutated.add(f"@{pwd}")
            elif rule == 'reverse':
                mutated.add(pwd[::-1])
            elif rule == 'leet':
                # Leet speak básico
                leet_map = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
                leet_pwd = pwd.lower()
                for char, replacement in leet_map.items():
                    leet_pwd = leet_pwd.replace(char, replacement)
                mutated.add(leet_pwd)
    
    with open(output_file, 'w') as f:
        for pwd in sorted(mutated):
            f.write(f"{pwd}\n")
    
    print(f"✓ {len(mutated)} passwords (com mutações) salvos em {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Gerador de Wordlists")
    subparsers = parser.add_subparsers(dest='command', help='Comando')
    
    # Gerar padrões
    pattern_parser = subparsers.add_parser('pattern', help='Gerar wordlist com padrão')
    pattern_parser.add_argument('-o', '--output', required=True, help='Ficheiro de saída')
    pattern_parser.add_argument('-p', '--pattern', required=True, help='Padrão (ex: password{:03d})')
    pattern_parser.add_argument('-n', '--count', type=int, default=100, help='Número de passwords')
    
    # Combinar
    combine_parser = subparsers.add_parser('combine', help='Combinar wordlists')
    combine_parser.add_argument('-o', '--output', required=True, help='Ficheiro de saída')
    combine_parser.add_argument('inputs', nargs='+', help='Wordlists a combinar')
    
    # Aplicar regras
    rules_parser = subparsers.add_parser('mutate', help='Aplicar regras de mutação')
    rules_parser.add_argument('-i', '--input', required=True, help='Wordlist base')
    rules_parser.add_argument('-o', '--output', required=True, help='Ficheiro de saída')
    rules_parser.add_argument('-r', '--rules', nargs='+', 
                             choices=['upper', 'lower', 'capitalize', 'append_123', 
                                     'append_!', 'prepend_@', 'reverse', 'leet'],
                             help='Regras a aplicar')
    
    args = parser.parse_args()
    
    if args.command == 'pattern':
        generate_patterns(Path(args.output), args.pattern, args.count)
    elif args.command == 'combine':
        combine_wordlists(Path(args.output), [Path(f) for f in args.inputs])
    elif args.command == 'mutate':
        apply_rules(Path(args.input), Path(args.output), args.rules)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
