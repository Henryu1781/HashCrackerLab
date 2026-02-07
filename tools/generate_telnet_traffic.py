#!/usr/bin/env python3
"""
Gerador simples de tráfego tipo Telnet (LAB)
- Modo servidor: escuta e grava linhas recebidas
- Modo cliente: envia sequência de login/senha simulada

Uso:
  Servidor: python tools/generate_telnet_traffic.py --server --host 0.0.0.0 --port 2323
  Cliente:  python tools/generate_telnet_traffic.py --client --host <IP_SERVIDOR> --port 2323
"""

import argparse
import socket
import threading
from datetime import datetime


def handle_client(conn, addr):
    attempts = 0
    max_attempts = 3
    
    with conn:
        print(f"Connection from {addr}")
        while attempts < max_attempts:
            try:
                conn.sendall(b"login: ")
                user_data = conn.recv(1024)
                if not user_data: break
                
                conn.sendall(b"password: ")
                pass_data = conn.recv(1024)
                if not pass_data: break
                
                user = user_data.strip().decode(errors='ignore')
                password = pass_data.strip().decode(errors='ignore')
                timestamp = datetime.now().isoformat()
                
                print(f"[{timestamp}] {addr} [Attempt {attempts+1}/{max_attempts}] -> {user} / {password}")
                
                # Simular falha para gerar mais tráfego e testar bloqueio
                attempts += 1
                if attempts >= max_attempts:
                    conn.sendall(b"\r\nAccount locked due to 3 failed attempts. Please try again in 15 minutes.\r\n")
                    print(f"[{timestamp}] {addr} -> Account Locked (15m)")
                else:
                    conn.sendall(b"\r\nLogin incorrect\r\n")
                    
            except BrokenPipeError:
                break


def run_server(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
        print(f"Servidor a ouvir em {host}:{port}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


def run_client(host: str, port: int, user: str, password: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        while True:
            data = s.recv(1024)
            if not data:
                break
            
            msg = data.decode(errors='ignore')
            # print(msg, end='') # Debug
            
            if "login:" in msg.lower():
                s.sendall((user + "\n").encode())
            elif "password:" in msg.lower():
                s.sendall((password + "\n").encode())
            elif "locked" in msg.lower():
                print(f"\n[!] Conta bloqueada detetada! Mensagem do servidor: {msg.strip()}")
                break
            elif "incorrect" in msg.lower():
                print(f"[-] Tentativa falhou com {user}:{password}")
                # O loop continua e o servidor deve enviar 'login:' novamente em seguida



def main():
    parser = argparse.ArgumentParser(description="Gerador de tráfego tipo Telnet (LAB)")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--server", action="store_true", help="Executar como servidor")
    mode.add_argument("--client", action="store_true", help="Executar como cliente")
    parser.add_argument("--host", default="127.0.0.1", help="Host para bind/connect")
    parser.add_argument("--port", type=int, default=2323, help="Porta TCP")
    parser.add_argument("--user", default="labuser", help="Utilizador (cliente)")
    parser.add_argument("--password", default="labpass", help="Password (cliente)")
    args = parser.parse_args()

    if args.server:
        run_server(args.host, args.port)
    else:
        run_client(args.host, args.port, args.user, args.password)


if __name__ == "__main__":
    main()
