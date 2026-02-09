# 🎭 GUIA DE APRESENTAÇÃO (30 minutos)

**Demonstração Profissional de Segurança Ofensiva**

---

## ⏱️ CRONOGRAMA (30 minutos exatos)

| Tempo | Fase | Quem | O Quê |
|-------|------|------|-------|
| **0:00-3:00** | Introdução | Henrique | Apresentação da equipa + objetivos |
| **3:00-10:00** | WiFi WPA2 | Ferro | Captura handshake + crack |
| **10:00-17:00** | Telnet Demo | Francisco/Duarte | Servidor + Wireshark |
| **17:00-27:00** | GPU Cracking | Henrique | 4 algoritmos + benchmark |
| **27:00-30:00** | Conclusões | Henrique | Resumo + Q&A |

---

## ✅ PRÉ-REQUISITOS (Dia Anterior)

### Henrique (Arch Linux)
```bash
cd ~/Projects/HashCrackerLab
./setup_arch.sh
source venv/bin/activate
python tools/validate_environment.py  # Tudo ✓
hashcat -I  # GPU detectada
```

### Ferro (Kali Linux)
```bash
cd ~/Projects/HashCrackerLab
./setup_kali.sh
sudo airmon-ng start wlan0  # Interface wlan0mon criada
```

### Francisco + Duarte (Windows)
```powershell
cd C:\Users\[USER]\HashCrackerLab
.\setup_windows.ps1
wireshark --version  # Funciona
```

---

## 🌐 SETUP DE REDE (10 min antes)

### Router WiFi
```
SSID:     LAB-SERVERS
Password: Cibersegura
Tipo:     WPA2-PSK
Gateway:  192.168.100.1 (opcional)
```

### IPs (se necessário)
| Máquina | IP |
|---------|-----|
| Henrique | 192.168.100.10 |
| Ferro | 192.168.100.20 |
| Francisco | 192.168.100.30 |
| Duarte | 192.168.100.40 |

**Teste rápido:** `ping 192.168.100.1` em todas as máquinas

---

## 🎬 FASE 1: INTRODUÇÃO (0:00-3:00)

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

## 🎬 FASE 2: WiFi WPA2 CRACKING (3:00-10:00)

**Duração: 7 minutos**

### Passo 1: Captura (3:00-6:00)

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

### Passo 2: Cracking (6:00-10:00)

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

## 🎬 FASE 3: TELNET CREDENTIAL CAPTURE (10:00-17:00)

**Duração: 7 minutos**

### Passo 1: Servidor (10:00-11:00)

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

### Passo 2: Cliente Conecta (11:00-13:00)

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

### Passo 3: Análise Wireshark (13:00-17:00)

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

## 🎬 FASE 4: GPU CRACKING (17:00-27:00)

**Duração: 10 minutos**

### Passo 1: Execução (17:00-19:00)

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

### Passo 2: Acompanhar Output (19:00-22:00)

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

### Passo 3: Benchmark + Demo Brute-Force (22:00-27:00)

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

## 🎬 FASE 5: CONCLUSÕES (27:00-30:00)

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

## 🆘 PLANO B (Se algo falhar)

| Problema | Solução Rápida |
|----------|----------------|
| **WiFi não captura** | Usar handshake pré-capturado: `hashes/wifi_sample.hc22000` |
| **GPU não funciona** | Usar CPU mode (mais lento mas funciona) |
| **Wireshark sem tráfego** | Usar `tcpdump` em terminal: `tcpdump -i any tcp port 23 -A` |
| **Rede cai** | Executar apenas GPU demo standalone (17:00-27:00) |

---

## ✅ CHECKLIST PRÉ-APRESENTAÇÃO (5 min antes)

**Todos:**
- [ ] Conectados à rede WiFi/Ethernet
- [ ] IPs funcionais (`ping 192.168.100.1`)
- [ ] Projector conectado
- [ ] Slides prontos

**Henrique:**
- [ ] `python tools/validate_environment.py` → Tudo ✓
- [ ] GPU detectada: `hashcat -I`

**Ferro:**
- [ ] Interface monitor: `iwconfig | grep mon`

**Francisco:**
- [ ] Wireshark aberto e interface selecionada

---

## 📊 DIÁLOGOS PREPARADOS

### Henrique (Introdução)
> "Vamos demonstrar 3 vulnerabilidades críticas de segurança em redes corporativas."

### Henrique (Durante WiFi crack)
> "O handshake WPA2 contém informação suficiente para ataque offline. Com GPU, testamos milhões de passwords por segundo."

### Henrique (Durante Telnet)
> "Vejam como credenciais aparecem em texto claro. Por isso SSH é obrigatório em produção."

### Henrique (Durante GPU)
> "A GPU é 16 vezes mais rápida que CPU para MD5. Mas algoritmos modernos como Argon2 são muito mais resistentes."

### Henrique (Conclusão)
> "Criptografia é inútil sem senhas fortes. Uma senha de 6 chars cai em segundos."

---

**Status:** ✅ Pronto para apresentação de 30 minutos | **Última atualização:** 2026-02-09
