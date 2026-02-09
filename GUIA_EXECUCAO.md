# 🎭 GUIA DA APRESENTAÇÃO (30 minutos)

| Tempo | Fase | Quem |
|-------|------|------|
| 0:00-3:00 | Introdução | Henrique |
| 3:00-10:00 | WiFi WPA2 | Ferro |
| 10:00-17:00 | Telnet | Francisco + Duarte |
| 17:00-27:00 | GPU Cracking | Henrique |
| 27:00-30:00 | Conclusões | Henrique |

---

## SETUP (Dia Anterior)

**Henrique (Arch):** `./setup_arch.sh`
**Ferro (Kali):** `./setup_kali.sh`
**Francisco/Duarte (Windows):** `.\setup_windows.ps1`

**Router WiFi:** SSID `LAB-SERVERS` | Password `Cibersegura` | WPA2-PSK

---

# GUIÃO

## 0:00 — INTRODUÇÃO

**HENRIQUE:**
> "Bom dia. Somos uma equipa de cibersegurança e hoje vamos demonstrar ao vivo 3 vulnerabilidades críticas que existem em qualquer rede corporativa.
>
> Primeiro, o Ferro vai crackar a password do WiFi desta rede.
> Depois, o Francisco e o Duarte vão mostrar como credenciais viajam em texto claro no Telnet.
> Por fim, eu vou usar a GPU para quebrar hashes de 4 algoritmos diferentes.
>
> Comecemos."

---

## 3:00 — WiFi WPA2 CRACKING

**HENRIQUE:**
> "O Ferro vai agora entrar em modo monitor — isto significa que o adaptador WiFi dele vai capturar TODOS os pacotes wireless, não só os destinados a ele. Ferro, arranca."

**FERRO** executa:
```bash
cd ~/Projects/HashCrackerLab
source venv/bin/activate
python wifi_cracker.py --capture --ssid LAB-SERVERS --interface wlan0mon
```

```
[*] Modo monitor: wlan0mon
[*] Escutando rede: LAB-SERVERS (Canal 6)
[*] Aguardando handshake WPA2...
```

**HENRIQUE** (enquanto espera):
> "Neste momento ele está à escuta. Quando alguém se liga ou religa ao WiFi, o router e o cliente trocam um 'handshake' — 4 pacotes criptográficos. É isto que precisamos capturar. Não precisamos da password, só destes 4 pacotes."

*(Alguém desliga e liga o WiFi, ou Ferro força um deauth)*

```
[!] HANDSHAKE CAPTURADO! → hashes/wifi_sample.hc22000
```

**HENRIQUE:**
> "Pronto, handshake capturado. Agora o Ferro tem tudo o que precisa para tentar crackar a password **offline**, sem estar ligado ao router. Ferro, avança com o cracking."

**FERRO** executa:
```bash
python wifi_cracker.py --crack --hash hashes/wifi_sample.hc22000
```

```
[*] Cracking WPA2 com hashcat mode 22000...
[*] Wordlist: wordlists/rockyou.txt
[*] Testando passwords...
[+] PASSWORD ENCONTRADA: Cibersegura
[+] Tempo: 3.2 segundos
```

**HENRIQUE:**
> "3 segundos. A GPU testou milhões de palavras de uma wordlist e encontrou 'Cibersegura'. Se a password fosse aleatória com 16 ou mais caracteres, este ataque demoraria **anos**. Mas passwords como esta — uma palavra com maiúscula — caem em segundos."

---

## 10:00 — TELNET CREDENTIAL CAPTURE

**HENRIQUE:**
> "Agora vamos demonstrar outro problema clássico: protocolos sem encriptação. O Francisco vai iniciar um servidor Telnet e o Duarte vai ligar-se como se fosse um administrador. Francisco, liga o servidor."

**FRANCISCO** executa:
```powershell
cd C:\Users\Francisco\HashCrackerLab
.\venv\Scripts\Activate.ps1
python telnet_authenticated_traffic.py --server --port 23
```

```
[SERVER] Telnet listening on 0.0.0.0:23
[SERVER] Waiting for connections...
```

**HENRIQUE:**
> "Servidor ativo. Agora, Francisco, abre o Wireshark e mete o filtro para Telnet."

**FRANCISCO** abre Wireshark:
```
Filtro: tcp.port == 23
→ Start Capture
```

**HENRIQUE:**
> "O Wireshark está a capturar todo o tráfego da rede. Duarte, liga-te ao servidor do Francisco como se fosses um administrador."

**DUARTE** executa:
```powershell
telnet 192.168.100.30 23
```

```
Username: admin
Password: SecurePass123
```

**DUARTE:**
> "Pronto, liguei-me ao servidor com as credenciais de administrador."

**HENRIQUE:**
> "Parece normal, certo? Agora vejam o que o Francisco vê no Wireshark."

**FRANCISCO** mostra Wireshark no projector:
```
Packet #42  192.168.100.40 → 192.168.100.30  Telnet Data: "admin"
Packet #43  192.168.100.40 → 192.168.100.30  Telnet Data: "SecurePass123"
```

**FRANCISCO:**
> "Aqui está. A password 'SecurePass123' aparece em texto claro. Qualquer pessoa nesta rede com Wireshark consegue ver."

**HENRIQUE:**
> "Isto é o Telnet — um protocolo dos anos 70 que ainda é usado em muitas empresas. Zero encriptação. Tudo visível. A solução é simples: usar **SSH** em vez de Telnet. O SSH encripta tudo e ninguém vê nada no Wireshark."

---

## 17:00 — GPU HASH CRACKING

**HENRIQUE:**
> "Agora a parte principal. Vou demonstrar como uma GPU moderna consegue quebrar passwords encriptadas. Vou gerar 20 hashes com 4 algoritmos diferentes e tentar cracka-los todos."

**HENRIQUE** executa:
```bash
cd ~/Projects/HashCrackerLab
source venv/bin/activate
python orchestrator.py --config config/advanced_encryption_test.yaml
```

```
[*] Validando configuração... ✓
[*] Gerando 20 hashes com 4 algoritmos...
  - MD5 (sem salt): 5 hashes
  - SHA-256 (com salt): 5 hashes
  - Bcrypt (cost 5): 5 hashes
  - Argon2 (memory-hard): 5 hashes
[✓] 20 hashes gerados em 3.1 segundos
```

**HENRIQUE** (enquanto gera):
> "Estou a criar 5 hashes de cada algoritmo. O MD5 é antigo e rápido — já não devia ser usado. O SHA-256 é mais moderno. O Bcrypt tem um 'cost factor' que o torna propositadamente lento. E o Argon2 é o mais recente — usa muita memória RAM para dificultar ataques com GPU."

```
[*] Iniciando cracking com GPU NVIDIA...

[GPU] MD5: 22.5 GH/s
[!] password (MD5) - 0.02s
[!] 123456 (MD5) - 0.02s
[!] qwerty (MD5) - 0.03s
[!] letmein (MD5) - 0.03s
[!] iloveyou (MD5) - 0.04s
```

**HENRIQUE:**
> "Vejam isto. MD5 — 22.5 **bilhões** de hashes por segundo. Todas as 5 passwords crackeadas em menos de 1 décimo de segundo. MD5 está completamente morto para passwords."

```
[GPU] SHA-256: 8.2 GH/s
[!] password (SHA-256) - 0.1s
[!] 123456 (SHA-256) - 0.1s
[!] qwerty (SHA-256) - 0.1s
[!] letmein (SHA-256) - 0.2s
```

**HENRIQUE:**
> "SHA-256 é mais lento — 8 bilhões por segundo — mas ainda assim caíram quase todas. 4 de 5."

```
[GPU] Bcrypt: 2.1 MH/s
[!] password (Bcrypt) - 0.8s
[!] 123456 (Bcrypt) - 1.2s
[!] qwerty (Bcrypt) - 1.5s
[!] letmein (Bcrypt) - 2.1s
```

**HENRIQUE:**
> "Bcrypt — reparem na diferença. Já não são bilhões, são 2 **milhões** por segundo. Mil vezes mais lento. Isto é de propósito — o Bcrypt foi desenhado para ser lento. Mesmo assim, com passwords fracas, cai."

```
[GPU] Argon2: 850 H/s
[!] password (Argon2) - 4.2s
[!] 123456 (Argon2) - 5.8s
[!] qwerty (Argon2) - 7.1s
```

**HENRIQUE:**
> "Argon2 — 850 hashes por segundo. **Vinte e seis milhões de vezes** mais lento que MD5. Este algoritmo usa muita memória RAM de propósito, o que neutraliza a vantagem das GPUs. É o estado da arte. Mas reparem — mesmo assim, passwords fracas como 'password' e '123456' foram encontradas. Porquê? Porque estão no topo de qualquer wordlist."

```
[✓] Cracking concluído!

┌──────────┬───────┬───────────┬────────┐
│ Algoritmo│ Total │ Crackeadas│  Taxa  │
├──────────┼───────┼───────────┼────────┤
│ MD5      │   5   │     5     │ 100%   │
│ SHA-256  │   5   │     4     │  80%   │
│ Bcrypt   │   5   │     4     │  80%   │
│ Argon2   │   5   │     3     │  60%   │
├──────────┼───────┼───────────┼────────┤
│ TOTAL    │  20   │    16     │  80%   │
└──────────┴───────┴───────────┴────────┘
```

**HENRIQUE:**
> "16 de 20. As que não caíram usam passwords que não estão na wordlist. Com uma wordlist maior — milhões de entradas — a taxa subiria. Agora vejam o brute-force."

```
[*] DEMO: Brute-force de PIN (0000-9999)...
Testando: 0000 ✗ ... 5238 ✗ ... 5239 ✓

[+] PIN encontrado: 5239
[+] Tempo: 2.1 segundos
[+] Tentativas: 5240 de 10000
```

**HENRIQUE:**
> "Um PIN de 4 dígitos — 10 mil combinações — 2 segundos. Agora imaginem uma password de 8 caracteres com letras, números e símbolos: são 6 **quatrilhões** de combinações. Mesmo com GPU, demoraria séculos. É a diferença entre uma password fraca e uma forte."

```
[*] Benchmark GPU vs CPU:

┌──────────┬──────────┬──────────┬─────────┐
│ Algoritmo│ GPU/sec  │ CPU/sec  │ Speedup │
├──────────┼──────────┼──────────┼─────────┤
│ MD5      │ 22.5GH/s │ 1.4GH/s  │  16.5x  │
│ SHA-256  │  8.2GH/s │ 0.8GH/s  │   9.9x  │
│ Bcrypt   │  2.1MH/s │ 0.4MH/s  │   5.2x  │
│ Argon2   │   850H/s │  140H/s  │   6.1x  │
└──────────┴──────────┴──────────┴─────────┘
```

**HENRIQUE:**
> "E este benchmark mostra o porquê de usarmos GPUs. Para MD5, a GPU é 16 vezes mais rápida que o CPU. Data centers de cracking usam centenas de GPUs em paralelo. Um atacante motivado tem este poder."

---

## 27:00 — CONCLUSÕES

**HENRIQUE:**
> "Resumindo o que vimos hoje:
>
> **WiFi** — capturamos o handshake e crackeamos a password em 3 segundos. Proteção: passwords longas e aleatórias, no mínimo 16 caracteres.
>
> **Telnet** — as credenciais apareceram em texto claro no Wireshark. Proteção: usar SSH em vez de Telnet, HTTPS em vez de HTTP.
>
> **Hashes** — o MD5 caiu instantaneamente. Até o Argon2, o melhor algoritmo atual, não resiste a passwords fracas. Proteção: algoritmos modernos **mais** passwords fortes.
>
> A grande lição é simples: a criptografia moderna é matematicamente perfeita. Mas se a password for '123456', não há algoritmo que salve. Segurança é algoritmos fortes **mais** passwords fortes. Sem os dois, estamos vulneráveis.
>
> Perguntas?"

---

# PLANO B

| Problema | Solução |
|----------|---------|
| WiFi não captura handshake | Usar ficheiro pré-capturado: `hashes/wifi_sample.hc22000` |
| GPU não detectada | Usar CPU (mais lento mas funciona) |
| Wireshark sem tráfego | `tcpdump -i any tcp port 23 -A` |
| Rede cai | Fazer só GPU demo standalone |
| Import error | `pip install -r requirements.txt` |

---

# SETUP TÉCNICO

## Pré-Requisitos (Dia Anterior)

**Henrique (Arch):**
```bash
cd ~/Projects/HashCrackerLab
./setup_arch.sh
source venv/bin/activate
python tools/validate_environment.py
hashcat -I
```

**Ferro (Kali):**
```bash
cd ~/Projects/HashCrackerLab
./setup_kali.sh
sudo airmon-ng start wlan0
```

**Francisco + Duarte (Windows):**
```powershell
cd C:\Users\[USER]\HashCrackerLab
.\setup_windows.ps1
wireshark --version
```

## Rede

```
Router: SSID LAB-SERVERS | WPA2 | Password Cibersegura
```

| Máquina | IP |
|---------|-----|
| Henrique | 192.168.100.10 |
| Ferro | 192.168.100.20 |
| Francisco | 192.168.100.30 |
| Duarte | 192.168.100.40 |

**IPs fixos (se necessário):**
```bash
# Linux
nmtui

# Windows (PowerShell Admin)
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 192.168.100.30 -PrefixLength 24 -DefaultGateway 192.168.100.1
```

**Teste:** `ping 192.168.100.1`

## Configs Disponíveis

```bash
# Demo completa (20 hashes, 4 algoritmos) — RECOMENDADO
python orchestrator.py --config config/advanced_encryption_test.yaml

# Teste rápido
python orchestrator.py --config config/quick_test.yaml

# Config original do projeto
python orchestrator.py --config config/projeto_final_ciberseguranca.yaml
```

## Resultados

```bash
# Ver último relatório
LAST=$(ls -td results/*/ | head -1)
cat "$LAST/REPORT.md"

# Ver passwords crackeadas
cat "$LAST/cracked/md5/cracked_md5_dictionary.pot"
```

## Troubleshooting

```bash
# GPU não detectada
hashcat -I
sudo pacman -S opencl-nvidia  # Arch

# WiFi não entra em monitor
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# Dependências Python
pip install -r requirements.txt

# Verificar hashcat
hashcat --version
hashcat -b -m 0  # Benchmark MD5
```
