#!/usr/bin/env python3

"""

Telnet Trfego com Autenticao e Hash

Gera trfego simulado com username/password/hash para captura



Uso:

    python telnet_authenticated_traffic.py --target 192.168.100.1 --user duarte --password Cibersegura

    python telnet_authenticated_traffic.py --target 192.168.100.1 --wordlist wordlists/custom.txt

"""



import socket

import hashlib

import random

import time

import argparse

import sys

from datetime import datetime

from pathlib import Path

from typing import Tuple, Optional



class AuthenticatedTelnet:

    """Simula trfego Telnet com autenticao"""

    

    TELNET_PORT = 23

    

    def __init__(self, target_host: str, target_port: int = 23, 

                 username: str = "user", password: str = "pass",

                 hash_algo: str = "sha256", verbose: bool = False):

        self.target_host = target_host

        self.target_port = target_port

        self.username = username

        self.password = password

        self.hash_algo = hash_algo

        self.verbose = verbose

        self.credentials_sent = []

        

    def hash_password(self, password: str) -> str:

        """Hash a password"""

        if self.hash_algo == "md5":

            return hashlib.md5(password.encode()).hexdigest()

        elif self.hash_algo == "sha256":

            return hashlib.sha256(password.encode()).hexdigest()

        elif self.hash_algo == "sha1":

            return hashlib.sha1(password.encode()).hexdigest()

        else:

            return password  # plaintext

    

    def connect_and_authenticate(self) -> bool:

        """Simula conexo Telnet com autenticao"""

        try:

            print(f" Conectando a {self.target_host}:{self.target_port}...")

            

            # Criar socket

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            sock.settimeout(5)

            

            # Conectar

            sock.connect((self.target_host, self.target_port))

            

            if self.verbose:

                print(f" Conectado!")

                print(f"   Enviando autenticao...")

            

            # 1. Enviar username (plaintext - visvel em Wireshark)

            auth_packet = f"{self.username}\r\n"

            sock.send(auth_packet.encode())

            

            if self.verbose:

                print(f"    Username: {self.username}")

            

            time.sleep(0.5)

            

            # 2. Enviar password com hash

            password_hash = self.hash_password(self.password)

            auth_packet = f"{password_hash}\r\n"

            sock.send(auth_packet.encode())

            

            if self.verbose:

                print(f"    Password ({self.hash_algo}): {password_hash[:16]}...")

            

            # 3. Enviar dados (simulando utilizao)

            time.sleep(0.3)

            messages = [

                "ls -la\r\n",

                "cat /etc/passwd\r\n",

                "id\r\n",

                "whoami\r\n",

            ]

            

            for msg in messages:

                sock.send(msg.encode())

                if self.verbose:

                    print(f"    Comando: {msg.strip()}")

                time.sleep(random.uniform(0.1, 0.5))

            

            # 4. Desconectar gracefully

            sock.send(b"exit\r\n")

            sock.close()

            

            # Registar

            self.credentials_sent.append({

                "timestamp": datetime.now().isoformat(),

                "username": self.username,

                "password": self.password,

                "password_hash": self.hash_password(self.password),

                "hash_algo": self.hash_algo,

                "target": f"{self.target_host}:{self.target_port}"

            })

            

            return True

            

        except socket.timeout:

            print(f"  Timeout - servidor no respondeu (OK para demo)")

            return False

        except ConnectionRefusedError:

            print(f" Conexo recusada - servidor no est a ouvir (OK para demo)")

            return False

        except Exception as e:

            print(f" Erro: {e}")

            return False

    

    def generate_multiple_connections(self, count: int = 5, interval: float = 1.0):

        """Gera mltiplas conexes com diferentes credenciais"""

        passwords = [

            "Cibersegura",

            "password123",

            "admin123",

            "test123",

            "secret"

        ]

        

        for i in range(count):

            pwd = passwords[i % len(passwords)]

            self.password = pwd

            

            print(f"\n[{i+1}/{count}] Conexo com password '{pwd}'...")

            

            self.connect_and_authenticate()

            

            if i < count - 1:

                time.sleep(interval)

        

        return self.credentials_sent

    

    def save_credentials_log(self, output_file: str = "captured_credentials.json"):

        """Salva log de credenciais para extrao posterior"""

        import json

        

        Path(output_file).parent.mkdir(exist_ok=True)

        

        with open(output_file, 'w', encoding='utf-8') as f:

            json.dump(self.credentials_sent, f, indent=2, ensure_ascii=False)

        

        print(f"\n Log de credenciais salvo: {output_file}")

        

        # Mostrar para confirmao

        print("\nCredenciais enviadas:")

        for cred in self.credentials_sent:

            print(f"  - {cred['username']} : {cred['password_hash'][:16]}... ({cred['hash_algo']})")

    

    def show_wireshark_instructions(self):

        """Mostra instrues para captar em Wireshark"""

        print()

        print("=" * 80)

        print("INSTRUES PARA CAPTURA EM WIRESHARK")

        print("=" * 80)

        print()

        print("1. Em Windows/Kali, abra Wireshark:")

        print("   $ wireshark")

        print()

        print("2. Selecione interface de rede (Ethernet)")

        print()

        print("3. Aplique filtro:")

        print("   tcp.port == 23")

        print()

        print("4. Inicie captura")

        print()

        print("5. Execute este script em outro terminal:")

        print(f"   python telnet_authenticated_traffic.py --target {self.target_host} --verbose")

        print()

        print("6. Em Wireshark, procure pelos pacotes TCP port 23:")

        print("   - Veja o username em plaintext")

        print("   - Veja a hash do password")

        print("   - Copie a hash para crackear com Hashcat!")

        print()

        print("=" * 80)



def main():

    parser = argparse.ArgumentParser(description="Telnet Trfego com Autenticao Capturvel")

    parser.add_argument("--target", default="192.168.100.1", help="Host alvo")

    parser.add_argument("--port", type=int, default=23, help="Porta (default: 23 Telnet)")

    parser.add_argument("--user", default="duarte", help="Username")

    parser.add_argument("--password", default="Cibersegura", help="Password")

    parser.add_argument("--hash-algo", choices=["md5", "sha256", "sha1", "plaintext"],

                       default="sha256", help="Algoritmo de hash")

    parser.add_argument("--count", type=int, default=5, help="Nmero de conexes")

    parser.add_argument("--interval", type=float, default=2.0, help="Intervalo entre conexes (seg)")

    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    parser.add_argument("--show-instructions", action="store_true", help="Mostrar instrues Wireshark")

    parser.add_argument("--wordlist", help="Usar wordlist para múltiplos passwords")

    parser.add_argument("--server", action="store_true", help="Executar como SERVIDOR (Fake Telnet)")
    
    args = parser.parse_args()
    
    if args.server:
        AuthenticatedTelnet.run_server(args.target, args.port)
        return

    

    # Mostrar instrues se pedido

    if args.show_instructions:

        telnet = AuthenticatedTelnet(args.target, args.port)

        telnet.show_wireshark_instructions()

        return

    

    # Criar cliente

    telnet = AuthenticatedTelnet(

        target_host=args.target,

        target_port=args.port,

        username=args.user,

        password=args.password,

        hash_algo=args.hash_algo,

        verbose=args.verbose

    )

    

    print("=" * 80)

    print("TELNET AUTENTICADO - GERADOR DE TRFEGO CAPTURVEL")

    print("=" * 80)

    print()

    print(f"Alvo     : {args.target}:{args.port}")

    print(f"Username : {args.user}")

    print(f"Password : {args.password}")

    print(f"Hash Algo: {args.hash_algo}")

    print()

    

    # Se wordlist fornecida, usar mltiplos passwords

    if args.wordlist:

        print(f"Usando wordlist: {args.wordlist}")

        try:

            with open(args.wordlist, 'r') as f:

                passwords = [line.strip() for line in f if line.strip()]

            

            for pwd in passwords[:args.count]:

                telnet.password = pwd

                print(f"\n Testando password: {pwd}")

                telnet.connect_and_authenticate()

                time.sleep(args.interval)

        except FileNotFoundError:

            print(f" Ficheiro no encontrado: {args.wordlist}")

            sys.exit(1)

    else:

        # Mltiplas conexes com mesmo password

        telnet.generate_multiple_connections(count=args.count, interval=args.interval)

    

    # Salvar log

    telnet.save_credentials_log("results/captured_telnet_credentials.json")

    

    print()

    print(" Trfego gerado! Verifique em Wireshark para capturar as credenciais.")



if __name__ == "__main__":

    main()

