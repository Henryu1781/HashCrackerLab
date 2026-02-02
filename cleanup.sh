#!/bin/bash
# Script de limpeza completa
# Remove dados sensíveis e restaura ambiente

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}================================${NC}"
echo -e "${YELLOW}Hash Cracker Lab - Limpeza${NC}"
echo -e "${YELLOW}================================${NC}"
echo ""

# Confirmar
read -p "Remover TODOS os resultados e dados sensíveis? (s/N): " confirm
if [[ ! "$confirm" =~ ^[Ss]$ ]]; then
    echo "Cancelado."
    exit 0
fi

echo -e "\n${YELLOW}[1/5] Removendo resultados...${NC}"
rm -rf results/*
echo "✓ Resultados removidos"

echo -e "${YELLOW}[2/5] Limpando hashes...${NC}"
rm -rf hashes/*
echo "✓ Hashes removidos"

echo -e "${YELLOW}[3/5] Limpando capturas...${NC}"
rm -rf captures/*
echo "✓ Capturas removidas"

echo -e "${YELLOW}[4/5] Limpando logs...${NC}"
rm -rf logs/*
echo "✓ Logs removidos"

echo -e "${YELLOW}[5/5] Limpando temporários...${NC}"
rm -rf temp/*
rm -rf src/__pycache__
rm -rf __pycache__
find . -name "*.pyc" -delete
find . -name "*.pot" -delete
find . -name "*.log" -delete
echo "✓ Temporários removidos"

# Criar ficheiro de auditoria
AUDIT_FILE="CLEANUP_$(date +%Y%m%d_%H%M%S).txt"
cat > "$AUDIT_FILE" << EOF
Hash Cracker Lab - Relatório de Limpeza
========================================

Data: $(date)
Utilizador: $(whoami)
Hostname: $(hostname)

Ações Realizadas:
- Resultados removidos: results/*
- Hashes removidos: hashes/*
- Capturas removidas: captures/*
- Logs removidos: logs/*
- Temporários removidos: temp/*, __pycache__, *.pyc, *.pot, *.log

Checksum deste relatório:
$(sha256sum "$AUDIT_FILE" | cut -d' ' -f1)
EOF

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Limpeza Concluída! ✓                ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "Relatório de auditoria: ${YELLOW}$AUDIT_FILE${NC}"
echo ""
