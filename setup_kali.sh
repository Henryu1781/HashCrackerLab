#!/bin/bash
# Setup script para Kali Linux (CPU Tester)
# Gonçalo Ferro - VM CPU

set -e

echo "==================================="
echo "Hash Cracker Lab - Setup Kali Linux"
echo "Role: CPU Tester"
echo "==================================="

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}Este script não deve ser executado como root${NC}"
   exit 1
fi

echo -e "${YELLOW}[1/7] Atualizando sistema...${NC}"
sudo apt update && sudo apt upgrade -y

echo -e "${YELLOW}[2/7] Instalando dependências...${NC}"
sudo apt install -y \
    python3 python3-pip python3-venv \
    hashcat \
    aircrack-ng \
    wireshark tshark \
    john \
    git \
    build-essential

echo -e "${YELLOW}[3/7] Configurando ambiente Python...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${YELLOW}[4/7] Criando estrutura de diretórios...${NC}"
mkdir -p {wordlists,rules,captures,results,logs,hashes,temp}

echo -e "${YELLOW}[5/7] Configurando wordlists...${NC}"
# Kali já vem com rockyou.txt
if [ -f "/usr/share/wordlists/rockyou.txt.gz" ]; then
    gunzip -c /usr/share/wordlists/rockyou.txt.gz > wordlists/rockyou.txt
elif [ -f "/usr/share/wordlists/rockyou.txt" ]; then
    cp /usr/share/wordlists/rockyou.txt wordlists/
fi

head -n 10000 wordlists/rockyou.txt > wordlists/rockyou-small.txt 2>/dev/null || true

echo -e "${YELLOW}[6/7] Configurando regras Hashcat...${NC}"
if [ ! -d "rules" ] || [ -z "$(ls -A rules)" ]; then
    cp -r /usr/share/hashcat/rules/* rules/ 2>/dev/null || {
        git clone https://github.com/hashcat/hashcat.git temp/hashcat-repo
        cp -r temp/hashcat-repo/rules/* rules/
        rm -rf temp/hashcat-repo
    }
fi

echo -e "${YELLOW}[7/7] Configurando permissões...${NC}"
sudo usermod -a -G wireshark $USER

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Setup Concluído com Sucesso! ✓      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Próximos passos:${NC}"
echo "1. Execute: source venv/bin/activate"
echo "2. Faça logout/login para ativar grupo wireshark"
echo "3. Aguarde instruções do orquestrador"
echo ""
echo -e "${YELLOW}Verificação CPU:${NC}"
echo "hashcat -b"
echo ""
