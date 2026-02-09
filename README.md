# 🔐 Hash Cracker Lab - Projeto Final de Cibersegurança

> **Demonstração prática de técnicas de cracking de passwords utilizando GPU, múltiplos algoritmos de hash e ataques coordenados.**

## 👥 Equipa

| Membro | Sistema | Função |
|--------|---------|--------|
| **Henrique** | Arch Linux | Orquestração & GPU Cracking |
| **Ferro** | Kali Linux | WiFi Penetration Testing |
| **Duarte** | Windows | Geração de Tráfego Telnet |
| **Francisco** | Windows | Servidor & Análise Wireshark |

---

## 📋 Pré-requisitos

### Hardware Requerido
- **Henrique**: GPU compatível (NVIDIA/AMD) para hashcat
- **Ferro**: Adaptador WiFi com modo monitor
- **Todos**: Mínimo 4GB RAM, 10GB espaço em disco

### Software Necessário

#### Linux (Arch/Kali)
```bash
# Hashcat, Aircrack-ng, Python 3.10+
sudo pacman -S hashcat aircrack-ng python  # Arch
sudo apt install hashcat aircrack-ng python3  # Kali
```

#### Windows
- Python 3.10+
- Wireshark
- Hashcat (opcional para benchmark local)

---

## 🚀 Instalação Rápida

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-repo/HashCrackerLab.git
cd HashCrackerLab
```

### 2. Setup Automático por Sistema Operativo

#### **Arch Linux (Henrique)**
```bash
bash setup_arch.sh
source venv/bin/activate
python tools/validate_environment.py
```

#### **Kali Linux (Ferro)**
```bash
bash setup_kali.sh
source venv/bin/activate
python tools/validate_environment.py
```

#### **Windows (Duarte/Francisco)**
```powershell
.\setup_windows.ps1
.\venv\Scripts\Activate.ps1
python tools\validate_environment.py
```

---

## 🎯 Como Executar a Demonstração

### Opção 1: Demonstração Completa (Recomendado)

Esta é a forma **mais simples** de executar todo o lab com demonstrações visuais.

#### **Henrique (Coordenador)**
```bash
# Ativar ambiente
source venv/bin/activate

# Executar orquestrador com config de demonstração
python orchestrator.py --config config/advanced_encryption_test.yaml
```

**O que acontece:**
1. ✅ Gera 20 hashes (Bcrypt, Argon2, MD5, SHA-256)
2. ✅ Executa cracking com dicionário
3. ✅ Mostra benchmark CPU vs GPU
4. ✅ Demonstração visual de força bruta
5. ✅ Gera relatório completo em \`results/\`

**Saída esperada:**
```
Total de hashes: 20
Hashes crackeadas: 16
Taxa de sucesso: 80.00%

Benchmark GPU vs CPU:
- MD5: GPU é 16.5x mais rápido
- SHA-256: GPU é 9.9x mais rápido  
- Bcrypt: GPU é 5.2x mais rápido
```

---

### Opção 2: Teste Rápido (5 minutos)

Para validação rápida do sistema:

```bash
python orchestrator.py --config config/quick_test.yaml
```

---

### Opção 3: Demonstração Avançada com WiFi e Telnet

**Requer coordenação de toda a equipa.**

#### **Passo 1: Francisco - Servidor Telnet**
```powershell
# Ativar ambiente
.\venv\Scripts\Activate.ps1

# Iniciar servidor fake Telnet
python telnet_authenticated_traffic.py --server --port 23

# Deixar a correr e anotar o IP (ex: 192.168.100.50)
```

#### **Passo 2: Duarte - Cliente Telnet**
```powershell
# Substituir IP_DO_FRANCISCO pelo IP real
python telnet_authenticated_traffic.py --target 192.168.100.50 --user duarte --password Cibersegura
```

**Francisco**: Capturar tráfego com Wireshark (filtro: \`tcp.port == 23\`)

#### **Passo 3: Ferro - WiFi Cracking**
```bash
# Modo monitor
sudo airmon-ng start wlan0

# Ataque à rede WiFi (simulado)
python wifi_cracker.py --network "LAB-SERVERS" --monitor wlan0mon
```

#### **Passo 4: Henrique - Orquestração Final**
```bash
# Executar configuração completa
python orchestrator.py --config config/projeto_final_ciberseguranca.yaml
```

---

## 📊 Resultados e Relatórios

Após execução, os resultados ficam em:
```
results/
└── [nome_experimento]_[timestamp]/
    ├── REPORT.md              # Relatório resumido
    ├── hashes/
    │   ├── generated_hashes.json
    │   └── hashes_safe.json   # Versão anonimizada
    ├── cracked/
    │   ├── bcrypt/cracked_*.pot
    │   ├── argon2/cracked_*.pot
    │   ├── md5/cracked_*.pot
    │   └── sha256/cracked_*.pot
    ├── metrics/
    │   ├── metrics.json
    │   ├── metrics_by_algorithm.csv
    │   └── benchmark_cpu_gpu.csv
    └── logs/
        └── orchestrator.log
```

**Ver relatório:**
```bash
cat results/[pasta_mais_recente]/REPORT.md
```

---

## 🔧 Configurações Disponíveis

| Ficheiro | Descrição | Uso |
|----------|-----------|-----|
| \`quick_test.yaml\` | Teste rápido (10 hashes) | Validação |
| \`advanced_encryption_test.yaml\` | Bcrypt + Argon2 + MD5 + SHA256 | **Recomendado para demo** |
| \`projeto_final_ciberseguranca.yaml\` | Demo completa com WiFi/Telnet | Apresentação avançada |
| \`full_test.yaml\` | Teste exaustivo (todos algoritmos) | Benchmarking |

---

## 📚 Documentação Adicional

- 📖 **[GUIA_DA_APRESENTACAO.md](GUIA_DA_APRESENTACAO.md)** - Guião passo-a-passo para apresentação
- 🔬 **[FULL_INTEGRATION_GUIDE.md](FULL_INTEGRATION_GUIDE.md)** - Guia técnico detalhado
- 🌐 **[docs/NETWORK_SETUP.md](docs/NETWORK_SETUP.md)** - Configuração de rede
- ❓ **[PERGUNTAS_E_RESPOSTAS.md](PERGUNTAS_E_RESPOSTAS.md)** - FAQ

---

## 🛠️ Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'yaml'"
**Solução:**
```bash
# Verificar se venv está ativo
which python  # Deve mostrar caminho do venv

# Reinstalar dependências
pip install -r requirements.txt
```

### Problema: "Hashcat not found"
**Solução:**
```bash
# Verificar instalação
hashcat --version

# Instalar se necessário
sudo pacman -S hashcat  # Arch
sudo apt install hashcat  # Kali
```

### Problema: "Rede não está isolada"
**Solução:**
```bash
# Desativar verificação (apenas para testes)
# Editar config/*.yaml:
security:
  isolated_network: false
```

### Problema: GPU não detectada
**Solução:**
```bash
# Verificar dispositivos OpenCL/CUDA
hashcat -I

# Se vazio, reinstalar drivers GPU
```

---

## 🎓 Objetivos de Aprendizagem

Após completar este lab, demonstra-se:

✅ **Conhecimento de Algoritmos de Hash**
- Diferença entre MD5, SHA-256, Bcrypt, Argon2
- Porque algoritmos modernos são mais seguros

✅ **Técnicas de Cracking**
- Dictionary attacks
- Brute-force com máscaras
- Rule-based mutations
- Hybrid attacks

✅ **Aceleração por GPU**
- Compreender speedup GPU vs CPU
- Limitações de algoritmos memory-hard

✅ **Análise de Tráfego**
- Captura de credenciais em texto plano (Telnet)
- Importância de protocolos encriptados (SSH)

✅ **Segurança WiFi**
- Vulnerabilidades WPA2
- Ataques de deauth + handshake capture

---

## 📞 Suporte

**Problemas técnicos durante demo:**
- Consultar logs: \`cat results/[experimento]/logs/orchestrator.log\`
- Executar validação: \`python tools/validate_environment.py\`

**Contactos:**
- Henrique: [email]
- Repositório: [GitHub URL]

---

## 📜 Licença

Este projeto é apenas para fins educacionais. **Não utilize estas técnicas em sistemas sem autorização explícita.**

MIT License - Ver [LICENSE](LICENSE)

---

*HashCrackerLab v2.0 - Fevereiro 2026*
