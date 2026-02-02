#!/bin/bash
# Script para configurar isolamento de rede LAB
# Garante que VMs não têm acesso à Internet

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Configuração de Isolamento de Rede${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

# Detectar sistema
if [ -f /etc/arch-release ]; then
    SYSTEM="arch"
    echo "Sistema: Arch Linux"
elif [ -f /etc/debian_version ]; then
    SYSTEM="debian"
    echo "Sistema: Debian/Kali"
else
    echo -e "${RED}Sistema não reconhecido${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Este script irá:${NC}"
echo "  1. Remover rota default (Internet)"
echo "  2. Configurar IP estático na rede LAB"
echo "  3. Configurar regras de firewall"
echo ""

# Detectar role baseado em hostname ou perguntar
read -p "Role desta VM (orchestrator/cpu/shared): " ROLE

case $ROLE in
    orchestrator)
        LAB_IP="192.168.100.10"
        echo "Configurando como Orchestrator + GPU"
        ;;
    cpu)
        LAB_IP="192.168.100.20"
        echo "Configurando como CPU Tester"
        ;;
    shared)
        LAB_IP="192.168.100.30"
        echo "Configurando como Shared Tester"
        ;;
    *)
        echo -e "${RED}Role inválido${NC}"
        exit 1
        ;;
esac

# Detectar interface de rede principal
INTERFACE=$(ip route | grep default | awk '{print $5}' | head -n1)

if [ -z "$INTERFACE" ]; then
    # Sem rota default, listar interfaces
    INTERFACE=$(ip link | grep -v lo | grep 'state UP' | head -n1 | cut -d: -f2 | tr -d ' ')
fi

echo ""
echo "Interface detectada: $INTERFACE"
echo "IP LAB: $LAB_IP"
echo ""
read -p "Continuar? (s/N): " confirm

if [[ ! "$confirm" =~ ^[Ss]$ ]]; then
    exit 0
fi

# Verificar se é root
if [[ $EUID -ne 0 ]]; then
   echo -e "${YELLOW}Algumas operações requerem sudo${NC}"
   SUDO="sudo"
else
   SUDO=""
fi

echo -e "\n${YELLOW}[1/4] Removendo rota default...${NC}"
$SUDO ip route del default 2>/dev/null || echo "  (Nenhuma rota default)"

echo -e "${YELLOW}[2/4] Configurando IP estático...${NC}"
$SUDO ip addr flush dev "$INTERFACE"
$SUDO ip addr add "${LAB_IP}/24" dev "$INTERFACE"
$SUDO ip link set "$INTERFACE" up

echo -e "${YELLOW}[3/4] Configurando firewall...${NC}"

# Permitir tráfego LAB, bloquear resto
$SUDO iptables -F
$SUDO iptables -P INPUT DROP
$SUDO iptables -P FORWARD DROP
$SUDO iptables -P OUTPUT DROP

# Permitir loopback
$SUDO iptables -A INPUT -i lo -j ACCEPT
$SUDO iptables -A OUTPUT -o lo -j ACCEPT

# Permitir rede LAB
$SUDO iptables -A INPUT -s 192.168.100.0/24 -j ACCEPT
$SUDO iptables -A OUTPUT -d 192.168.100.0/24 -j ACCEPT

# Permitir conexões estabelecidas
$SUDO iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
$SUDO iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

echo -e "${YELLOW}[4/4] Salvando configuração...${NC}"

# Criar script de persistência
cat > /tmp/network_lab_config.sh << PERSIST_SCRIPT
#!/bin/bash
# Configuração de rede LAB - Auto-gerado

# Remover Internet
ip route del default 2>/dev/null || true

# Configurar IP LAB
ip addr flush dev $INTERFACE
ip addr add ${LAB_IP}/24 dev $INTERFACE
ip link set $INTERFACE up

# Firewall
iptables -F
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

iptables -A INPUT -s 192.168.100.0/24 -j ACCEPT
iptables -A OUTPUT -d 192.168.100.0/24 -j ACCEPT

iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

echo "Rede LAB configurada: ${LAB_IP}"
PERSIST_SCRIPT

$SUDO mv /tmp/network_lab_config.sh /usr/local/bin/
$SUDO chmod +x /usr/local/bin/network_lab_config.sh

# Criar serviço systemd (opcional)
if command -v systemctl &> /dev/null; then
    cat > /tmp/network-lab.service << SERVICE
[Unit]
Description=Hash Cracker Lab Network Configuration
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/network_lab_config.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
SERVICE

    $SUDO mv /tmp/network-lab.service /etc/systemd/system/
    $SUDO systemctl daemon-reload
    $SUDO systemctl enable network-lab.service
    
    echo "  Serviço systemd criado e habilitado"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Isolamento Configurado! ✓           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Configuração:${NC}"
echo "  IP LAB:      $LAB_IP"
echo "  Interface:   $INTERFACE"
echo "  Máscara:     255.255.255.0 (/24)"
echo ""
echo -e "${YELLOW}Verificação:${NC}"
ip addr show "$INTERFACE" | grep inet
echo ""
ip route
echo ""

echo -e "${YELLOW}Testes:${NC}"
echo "  Ping LAB:     ping 192.168.100.10"
echo "  Ping Internet (deve falhar): ping 8.8.8.8"
echo ""

echo -e "${YELLOW}Para reverter:${NC}"
echo "  sudo systemctl disable network-lab.service"
echo "  sudo systemctl restart NetworkManager"
echo ""
