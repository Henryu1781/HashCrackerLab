#!/bin/bash
# Setup script para Arch Linux (Orquestrador + GPU)
# Henrique Carvalho - VM Principal

set -e

echo "==================================="
echo "Hash Cracker Lab - Setup Arch Linux"
echo "Role: Orchestrator + GPU Tester"
echo "==================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se é root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}Este script não deve ser executado como root${NC}"
   echo "Execute como utilizador normal (vai pedir sudo quando necessário)"
   exit 1
fi

echo -e "${YELLOW}[1/8] Atualizando sistema...${NC}"
sudo pacman -Syu --noconfirm

echo -e "${YELLOW}[2/8] Instalando dependências do sistema...${NC}"
sudo pacman -S --needed --noconfirm \
    python python-pip \
    hashcat \
    aircrack-ng \
    wireshark-cli \
    tcpdump \
    john \
    git \
    base-devel \
    opencl-headers \
    ocl-icd

echo -e "${YELLOW}[3/8] Verificando suporte GPU...${NC}"
# NVIDIA
if lspci | grep -i nvidia &> /dev/null; then
    echo "GPU NVIDIA detectada"
    sudo pacman -S --needed --noconfirm nvidia nvidia-utils opencl-nvidia
fi

# AMD
if lspci | grep -i amd.*vga &> /dev/null; then
    echo "GPU AMD detectada"
    sudo pacman -S --needed --noconfirm opencl-mesa
fi

echo -e "${YELLOW}[4/8] Instalando dependências Python...${NC}"
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${YELLOW}[5/8] Criando estrutura de diretórios...${NC}"
mkdir -p {wordlists,rules,captures,results,logs,hashes,temp}

echo -e "${YELLOW}[6/8] Baixando wordlists...${NC}"
if [ ! -f "wordlists/rockyou.txt" ]; then
    wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt \
        -O wordlists/rockyou.txt 2>/dev/null || echo "Falha ao baixar rockyou, use manualmente"
fi

# Criar wordlist pequena para testes
head -n 10000 wordlists/rockyou.txt > wordlists/rockyou-small.txt 2>/dev/null || true

echo -e "${YELLOW}[7/8] Baixando regras do Hashcat...${NC}"
if [ ! -d "rules" ] || [ -z "$(ls -A rules)" ]; then
    git clone https://github.com/hashcat/hashcat.git temp/hashcat-repo
    cp -r temp/hashcat-repo/rules/* rules/
    rm -rf temp/hashcat-repo
fi

echo -e "${YELLOW}[8/8] Configurando permissões...${NC}"
# Adicionar utilizador ao grupo necessário para captura de rede
sudo usermod -a -G wireshark $USER

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Setup Concluído com Sucesso! ✓      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Próximos passos:${NC}"
echo "1. Execute: source venv/bin/activate"
echo "2. Faça logout/login para ativar grupo wireshark"
echo "3. Teste: python orchestrator.py --config config/experiment_example.yaml"
echo ""
echo -e "${YELLOW}Verificação GPU:${NC}"
echo "hashcat -I"
echo ""
