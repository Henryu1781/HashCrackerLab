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

## ⚡ COMANDOS RÁPIDOS (Referência)

**Henrique - GPU Demo:**
```bash
cd ~/Projects/HashCrackerLab && source venv/bin/activate
python orchestrator.py --config config/advanced_encryption_test.yaml
```

**Ferro - WiFi:**
```bash
python wifi_cracker.py --capture --ssid LAB-SERVERS --interface wlan0mon
python wifi_cracker.py --crack --hash hashes/wifi_sample.hc22000
```

**Francisco - Telnet Server:**
```powershell
python telnet_authenticated_traffic.py --server --port 23
```

**Duarte - Telnet Client:**
```powershell
telnet 192.168.100.30 23
```

---

## 🎬 APRESENTAÇÃO DETALHADA (30 minutos)

### FASE 1: INTRODUÇÃO (0:00-3:00)

**👤 Henrique fala:**

> "Bom dia. Somos especialistas em cibersegurança e hoje vamos demonstrar **3 vulnerabilidades críticas**:
> 
> 1. **WiFi WPA2** pode ser crackeado offline
> 2. **Tráfego não-encriptado** expõe credenciais
> 3. **GPUs modernas** quebram encriptação em segundos
> 
> Vejam como."

**📋 Ações paralelas:**
- Mostrar slides (30s)
- Apresentar equipa (30s)
- Setup projector (1min)
- Todos: Abrir terminais e preparar comandos

---

### FASE 2: WiFi WPA2 CRACKING (3:00-10:00)

**⏱️ Duração: 7 minutos**

---

#### ⏰ 3:00 - Início da Captura

**💻 Ferro executa (terminal visível no projector):**
```bash
cd ~/Projects/HashCrackerLab
source venv/bin/activate
python wifi_cracker.py --capture --ssid LAB-SERVERS --interface wlan0mon
```

**📺 Output esperado:**
```
[*] Modo monitor: wlan0mon
[*] Escutando rede: LAB-SERVERS (Canal 6)
[*] Aguardando handshake WPA2...
```

**👤 Henrique narra (enquanto Ferro executa):**
> "O Ferro está em modo promíscuo, capturando todo o tráfego WiFi. Quando alguém se conecta à rede 'LAB-SERVERS', capturamos o handshake WPA2. Este handshake contém informação suficiente para um ataque offline com dicionário."

---

#### ⏰ 5:00 - Handshake Capturado

**📺 Terminal do Ferro mostra:**
```
[!] HANDSHAKE CAPTURADO! → hashes/wifi_sample.hc22000
```

**👤 Henrique:**
> "Pronto! Handshake capturado. Agora vamos para a fase de cracking offline."

---

#### ⏰ 6:00 - Começar Cracking

**💻 Ferro executa:**
```bash
python wifi_cracker.py --crack --hash hashes/wifi_sample.hc22000
```

**📺 Output em tempo real:**
```
[*] Cracking WPA2 com hashcat mode 22000...
[*] Wordlist: wordlists/rockyou.txt
[*] Testando passwords...
[+] PASSWORD ENCONTRADA: Cibersegura
[+] Tempo: 3.2 segundos
```

**👤 Henrique explica:**
> "Em apenas **3 segundos**, a GPU encontrou a password! Testou milhões de combinações da wordlist. 
> 
> Se a password fosse forte - 16+ caracteres aleatórios - este ataque demoraria anos. Mas 'Cibersegura' está numa wordlist comum."

**⏱️ Tempo total fase: ~7 minutos**

---

### FASE 3: TELNET CREDENTIAL CAPTURE (10:00-17:00)

**⏱️ Duração: 7 minutos**

---

#### ⏰ 10:00 - Setup Servidor + Wireshark

**💻 Francisco executa (terminal 1):**
```powershell
cd C:\Users\Francisco\HashCrackerLab
.\venv\Scripts\Activate.ps1
python telnet_authenticated_traffic.py --server --port 23
```

**📺 Output:**
```
[SERVER] Telnet listening on 0.0.0.0:23
[SERVER] Waiting for connections...
```

**💻 Francisco abre Wireshark (paralelo):**
```
1. Abrir Wireshark
2. Selecionar interface de rede (WiFi/Ethernet)
3. Filtro: tcp.port == 23
4. Start Capture
```

**👤 Henrique explica:**
> "O Francisco iniciou um servidor Telnet fake e o Wireshark para capturar todo o tráfego. Telnet não usa encriptação - tudo vai em texto claro."

---

#### ⏰ 11:00 - Cliente Conecta

**💻 Duarte executa (projector em split-screen: terminal + Wireshark):**
```powershell
telnet 192.168.100.30 23
```

**📺 Prompt Telnet:**
```
Username: admin
Password: SecurePass123
```

**💻 Duarte digita:**
```
admin [ENTER]
SecurePass123 [ENTER]
```

---

#### ⏰ 13:00 - Análise no Wireshark

**📺 Francisco mostra Wireshark (projetado):**
```
Packet #42: Telnet Data
    Source: 192.168.100.40 (Duarte)
    Destination: 192.168.100.30 (Francisco)
    Data: "admin"

Packet #43: Telnet Data
    Data: "SecurePass123"
```

**👤 Henrique narra (apontando para tela):**
> "Vejam aqui! A password **'SecurePass123'** aparece em **texto claro** no Wireshark. 
> 
> Qualquer pessoa nesta rede - um atacante com Wireshark - consegue ver as credenciais. 
> 
> Por isso, em produção, **NUNCA** usamos Telnet. Usamos SSH, que encripta tudo."

**👤 Francisco (mostra outro packet):**
> "E não é só a password. Tudo que o Duarte digitar - comandos, ficheiros - fica visível."

**⏱️ Tempo total fase: ~7 minutos**

---

### FASE 4: GPU CRACKING (17:00-27:00)

**⏱️ Duração: 10 minutos**

---

#### ⏰ 17:00 - Início da Demo GPU

**💻 Henrique executa (terminal em full screen no projector):**
```bash
cd ~/Projects/HashCrackerLab
source venv/bin/activate
python orchestrator.py --config config/advanced_encryption_test.yaml
```

**👤 Henrique narra (antes de executar):**
> "Agora vou demonstrar o poder das GPUs modernas. Vou gerar 20 hashes com **4 algoritmos diferentes**:
> - **MD5** - legacy, muito rápido
> - **SHA-256** - moderno, usado em Bitcoin
> - **Bcrypt** - resistente, tem 'cost factor'
> - **Argon2** - memory-hard, o mais recente e seguro
> 
> A GPU vai tentar cracka-los todos. Vejam a diferença de velocidade."

---

#### ⏰ 17:30 - Geração de Hashes

**📺 Output em tempo real:**
```
[*] Validando configuração... ✓
[*] Gerando 20 hashes com 4 algoritmos...
  - Bcrypt (cost 5): 5 hashes
  - Argon2 (memory-hard): 5 hashes
  - MD5 (sem salt): 5 hashes
  - SHA-256 (com salt): 5 hashes
[✓] 20 hashes gerados em 3.1 segundos
```

---

#### ⏰ 18:00 - Cracking Começa

**📺 Output continua (terminal a rolar):**
```
[*] Iniciando cracking com GPU NVIDIA...
[*] Modo: Dictionary Attack
[*] Wordlist: wordlists/rockyou.txt (14M passwords)

[GPU] MD5: 22.5 GH/s ⚡⚡⚡
[GPU] SHA-256: 8.2 GH/s ⚡⚡
[GPU] Bcrypt: 2.1 MH/s ⚡
[GPU] Argon2: 850 H/s

[!] Password encontrada: password (MD5) - 0.02s
[!] Password encontrada: 123456 (Bcrypt) - 0.8s
[!] Password encontrada: qwerty (SHA-256) - 0.1s
[!] Password encontrada: letmein (MD5) - 0.03s
[!] Password encontrada: password (Argon2) - 4.2s
...
```

**👤 Henrique explica (enquanto executa):**
> "Vejam a velocidade:
> - **MD5:** 22.5 **bilhões** de hashes por segundo! É por isso que MD5 não é mais usado para passwords.
> - **SHA-256:** 8.2 bilhões/s - ainda muito rápido
> - **Bcrypt:** Apenas 2.1 **milhões**/s - muito mais resistente porque tem 'cost factor'
> - **Argon2:** 850 hashes/s - memory-hard, o mais lento e seguro
> 
> A GPU é **16 vezes mais rápida** que CPU para MD5!"

---

#### ⏰ 19:00 - Resultados Finais

**📺 Output:**
```
[✓] Cracking concluído em 42 segundos!

RESUMO:
┌──────────┬───────┬───────────┬────────┐
│ Algoritmo│ Total │ Crackeadas│  Taxa  │
├──────────┼───────┼───────────┼────────┤
│ MD5      │   5   │     5     │ 100% ✓ │
│ SHA-256  │   5   │     4     │  80%   │
│ Bcrypt   │   5   │     4     │  80%   │
│ Argon2   │   5   │     3     │  60%   │
├──────────┼───────┼───────────┼────────┤
│ TOTAL    │  20   │    16     │  80%   │
└──────────┴───────┴───────────┴────────┘
```

**👤 Henrique:**
> "80% de sucesso. Porquê não 100%? Porque algumas passwords ('admin', 'teste') não estão na wordlist. Em produção, usam-se wordlists gigantes com milhões de entradas."

---

#### ⏰ 22:00 - Demo Visual de Brute-Force

**📺 Output continua:**
```
[*] DEMO: Simulando brute-force de PIN (0000-9999)...

Testando: 0000 ✗
Testando: 0001 ✗
Testando: 0002 ✗
...
Testando: 5237 ✗
Testando: 5238 ✗
Testando: 5239 ✓

[+] PIN encontrado: 5239
[+] Tempo: 2.1 segundos
[+] Tentativas: 5240 de 10000 possíveis
```

**👤 Henrique explica:**
> "Esta demo mostra o conceito de **tentativa e erro**. 
> 
> Para um PIN de 4 dígitos (10.000 combinações), a GPU levou 2 segundos.
> 
> Mas para uma password de 8 caracteres alfanuméricos: 62^8 = 218 **trilhões** de combinações. Mesmo a GPU demoraria anos!
> 
> **Por isso senhas fortes (16+ chars aleatórios) são críticas.**"

---

#### ⏰ 24:00 - Benchmark GPU vs CPU

**📺 Output final:**
```
[*] Benchmark GPU vs CPU:

┌──────────┬──────────┬──────────┬─────────────┐
│ Algoritmo│ GPU/sec  │ CPU/sec  │  Speedup    │
├──────────┼──────────┼──────────┼─────────────┤
│ MD5      │ 22.5GH/s │ 1.4GH/s  │ 16.5x ⚡⚡⚡ │
│ SHA-256  │ 8.2GH/s  │ 0.8GH/s  │  9.9x ⚡⚡  │
│ Bcrypt   │ 2.1MH/s  │ 0.4MH/s  │  5.2x ⚡    │
│ Argon2   │ 850 H/s  │ 140 H/s  │  6.1x ⚡    │
└──────────┴──────────┴──────────┴─────────────┘

[✓] Resultados salvos em: results/advanced_crypto_test_20260209_150345/
```

**👤 Henrique:**
> "Este benchmark mostra porque GPUs são usadas em Bitcoin mining e password cracking. 
> 
> A diferença é **brutal** - 16 vezes mais rápida para MD5. É por isso que data centers de cracking usam racks com dezenas de GPUs."

**⏱️ Tempo total fase: ~10 minutos**

---

### FASE 5: CONCLUSÕES (27:00-30:00)

**⏱️ Duração: 3 minutos**

---

#### ⏰ 27:00 - Resumo Final

**📺 Slide/Projector: Resumo das 3 Vulnerabilidades**

**👤 Henrique:**

> "**Resumo do que demonstramos hoje:**
> 
> **1. WiFi WPA2 - Crackeável Offline**
> - Handshake capturado em 2-3 minutos
> - Password crackeada em 3 segundos com GPU
> - **Proteção:** Senhas fortes (16+ caracteres aleatórios)
> 
> **2. Telnet - Credenciais em Texto Claro**
> - Tudo visível no Wireshark
> - Qualquer pessoa na rede consegue ver
> - **Proteção:** Usar SSH, HTTPS, VPNs sempre
> 
> **3. Hashes Fracos - GPU Cracking**
> - MD5: 22 bilhões de tentativas/segundo
> - GPU 16x mais rápida que CPU
> - **Proteção:** Algoritmos modernos (Argon2, Bcrypt) + senhas fortes"

---

#### ⏰ 28:30 - Lição Final

**👤 Henrique (conclusão):**

> "**A grande lição:**
> 
> Criptografia moderna (WPA2, Bcrypt, Argon2) é **matematicamente robusta**. 
> 
> Mas é **completamente inútil** se usarmos senhas fracas como:
> - 'password'
> - '123456'
> - 'Cibersegura'
> 
> Uma senha de 6 caracteres pode ser crackeada em minutos.
> Uma senha de 16+ caracteres aleatórios levaria **séculos** mesmo com GPU.
> 
> **Segurança = Algoritmos Fortes + Senhas Fortes**
> 
> Sem ambos, estamos vulneráveis."

---

#### ⏰ 29:00 - Q&A

**👤 Henrique:**

> "Perguntas?"

**📋 Tópicos de resposta (se perguntarem):**
- Quanto tempo demoraria com senha forte? → Séculos/milénios
- Isto é legal? → Apenas em ambientes controlados/autorizados (pentest)
- Como me proteger? → Senhas únicas 16+ chars, 2FA, password manager
- WPA3 é melhor? → Sim, mas ainda vulnerável a senhas fracas

**⏱️ Tempo total fase: ~3 minutos**

---

## 📋 CHECKLIST PRÉ-APRESENTAÇÃO (5 min antes)

**Todos:**
- [ ] Conectados à rede WiFi/Ethernet
- [ ] IPs funcionais: `ping 192.168.100.1`
- [ ] Projector conectado e testado
- [ ] Terminais abertos e prontos

**Henrique:**
- [ ] `python tools/validate_environment.py` → ✓
- [ ] `hashcat -I` → GPU detectada

**Ferro:**
- [ ] `iwconfig | grep mon` → wlan0mon existe
- [ ] Wordlist presente: `ls wordlists/rockyou.txt`

**Francisco:**
- [ ] Wireshark aberto
- [ ] Interface de rede selecionada
- [ ] Filtro preparado: `tcp.port == 23`

**Duarte:**
- [ ] Terminal aberto
- [ ] Comando telnet testado

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
