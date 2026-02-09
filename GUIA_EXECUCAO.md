# 📘 GUIA DE EXECUÇÃO TÉCNICA

**Setup + Testes + Troubleshooting**

---

## ⚡ EXECUÇÃO RÁPIDA (5 minutos)

### Henrique - Demo GPU Completa
```bash
cd ~/Projects/HashCrackerLab
source venv/bin/activate
python orchestrator.py --config config/advanced_encryption_test.yaml
```

**Timeline:**
- Validação: 5s
- Geração 20 hashes: 10s
- Cracking GPU: 30s
- Brute-force demo: 5s
- Benchmark: 15s
- **Total: ~1min 20s**

**Resultado esperado:**
```
Total: 20 hashes
Crackeadas: 16 (80%)
GPU Speedup: 16.5x (MD5)
```

### Ferro - WiFi Cracking
```bash
# 1. Capturar handshake (~2-3 min)
python wifi_cracker.py --capture --ssid LAB-SERVERS --interface wlan0mon

# 2. Crack (~30 segundos)
python wifi_cracker.py --crack --hash hashes/wifi_sample.hc22000
```

### Francisco + Duarte - Telnet Demo
```powershell
# Francisco (servidor):
python telnet_authenticated_traffic.py --server --port 23

# Duarte (cliente):
telnet 192.168.100.30 23
# Username: admin
# Password: SecurePass123
```

**Wireshark (Francisco):** Filtro `tcp.port == 23` → Ver credenciais em claro

---

## 🔧 SETUP DETALHADO

### 1. Setup Inicial (Dia Anterior - 10 min)

#### Henrique (Arch Linux)
```bash
cd ~/Projects/HashCrackerLab
./setup_arch.sh
source venv/bin/activate

# Validar
python tools/validate_environment.py
hashcat -I  # Ver GPU
```

**Saída esperada:**
```
✓ Python 3.14.2
✓ Hashcat v7.1.2
✓ GPU: NVIDIA (OpenCL)
✓ Dependencies OK
```

#### Ferro (Kali Linux)
```bash
cd ~/Projects/HashCrackerLab
./setup_kali.sh
source venv/bin/activate

# Testar modo monitor
sudo airmon-ng start wlan0
iwconfig | grep mon  # Deve ver wlan0mon
```

#### Francisco + Duarte (Windows)
```powershell
cd C:\Users\[USER]\HashCrackerLab
.\setup_windows.ps1
.\venv\Scripts\Activate.ps1

# Validar Wireshark
wireshark --version
```

### 2. Setup de Rede (10 min antes - Opcional)

**Router WiFi:**
```
SSID: LAB-SERVERS
Password: Cibersegura
Encryption: WPA2-PSK
```

**IPs Fixos (opcional):**
```bash
# Linux (nmtui ou nmcli)
nmtui  # Interface gráfica

# Windows (PowerShell como Admin)
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 192.168.100.30 `
  -PrefixLength 24 -DefaultGateway 192.168.100.1
```

**Teste de conectividade:**
```bash
ping 192.168.100.1  # Gateway
ping 192.168.100.10  # Henrique
ping 192.168.100.20  # Ferro
```

---

## 🧪 TESTES DE VALIDAÇÃO

### Teste 1: GPU Funcional (Henrique)
```bash
hashcat -b  # Benchmark completo (~2 min)
# Deve ver MD5: ~20+ GH/s
```

### Teste 2: WiFi Monitor Mode (Ferro)
```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
airodump-ng wlan0mon  # Deve ver redes WiFi
# Ctrl+C para sair
```

### Teste 3: Wireshark (Francisco)
```powershell
# Abrir Wireshark
# Interface: WiFi ou Ethernet
# Start Capture → deve ver pacotes
```

### Teste 4: Python Environment (Todos)
```bash
python -c "import yaml, passlib, argon2; print('OK')"
```

---

## 📊 CONFIGURAÇÕES DISPONÍVEIS

### config/advanced_encryption_test.yaml
**Uso:** Demo completa com 4 algoritmos  
**Hashes:** 20 (5 de cada)  
**Tempo:** ~1 minuto  
```bash
python orchestrator.py --config config/advanced_encryption_test.yaml
```

### config/quick_test.yaml
**Uso:** Teste rápido  
**Hashes:** 20  
**Tempo:** ~30 segundos  
```bash
python orchestrator.py --config config/quick_test.yaml
```

### config/projeto_final_ciberseguranca.yaml
**Uso:** Configuração original do projeto  
**Hashes:** Variável  
```bash
python orchestrator.py --config config/projeto_final_ciberseguranca.yaml
```

---

## 🆘 TROUBLESHOOTING

### GPU Não Detectada
```bash
# Verificar
hashcat -I

# Se não aparecer:
sudo pacman -S opencl-nvidia  # Arch
sudo apt install nvidia-opencl-icd  # Kali/Ubuntu

# Reboot pode ser necessário
```

### WiFi Não Entra em Modo Monitor
```bash
# Matar processos interferentes
sudo airmon-ng check kill

# Tentar novamente
sudo airmon-ng start wlan0

# Alternativa: usar outra interface
ip link show  # Listar interfaces
sudo airmon-ng start wlan1  # Se existir
```

### Wireshark Sem Permissões (Linux)
```bash
# Adicionar user ao grupo wireshark
sudo usermod -aG wireshark $USER
# Logout e login novamente

# Alternativa: usar como root (não recomendado)
sudo wireshark
```

### Import Errors
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt

# Se persistir:
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Hashcat "No devices found"
```bash
# Verificar drivers
nvidia-smi  # NVIDIA
clinfo  # OpenCL geral

# Se GPU NVIDIA não aparece:
# Reinstalar drivers NVIDIA + OpenCL
```

### Network Unreachable
```bash
# Verificar gateway
ip route show

# Adicionar rota se necessário
sudo ip route add default via 192.168.100.1

# Verificar DNS
ping 8.8.8.8  # Google DNS
```

---

## 📂 ESTRUTURA DE RESULTADOS

Após execução, resultados em `results/`:
```
results/
└── advanced_crypto_test_20260209_115842/
    ├── REPORT.md              # Resumo completo
    ├── execution_details.json  # Métricas técnicas
    ├── cracked/
    │   ├── bcrypt/
    │   │   └── cracked_bcrypt_dictionary.pot
    │   ├── argon2/
    │   ├── md5/
    │   └── sha256/
    └── logs/
        └── orchestrator.log
```

**Ver resultados:**
```bash
# Listar execuções
ls -lht results/ | head

# Ver último relatório
LAST=$(ls -td results/*/ | head -1)
cat "$LAST/REPORT.md"

# Ver passwords crackeadas (MD5)
cat "$LAST/cracked/md5/cracked_md5_dictionary.pot"
```

---

## 🔍 ANÁLISE DE OUTPUTS

### Interpretar Taxa de Sucesso
```
Total: 20 hashes
Crackeadas: 16 (80%)
```

**80% é normal porque:**
- Algumas passwords (`admin`, `teste`) não estão na wordlist
- Em produção: wordlists com milhões de entradas → taxa ~95%+

### Interpretar Benchmark
```
MD5: GPU 22.5 GH/s vs CPU 1.4 GH/s → 16.5x speedup
```

**Significado:**
- GPU testa 22.5 **bilhões** de hashes MD5 por segundo
- CPU testa apenas 1.4 bilhões
- GPU é 16.5 vezes mais rápida

### Interpretar Tempo de Cracking
```
[!] Password encontrada: password (MD5) - Tempo: 0.02s
```

**Por quê tão rápido?**
- `password` está no topo da wordlist
- MD5 é extremamente rápido na GPU
- Se não estivesse na wordlist: nunca seria encontrada

---

## 📈 MÉTRICAS DE SUCESSO

**Demo considerada bem-sucedida se:**
- ✅ GPU detectada e funcional
- ✅ Pelo menos 70% dos hashes crackeados
- ✅ Benchmark mostra speedup GPU > 5x
- ✅ WiFi handshake capturado (se aplicável)
- ✅ Wireshark mostra tráfego Telnet (se aplicável)

---

## 🚀 COMANDOS ÚTEIS

### Limpar Resultados Antigos
```bash
rm -rf results/*
rm -rf logs/*
```

### Ver Logs em Tempo Real
```bash
tail -f logs/orchestrator.log
```

### Listar Hashes Gerados
```bash
ls -lh hashes/
```

### Benchmark Rápido Hashcat
```bash
hashcat -b -m 0  # MD5
hashcat -b -m 1400  # SHA-256
hashcat -b -m 3200  # Bcrypt
```

---

**Status:** ✅ Guia Técnico Completo | **Última atualização:** 2026-02-09
