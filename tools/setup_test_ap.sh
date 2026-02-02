#!/bin/bash
# Script para configurar Access Point de teste (LAB)
# APENAS para ambiente controlado e isolado!

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configurações
SSID="LAB-SERVERS"
PASSWORD="Cibersegura"
CHANNEL=6
INTERFACE="wlan0"

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Hash Cracker Lab - Setup AP de Teste${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

# Verificar se é root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}Este script deve ser executado como root${NC}"
   exit 1
fi

# Confirmar
echo -e "${YELLOW}ATENÇÃO:${NC} Este script configura um AP de teste"
echo "SSID: $SSID"
echo "Password: $PASSWORD"
echo "Interface: $INTERFACE"
echo ""
read -p "Continuar? (s/N): " confirm
if [[ ! "$confirm" =~ ^[Ss]$ ]]; then
    exit 0
fi

echo -e "\n${YELLOW}[1/5] Instalando dependências...${NC}"
if command -v pacman &> /dev/null; then
    # Arch
    pacman -S --needed hostapd dnsmasq
elif command -v apt &> /dev/null; then
    # Debian/Kali
    apt update
    apt install -y hostapd dnsmasq
else
    echo -e "${RED}Sistema não suportado${NC}"
    exit 1
fi

echo -e "${YELLOW}[2/5] Configurando hostapd...${NC}"
cat > /etc/hostapd/hostapd_lab.conf << EOF
# Lab Test AP Configuration
interface=$INTERFACE
driver=nl80211
ssid=$SSID
hw_mode=g
channel=$CHANNEL
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=$PASSWORD
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
rsn_pairwise=CCMP
EOF

echo -e "${YELLOW}[3/5] Configurando dnsmasq...${NC}"
cat > /etc/dnsmasq_lab.conf << EOF
# Lab Test DHCP Configuration
interface=$INTERFACE
dhcp-range=192.168.50.10,192.168.50.50,255.255.255.0,12h
dhcp-option=3,192.168.50.1  # Gateway
dhcp-option=6,192.168.50.1  # DNS
server=8.8.8.8  # DNS upstream (se necessário)
log-queries
log-dhcp
bind-interfaces
EOF

echo -e "${YELLOW}[4/5] Configurando interface de rede...${NC}"
ip addr flush dev $INTERFACE
ip addr add 192.168.50.1/24 dev $INTERFACE
ip link set $INTERFACE up

echo -e "${YELLOW}[5/5] Scripts de controlo criados...${NC}"

# Script para iniciar AP
cat > /usr/local/bin/start_lab_ap.sh << 'SCRIPT_START'
#!/bin/bash
INTERFACE="wlan0"

echo "Iniciando Lab Test AP..."

# Parar serviços conflituantes
systemctl stop NetworkManager 2>/dev/null || true
systemctl stop wpa_supplicant 2>/dev/null || true

# Configurar interface
ip addr flush dev $INTERFACE
ip addr add 192.168.50.1/24 dev $INTERFACE
ip link set $INTERFACE up

# Iniciar dnsmasq
dnsmasq -C /etc/dnsmasq_lab.conf -d &
DNSMASQ_PID=$!

# Iniciar hostapd
hostapd /etc/hostapd/hostapd_lab.conf &
HOSTAPD_PID=$!

echo "AP Iniciado!"
echo "SSID: LAB-SERVERS"
echo "Password: Cibersegura"
echo ""
echo "Pressione Ctrl+C para parar"

# Aguardar
trap "kill $DNSMASQ_PID $HOSTAPD_PID 2>/dev/null" EXIT
wait
SCRIPT_START

chmod +x /usr/local/bin/start_lab_ap.sh

# Script para parar AP
cat > /usr/local/bin/stop_lab_ap.sh << 'SCRIPT_STOP'
#!/bin/bash

echo "Parando Lab Test AP..."

killall hostapd 2>/dev/null || true
killall dnsmasq 2>/dev/null || true

# Reiniciar NetworkManager
systemctl start NetworkManager 2>/dev/null || true

echo "AP parado"
SCRIPT_STOP

chmod +x /usr/local/bin/stop_lab_ap.sh

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Setup AP Concluído! ✓               ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Comandos:${NC}"
echo "  Iniciar AP:  sudo start_lab_ap.sh"
echo "  Parar AP:    sudo stop_lab_ap.sh"
echo ""
echo -e "${YELLOW}Configuração:${NC}"
echo "  SSID:     $SSID"
echo "  Password: $PASSWORD"
echo "  Canal:    $CHANNEL"
echo "  Range IP: 192.168.50.10-50"
echo ""
