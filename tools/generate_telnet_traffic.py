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
    with conn:
        conn.sendall(b"login: ")
        data = conn.recv(1024)
        conn.sendall(b"password: ")
        data2 = conn.recv(1024)
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] {addr} -> {data.strip().decode(errors='ignore')} / {data2.strip().decode(errors='ignore')}")


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
        s.recv(1024)
        s.sendall((user + "\n").encode())
        s.recv(1024)
        s.sendall((password + "\n").encode())
        print("Credenciais enviadas")


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
