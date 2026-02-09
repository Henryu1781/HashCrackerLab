#!/bin/bash
# Setup script para Arch Linux (Orquestrador + GPU)
# Henrique Carvalho - VM Principal

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

# Verificação prévia de erro comum (typo em mkinitcpio)
if [ -f /etc/mkinitcpio.conf ]; then
    if grep -q "nvida" /etc/mkinitcpio.conf 2>/dev/null; then
        echo -e "${RED}ERRO DETECTADO:${NC} Typo 'nvida' encontrado em /etc/mkinitcpio.conf"
        echo -e "${YELLOW}Tentando corrigir automaticamente para 'nvidia'...${NC}"
        sudo sed -i 's/nvida/nvidia/g' /etc/mkinitcpio.conf || echo -e "${RED}Falha na correção automática${NC}"
    fi
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
    ocl-icd \
    pocl \
    clinfo

echo -e "${YELLOW}[3/8] Verificando suporte GPU...${NC}"
# NVIDIA
if lspci | grep -i nvidia &> /dev/null; then
    echo "GPU NVIDIA detectada"
    # Removido 2>/dev/null para mostrar erros de instalação se ocorrerem
    sudo pacman -S --needed --noconfirm nvidia nvidia-utils opencl-nvidia cuda || \
        echo -e "${YELLOW}Aviso: Não foi possível instalar drivers NVIDIA. Continue manualmente se necessário.${NC}"
fi

# AMD
if lspci | grep -i amd.*vga &> /dev/null; then
    echo "GPU AMD detectada"
    sudo pacman -S --needed --noconfirm opencl-mesa 2>/dev/null || \
        echo -e "${YELLOW}Aviso: Não foi possível instalar suporte AMD GPU.${NC}"
fi

# OpenCL CPU (para benchmark CPU vs GPU no hashcat)
echo -e "${YELLOW}Verificando OpenCL CPU (POCL)...${NC}"
if clinfo 2>/dev/null | grep -q "Device Type.*CPU"; then
    echo -e "${GREEN}[OK] OpenCL CPU detectado (benchmark CPU disponível)${NC}"
else
    echo -e "${YELLOW}[WARN] OpenCL CPU não detectado. O benchmark CPU pode aparecer como n/a.${NC}"
    echo -e "${YELLOW}       Tente reiniciar sessão ou reinstalar: sudo pacman -S pocl ocl-icd${NC}"
fi

echo -e "${YELLOW}[4/8] Instalando dependências Python...${NC}"
# Usar --clear para garantir que o venv é recriado se estiver corrompido ou movido
python -m venv --clear venv || { echo "Erro ao criar venv"; exit 1; }
source venv/bin/activate || { echo "Erro ao ativar venv"; exit 1; }
pip install --upgrade pip || echo "Aviso: Erro ao atualizar pip"
pip install -r requirements.txt || { echo "Erro ao instalar dependências Python"; exit 1; }

echo -e "${YELLOW}[5/8] Criando estrutura de diretórios...${NC}"
mkdir -p {wordlists,rules,captures,results,logs,hashes,temp}

echo -e "${YELLOW}[6/8] Baixando wordlists...${NC}"
if [ ! -f "wordlists/rockyou.txt" ]; then
    wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt \
        -O wordlists/rockyou.txt 2>/dev/null || echo "Falha ao baixar rockyou, use manualmente"
fi

# Criar wordlist pequena para testes
if [ -f "wordlists/rockyou.txt" ]; then
    head -n 10000 wordlists/rockyou.txt > wordlists/rockyou-small.txt 2>/dev/null || \
        echo -e "${YELLOW}Aviso: Não foi possível criar wordlist pequena.${NC}"
else
    echo -e "${YELLOW}Aviso: rockyou.txt não encontrado. Pule este passo ou faça download manualmente.${NC}"
fi

echo -e "${YELLOW}[7/8] Baixando regras do Hashcat...${NC}"
if [ ! -d "rules" ] || [ -z "$(ls -A rules)" ]; then
    git clone https://github.com/hashcat/hashcat.git temp/hashcat-repo 2>/dev/null || { 
        echo -e "${YELLOW}Aviso: Falha ao clonar repositório hashcat. Pode continuar sem regras.${NC}"
        mkdir -p rules
        touch rules/.placeholder
    }
    if [ -d "temp/hashcat-repo/rules" ]; then
        cp -r temp/hashcat-repo/rules/* rules/ 2>/dev/null || \
            echo -e "${YELLOW}Aviso: Não foi possível copiar regras.${NC}"
        rm -rf temp/hashcat-repo
    fi
fi

echo -e "${YELLOW}[8/8] Configurando permissões...${NC}"
# Adicionar utilizador ao grupo necessário para captura de rede
if getent group wireshark > /dev/null; then
    sudo usermod -a -G wireshark $USER 2>/dev/null || \
        echo -e "${YELLOW}Aviso: Não foi possível adicionar ao grupo wireshark.${NC}"
else
    echo -e "${YELLOW}Aviso: Grupo wireshark não existe. Pode instalar manualmente.${NC}"
fi

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
