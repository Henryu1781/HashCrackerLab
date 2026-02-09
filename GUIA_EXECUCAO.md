# 🎭 GUIA COMPLETO - Apresentação e Execução (30 minutos)

**Demonstração Profissional de Segurança Ofensiva**

---

## ⏱️ CRONOGRAMA DA APRESENTAÇÃO (30 minutos)

| Tempo | Fase | Quem | O Quê |
|-------|------|------|-------|
| **0:00-3:00** | Introdução | Henrique | Apresentação + objetivos |
| **3:00-10:00** | WiFi WPA2 | Ferro | Captura handshake + crack |
| **10:00-17:00** | Telnet Demo | Francisco/Duarte | Servidor + Wireshark |
| **17:00-27:00** | GPU Cracking | Henrique | 4 algoritmos + benchmark |
| **27:00-30:00** | Conclusões | Henrique | Resumo + Q&A |

---

## ⚡ EXECUÇÃO RÁPIDA (5 minutos de setup)

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

## 🎬 APRESENTAÇÃO DETALHADA (30 minutos)

### FASE 1: INTRODUÇÃO (0:00-3:00)

**Henrique (narrador):**

> "Bom dia. Somos especialistas em cibersegurança e hoje vamos demonstrar **3 vulnerabilidades críticas**:
> 
> 1. **WiFi WPA2** pode ser crackeado offline
> 2. **Tráfego não-encriptado** expõe credenciais
> 3. **GPUs modernas** quebram encriptação em segundos
> 
> Vejam como."

**Ação:** Mostrar slides (30s) + apresentar equipa (30s) + setup projector (1min)

---

### FASE 2: WiFi WPA2 CRACKING (3:00-10:00)

**Duração: 7 minutos**

#### Passo 1: Captura (3:00-6:00)

**Ferro executa:**
```bash
cd ~/Projects/HashCrackerLab
source venv/bin/activate
python wifi_cracker.py --capture --ssid LAB-SERVERS --interface wlan0mon
```

**Output esperado:**
```
[*] Modo monitor: wlan0mon
[*] Escutando rede: LAB-SERVERS (Canal 6)
[*] Aguardando handshake WPA2...
[!] HANDSHAKE CAPTURADO! → hashes/wifi_sample.hc22000
```

**Henrique narra (enquanto captura):**
> "O Ferro está em modo promíscuo, capturando tráfego WiFi. Quando alguém se conecta à rede 'LAB-SERVERS', capturamos o handshake WPA2. Este handshake contém informação suficiente para ataque offline."

**⏱️ Tempo: ~2-3 minutos**

#### Passo 2: Cracking (6:00-10:00)

**Ferro executa:**
```bash
python wifi_cracker.py --crack --hash hashes/wifi_sample.hc22000
```

**Output esperado:**
```
[*] Cracking WPA2 com hashcat mode 22000...
[*] Wordlist: wordlists/rockyou.txt
[+] PASSWORD ENCONTRADA: Cibersegura
[+] Tempo: 3.2 segundos
```

**Henrique narra:**
> "Em **3 segundos**, encontramos a password. A GPU testou milhões de combinações. Se a password fosse forte (16+ caracteres aleatórios), demoraria anos."

**⏱️ Tempo: ~30 segundos de cracking + 3 min explicação**

---

### FASE 3: TELNET CREDENTIAL CAPTURE (10:00-17:00)

**Duração: 7 minutos**

#### Passo 1: Servidor (10:00-11:00)

**Francisco executa:**
```powershell
cd C:\Users\Francisco\HashCrackerLab
.\venv\Scripts\Activate.ps1
python telnet_authenticated_traffic.py --server --port 23
```

**Output:**
```
[SERVER] Telnet listening on 0.0.0.0:23
[SERVER] Waiting for connections...
```

**Francisco abre Wireshark:**
```
Filtro: tcp.port == 23
Start Capture
```

#### Passo 2: Cliente Conecta (11:00-13:00)

**Duarte executa:**
```powershell
telnet 192.168.100.30 23
```

**No Telnet prompt:**
```
Username: admin
Password: SecurePass123
```

**⏱️ Tempo: ~1 minuto**

#### Passo 3: Análise Wireshark (13:00-17:00)

**Francisco mostra no Wireshark (projetado):**
```
Packet #42: Telnet Data
    Data: "admin"
Packet #43: Telnet Data
    Data: "SecurePass123"
```

**Henrique narra:**
> "Vejam! A password 'SecurePass123' aparece em **texto claro**. Qualquer pessoa nesta rede consegue ver. Por isso usamos **SSH** em produção, nunca Telnet."

**⏱️ Tempo: ~4 minutos (demo + explicação)**

---

### FASE 4: GPU CRACKING (17:00-27:00)

**Duração: 10 minutos**

#### Passo 1: Execução (17:00-19:00)

**Henrique executa:**
```bash
cd ~/Projects/HashCrackerLab
source venv/bin/activate
python orchestrator.py --config config/advanced_encryption_test.yaml
```

**Henrique narra (durante execução):**
> "Vou gerar 20 hashes com **4 algoritmos diferentes**:
> - MD5 (legacy, rápido)
> - SHA-256 (moderno, comum)
> - Bcrypt (resistente, com 'cost factor')
> - Argon2 (memory-hard, mais recente)
> 
> A GPU vai tentar cracka-los todos."

#### Passo 2: Acompanhar Output (19:00-22:00)

**Output em tempo real:**
```
[*] Validando configuração... ✓
[*] Gerando 20 hashes...
  - Bcrypt (cost 5): 5 hashes
  - Argon2: 5 hashes
  - MD5: 5 hashes
  - SHA-256: 5 hashes
[✓] 20 hashes gerados em 3.1s

[*] Iniciando cracking com GPU...
[GPU] MD5: 22.5 GH/s ⚡⚡⚡
[GPU] SHA-256: 8.2 GH/s ⚡⚡
[GPU] Bcrypt: 2.1 MH/s ⚡
[GPU] Argon2: Testing...

[!] Password encontrada: password (MD5)
[!] Password encontrada: 123456 (Bcrypt)
[!] Password encontrada: qwerty (SHA-256)
...

[✓] Cracking concluído! 16 de 20 crackeadas (80%)
```

**Henrique explica (durante execução):**
> "Vejam a velocidade da GPU:
> - **MD5:** 22 **bilhões** de hashes por segundo!
> - **Bcrypt:** Mais resistente, apenas 2 milhões/s
> - **Argon2:** Memory-hard, ainda mais lento
> 
> A GPU é **16 vezes mais rápida** que CPU para MD5!"

#### Passo 3: Benchmark + Demo Brute-Force (22:00-27:00)

**Output continua:**
```
[*] Simulando brute-force de PIN (0000-9999)...
Testando: 0000, 0001, 0002, ..., 5239
[+] PIN encontrado: 5239 (2.1 segundos, 2450 tentativas)

[*] Benchmark GPU vs CPU:
┌──────────┬──────────┬──────────┬─────────┐
│ Algoritmo│ GPU/sec  │ CPU/sec  │ Speedup │
├──────────┼──────────┼──────────┼─────────┤
│ MD5      │ 22.5GH/s │ 1.4GH/s  │ 16.5x ⚡ │
│ SHA-256  │ 8.2GH/s  │ 0.8GH/s  │  9.9x ⚡ │
│ Bcrypt   │ 2.1MH/s  │ 0.4MH/s  │  5.2x ⚡ │
└──────────┴──────────┴──────────┴─────────┘

[✓] Resultados salvos em: results/advanced_crypto_test_*/
```

**Henrique narra:**
> "A demo de força bruta mostra **tentativa e erro**. Para um PIN de 4 dígitos (10.000 combinações), a GPU leva 2 segundos.
> 
> Para uma password de 8 caracteres alfanuméricos (62^8 = 218 **trilhões**), mesmo a GPU demoraria anos. Por isso **senhas fortes são críticas**."

**⏱️ Tempo: ~8 minutos (execução + narração + benchmark)**

---

### FASE 5: CONCLUSÕES (27:00-30:00)

**Duração: 3 minutos**

**Henrique:**

> "**Resumo das vulnerabilidades demonstradas:**
> 
> 1. **WiFi WPA2:** Handshake capturável → attack offline → 3 segundos com GPU
>    - **Proteção:** Senhas fortes (16+ chars aleatórios)
> 
> 2. **Telnet:** Credenciais em texto claro → visível para todos na rede
>    - **Proteção:** Usar SSH, HTTPS, VPNs
> 
> 3. **Hashes fracos:** MD5 cai em segundos → 22 bilhões de tentativas/segundo
>    - **Proteção:** Algoritmos modernos (Argon2, Bcrypt) + senhas fortes
> 
> **A lição final:** 
> Criptografia moderna é **robusta**, mas **inútil sem senhas fortes**. 
> Uma senha de 6 caracteres é pior que nenhuma encriptação.
> 
> Perguntas?"

**⏱️ Tempo: 2 min resumo + 1 min Q&A**

---

## 🔧 SETUP DETALHADO

### 1. Setup Inicial (Dia Anterior - 10 min)

#### ✅ PRÉ-REQUISITOS

**Henrique (Arch Linux):**
```bash
cd ~/Projects/HashCrackerLab
./setup_arch.sh
source venv/bin/activate
python tools/validate_environment.py  # Tudo ✓
hashcat -I  # GPU detectada
```

**Ferro (Kali Linux):**
```bash
cd ~/Projects/HashCrackerLab
./setup_kali.sh
sudo airmon-ng start wlan0  # Interface wlan0mon criada
```

**Francisco + Duarte (Windows):**
```powershell
cd C:\Users\[USER]\HashCrackerLab
.\setup_windows.ps1
wireshark --version  # Funciona
```

### 2. Setup de Rede (10 min antes da apresentação)

**Router WiFi:**
```
SSID:     LAB-SERVERS
Password: Cibersegura
Tipo:     WPA2-PSK
Gateway:  192.168.100.1 (opcional)
```

**IPs (se necessário):**

| Máquina | IP |
|---------|-----|
| Henrique | 192.168.100.10 |
| Ferro | 192.168.100.20 |
| Francisco | 192.168.100.30 |
| Duarte | 192.168.100.40 |

**Configurar IPs:**
```bash
# Linux (nmtui)
nmtui  # Interface gráfica

# Windows (PowerShell como Admin)
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 192.168.100.30 `
  -PrefixLength 24 -DefaultGateway 192.168.100.1
```

**Teste:** `ping 192.168.100.1` em todas as máquinas

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
