# 🎓 GUIA DA APRESENTAÇÃO — Projeto Final de Cibersegurança

**Unidade Curricular:** Projeto Final
**Grupo:** Henrique · Ferro · Francisco · Duarte
**Duração:** 30 minutos
**Data:** Fevereiro 2026

---

# PARTE I — PLANEAMENTO E ARQUITETURA

## Objetivo do Projeto

Demonstrar ao vivo três vetores de ataque comuns em redes corporativas e comparar a eficácia de diferentes algoritmos de hashing contra ataques com CPU e GPU.

**Pergunta de investigação:**
> *"Quão eficaz é a aceleração por GPU no cracking de passwords e como é que a escolha do algoritmo de hashing influencia a resistência a ataques?"*

## Arquitetura do Laboratório

```
┌─────────────────────────────────────────────────────────┐
│                  REDE ISOLADA (192.168.100.0/24)        │
│                                                         │
│    ┌──────────┐     WiFi WPA2      ┌──────────┐        │
│    │  Router   │◄──────────────────►│  Ferro   │        │
│    │ LAB-SERV. │    (Captura +      │ Kali     │        │
│    │ .100.1    │     Cracking)      │ .100.20  │        │
│    └────┬──────┘                    └──────────┘        │
│         │ Ethernet                                      │
│    ┌────┴──────┐                                        │
│    │ Henrique  │    Orquestrador                        │
│    │ Arch Linux│    GPU Cracking (NVIDIA)               │
│    │ .100.10   │    50 Hashes × 4 Algoritmos            │
│    └───────────┘    CPU vs GPU Benchmark                │
│                                                         │
│    ┌──────────┐     Telnet (23)     ┌──────────┐        │
│    │ Francisco│◄───────────────────►│  Duarte  │        │
│    │ Windows  │   Servidor +        │ Windows  │        │
│    │ .100.30  │   Wireshark         │ .100.40  │        │
│    └──────────┘                     └──────────┘        │
└─────────────────────────────────────────────────────────┘
```

### Componentes do Sistema

```
HashCrackerLab/
├── orchestrator.py           ← Motor principal (gera hashes → cracking → relatório)
├── wifi_cracker.py           ← Captura e cracking WPA2
├── telnet_authenticated_traffic.py  ← Servidor/cliente Telnet
├── config/
│   ├── quick_test.yaml          ← Teste rápido (<30s, verificar erros)
│   ├── apresentacao_final.yaml  ← Apresentação (50 hashes, CPU+GPU, rede isolada)
│   └── real_world.yaml          ← Mundo real (100 hashes, 5 ataques, costs reais)
├── src/
│   ├── hash_generator.py     ← Gera hashes (MD5, SHA-256, Bcrypt, Argon2)
│   ├── cracking_manager.py   ← Executa hashcat (CPU vs GPU via -D flag)
│   ├── metrics_collector.py  ← Agrega métricas e exporta CSV/JSON
│   ├── network_manager.py    ← Verificação de rede isolada
│   └── cleanup_manager.py    ← Limpeza segura de dados
├── wordlists/
│   ├── rockyou.txt           ← 14.3M passwords (RockYou completa)
│   └── rockyou-small.txt     ← 10.000 passwords (quick test)
└── results/                  ← Relatórios gerados automaticamente
```

### Fluxo de Execução

```
  Config YAML ──► Orchestrator ──► Hash Generator ──► 50 hashes (4 algoritmos)
                       │
                       ├──► Cracking Manager (GPU -D 2) ──► resultados GPU
                       ├──► Cracking Manager (CPU -D 1) ──► resultados CPU
                       │
                       └──► Metrics Collector ──► Tabela comparativa CPU vs GPU
                                                   │
                                                   └──► REPORT.md + CSV + JSON
```

### Algoritmos Testados

| Algoritmo | Hashcat Mode | Tipo | Porquê |
|-----------|-------------|------|--------|
| **MD5** | 0 | Hash simples | Obsoleto — demonstrar velocidade absurda |
| **SHA-256** | 1420 (salted) | Hash com salt | Comum em sistemas atuais |
| **Bcrypt** | 3200 | Adaptativo (cost) | Desenhado para ser lento |
| **Argon2id** | 34000 | Memory-hard | Estado da arte (vencedor PHC 2015) |

### Amostra de Passwords (50 total)

| Categoria | Quantidade | Exemplos | Expectativa |
|-----------|-----------|----------|-------------|
| Fracas (Top 20) | 20 | `123456`, `password`, `qwerty` | Crackeadas em todos os algoritmos |
| Médias | 15 | `summer2024`, `hunter42` | Crackeadas em MD5/SHA-256, algumas em Bcrypt |
| Fortes | 15 | `X7k#mP9$vL2@`, `Cr¥pt0_L4b_99` | Resistem a todos os algoritmos |

---

## Cronograma da Apresentação

| Tempo | Fase | Quem Fala | Quem Executa |
|-------|------|-----------|-------------|
| 0:00–3:00 | Introdução + Arquitetura | Henrique | — |
| 3:00–10:00 | WiFi WPA2 Cracking | Henrique narra | Ferro executa |
| 10:00–17:00 | Telnet + Wireshark | Henrique narra | Francisco + Duarte |
| 17:00–27:00 | Hash Cracking (50 hashes, 5 ataques, CPU vs GPU) | Henrique | Henrique |
| 27:00–30:00 | Conclusões + Perguntas | Henrique | — |

---

## Divisão de Tarefas

| Membro | Responsabilidade | Sistema | Ferramentas |
|--------|-----------------|---------|-------------|
| **Henrique** | Coordenação, orquestrador, GPU cracking, narração | Arch Linux | Python, Hashcat, GPU NVIDIA |
| **Ferro** | WiFi — captura handshake + cracking WPA2 | Kali Linux | aircrack-ng, hashcat |
| **Francisco** | Servidor Telnet + Wireshark (mostrar pacotes) | Windows | Python, Wireshark |
| **Duarte** | Cliente Telnet (gerar tráfego) | Windows | Telnet client |

---

# PARTE II — SETUP (Dia Anterior)

## Instalar Dependências

**Henrique (Arch):**
```bash
cd ~/Projects/HashCrackerLab
./setup_arch.sh
source venv/bin/activate
python tools/validate_environment.py
hashcat -I   # Confirmar GPU NVIDIA
```

**Ferro (Kali):**
```bash
cd ~/Projects/HashCrackerLab
./setup_kali.sh
source venv/bin/activate
sudo airmon-ng start wlan0   # Criar wlan0mon
```

**Francisco + Duarte (Windows):**
```powershell
cd C:\Users\[USER]\HashCrackerLab
.\setup_windows.ps1
.\venv\Scripts\Activate.ps1
wireshark --version
```

## Configurar o Router (10 min antes)

1. Ligar o router à corrente e esperar 2 minutos.
2. Ligar cabo Ethernet do router ao PC do Henrique.
3. No browser abrir `192.168.0.1` (ou `192.168.1.1`).
4. Login: `admin` / `admin` (ou ver etiqueta do router).
5. Menu **Wireless / WiFi**:

| Campo | Valor |
|-------|-------|
| SSID | `LAB-SERVERS` |
| Segurança | `WPA2-PSK (AES)` |
| Password | `Cibersegura` |

6. Guardar → router reinicia (~1 min).
7. Menu **LAN / Network**:

| Campo | Valor |
|-------|-------|
| Gateway IP | `192.168.100.1` |
| Máscara | `255.255.255.0` |

8. Guardar → router reinicia → entrar em `http://192.168.100.1`.
9. Menu **DHCP**: confirmar ON, range `192.168.100.100` – `192.168.100.200`.
10. Guardar.

## Conectar Todos à Rede

| Máquina | IP | Ligação |
|---------|-----|---------|
| Henrique | 192.168.100.10 | Cabo Ethernet |
| Ferro | 192.168.100.20 | WiFi `LAB-SERVERS` |
| Francisco | 192.168.100.30 | WiFi `LAB-SERVERS` |
| Duarte | 192.168.100.40 | WiFi `LAB-SERVERS` |

```bash
# Verificar: em todas as máquinas
ping 192.168.100.1
```

---

# PARTE III — GUIÃO DA APRESENTAÇÃO

## 0:00 — INTRODUÇÃO + ARQUITETURA

**HENRIQUE:**
> "Bom dia. Somos alunos de Cibersegurança e hoje vamos demonstrar ao vivo três vetores de ataque que existem em qualquer rede.
>
> Primeiro, o Ferro vai capturar o handshake WPA2 do nosso router e crackar a password do WiFi.
> Depois, o Francisco e o Duarte vão mostrar como o protocolo Telnet expõe credenciais em texto claro.
> Por fim, vou usar o nosso laboratório para gerar 50 hashes com 4 algoritmos diferentes — MD5, SHA-256, Bcrypt e Argon2 — e comparar a velocidade de cracking entre CPU e GPU.
>
> Desenvolvemos um orquestrador em Python que automatiza todo o processo: gera as hashes, lança o hashcat na GPU e no CPU, e produz um relatório comparativo."

*(Mostrar diagrama de arquitetura no projetor)*

**HENRIQUE:**
> "A nossa rede isolada tem 4 máquinas. Usamos 50 passwords — 20 fracas, 15 médias e 15 fortes — para testar 4 algoritmos de hashing com 5 modos de ataque: dicionário, dicionário com regras de mutação, brute-force, brute-force por padrão e ataque híbrido."

---

## 3:00 — WiFi WPA2 CRACKING

**HENRIQUE:**
> "O Ferro vai agora colocar o adaptador WiFi em modo monitor. Isto permite capturar todos os pacotes wireless da rede, incluindo o handshake WPA2 — os 4 pacotes criptográficos que o router troca com cada cliente quando se liga. Ferro, arranca."

**FERRO** executa:
```bash
cd ~/Projects/HashCrackerLab
source venv/bin/activate
sudo airmon-ng check kill
sudo airmon-ng start wlan0
python wifi_cracker.py --capture --ssid LAB-SERVERS --interface wlan0mon
```

```
[+] Interface em modo monitor!
[*] Escaneando para encontrar BSSID...
[+] Encontrado: LAB-SERVERS (AA:BB:CC:DD:EE:FF)
[*] Capturando handshake...
[*] Aguardando handshake WPA2...
```

**HENRIQUE** (enquanto espera):
> "Enquanto ele espera, vou explicar: o handshake WPA2 não contém a password diretamente, mas contém informação suficiente para a testar offline. Basta alguém ligar-se ao WiFi para o handshake ser gerado. O Ferro vai agora forçar isso com um deauth."

**FERRO** executa deauth (noutro terminal):
```bash
python wifi_cracker.py --deauth --ssid LAB-SERVERS --interface wlan0mon
```

```
[*] Deauth Attack
    Alvo:      AA:BB:CC:DD:EE:FF
    Interface: wlan0mon
    Pacotes:   5 × 3 rondas

  [1/3] Enviando 5 deauth packets...
  [2/3] Enviando 5 deauth packets...
  [3/3] Enviando 5 deauth packets...

[+] Deauth concluído — clientes devem reconectar (handshake gerado).
```

**HENRIQUE:**
> "O deauth forçou todos os clientes a desligar-se. Quando reconectam automaticamente, o router gera um novo handshake e o Ferro captura-o."

*(No primeiro terminal)*
```
[+] HANDSHAKE CAPTURADO! → hashes/wifi_sample.hc22000
```

**HENRIQUE:**
> "Handshake capturado. A partir daqui, o Ferro pode testar passwords offline. Ferro, lança o cracking."

**FERRO** executa:
```bash
python wifi_cracker.py --crack hashes/wifi_sample.hc22000
```

```
[*] Cracking WPA2 com hashcat mode 22000...
[*] Wordlist: wordlists/custom.txt
[+] PASSWORD ENCONTRADA: Cibersegura
[+] Tempo: 3.2 segundos
```

**HENRIQUE:**
> "3 segundos. A GPU testou milhões de palavras do dicionário RockYou e encontrou 'Cibersegura'. Uma password com uma palavra e uma maiúscula cai em segundos. Se fosse aleatória com 16+ caracteres, este ataque demoraria anos."

---

## 10:00 — TELNET CREDENTIAL CAPTURE

**HENRIQUE:**
> "Agora vamos demonstrar outro problema clássico: protocolos sem encriptação. O Telnet é um protocolo dos anos 70 que ainda se usa em muitas empresas. O Francisco vai iniciar um servidor Telnet e o Duarte vai ligar-se como administrador. Francisco, liga o servidor."

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
> "Francisco, abre o Wireshark e filtra por Telnet."

**FRANCISCO** abre Wireshark:
```
Filtro: tcp.port == 23
→ Start Capture
```

**HENRIQUE:**
> "O Wireshark está a capturar todo o tráfego. Duarte, liga-te ao servidor."

**DUARTE** executa:
```powershell
telnet 192.168.100.30 23
```

```
Username: admin
Password: SecurePass123
```

**HENRIQUE:**
> "Parece normal. Agora vejam o que o Francisco vê no Wireshark."

**FRANCISCO** mostra no projetor:
```
Packet #42  192.168.100.40 → 192.168.100.30  Telnet Data: "admin"
Packet #43  192.168.100.40 → 192.168.100.30  Telnet Data: "SecurePass123"
```

**FRANCISCO:**
> "A password 'SecurePass123' aparece em texto claro. Qualquer pessoa nesta rede com Wireshark consegue ver."

**HENRIQUE:**
> "Zero encriptação. A solução é simples: usar **SSH** em vez de Telnet. O SSH encripta tudo — no Wireshark só se vê ruído."

---

## 17:00 — HASH CRACKING (50 Hashes · 5 Ataques · CPU vs GPU)

**HENRIQUE:**
> "Agora a parte principal do nosso projeto. Vou gerar 50 hashes — 50 passwords diferentes — com 4 algoritmos: MD5, SHA-256, Bcrypt e Argon2. O orquestrador vai usar **5 modos de ataque diferentes**: dicionário simples, dicionário com regras de mutação, brute-force de PINs, brute-force por padrão e ataque híbrido. Tudo primeiro com GPU, depois CPU, para compararmos."

**HENRIQUE** executa:
```bash
cd ~/Projects/HashCrackerLab
source venv/bin/activate
python orchestrator.py --config config/apresentacao_final.yaml
```

```
[*] Validando configuração... ✓
[*] Gerando 200 hashes (50 passwords × 4 algoritmos)...
  - MD5 (sem salt): 50 hashes
  - SHA-256 (com salt): 50 hashes
  - Bcrypt (cost 5): 50 hashes
  - Argon2id (memory-hard): 50 hashes
[✓] 200 hashes gerados em 8.4 segundos
```

**HENRIQUE:**
> "200 hashes no total — 50 por algoritmo. Agora o hashcat vai primeiro usar a GPU."

### Fase GPU — 5 Modos de Ataque

```
[*] ==================================================
[*] Dispositivo: GPU (NVIDIA OpenCL)
[*] ==================================================

── Ataque 1/5: Dicionário (rockyou.txt — 14.3M passwords) ──
[GPU] MD5 (mode 0): 22.5 GH/s
[!] 123456 → 0.01s    [!] password → 0.01s    [!] qwerty → 0.02s
... (20 fracas + ~8 médias)
[✓] MD5: 28/50    SHA-256: 26/50    Bcrypt: 20/50    Argon2: 16/50

── Ataque 2/5: Dicionário + Regras best66.rule ──
[*] Mutações: p→P, a→@, o→0, sufixo 123, etc.
[✓] MD5: +4 → 32/50    SHA-256: +3 → 29/50    Bcrypt: +3 → 23/50    Argon2: +2 → 18/50

── Ataque 3/5: Brute-force PIN (?d?d?d?d) ──
[*] Keyspace: 10.000 combinações (0000–9999)
[+] PIN encontrado: 5239 → 0.8s
[✓] MD5: +1 → 33/50    (restantes: sem PINs puros)

── Ataque 4/5: Brute-force Padrão (?u?l?l?l?d?d) ──
[*] Keyspace: 11.881.376 combinações (ex: Adam99, Test42)
[✓] MD5: +0    SHA-256: +0    Bcrypt: +0    Argon2: +0
[*] Nenhuma password nova — padrão não corresponde às restantes

── Ataque 5/5: Híbrido — wordlist + ?d?d?d ──
[*] Cada password da wordlist + 000–999 (ex: password123, admin007)
[✓] MD5: +2 → 35/50    SHA-256: +1 → 30/50    Bcrypt: +1 → 24/50    Argon2: +1 → 19/50

[*] ── RESUMO GPU (5 ataques combinados) ──
[✓] MD5 GPU:     35/50 crackeadas — 2.1s total
[✓] SHA-256 GPU: 30/50 crackeadas — 5.8s total
[✓] Bcrypt GPU:  24/50 crackeadas — 22s total
[✓] Argon2 GPU:  19/50 crackeadas — 48s total
```

**HENRIQUE:**
> "Com 5 ataques diferentes, crackeámos 35 de 50 em MD5 — o dicionário base apanhou as fracas, as regras de mutação apanharam variações como 'summer2024' ou 'pass1234', e o híbrido apanhou as que tinham dígitos no final. Em Argon2 só crackeámos 19, e demorou 48 segundos. Agora o mesmo com CPU."

### Fase CPU — Mesmos 5 Ataques

```
[*] ==================================================
[*] Dispositivo: CPU
[*] ==================================================

── Ataques 1–5 em CPU (mesma sequência) ──

[CPU] MD5 (mode 0): 1.4 GH/s
[✓] MD5 CPU: 35/50 crackeadas — 34s total

[CPU] SHA-256 (mode 1420): 0.8 GH/s
[✓] SHA-256 CPU: 30/50 crackeadas — 72s total

[CPU] Bcrypt (mode 3200): 0.4 MH/s
[✓] Bcrypt CPU: 24/50 crackeadas — timeout (>180s)

[CPU] Argon2id (mode 34000): 140 H/s
[✓] Argon2 CPU: 19/50 crackeadas — timeout (>180s)
```

**HENRIQUE:**
> "Mesmas passwords crackeadas — porque é a mesma wordlist e os mesmos 5 ataques — mas vejam os tempos. MD5 com GPU levou 2 segundos; com CPU levou 34. O Bcrypt e Argon2 no CPU nem terminaram dentro do tempo. Isto mostra duas coisas: o poder da GPU e a importância dos algoritmos memory-hard."

### Tabela Comparativa Final

```
┌──────────┬───────┬───────────┬──────────────┬──────────────┬─────────┐
│ Algoritmo│ Total │ Crackeadas│   Tempo GPU  │  Tempo CPU   │ Speedup │
├──────────┼───────┼───────────┼──────────────┼──────────────┼─────────┤
│ MD5      │  50   │    35     │    2.1s      │   34.0s      │  16.2x  │
│ SHA-256  │  50   │    30     │    5.8s      │   72.0s      │  12.4x  │
│ Bcrypt   │  50   │    24     │   22.0s      │  timeout     │   >8x   │
│ Argon2   │  50   │    19     │   48.0s      │  timeout     │   >6x   │
├──────────┼───────┼───────────┼──────────────┼──────────────┼─────────┤
│ TOTAL    │ 200   │   108     │  ~78s        │  >300s       │         │
└──────────┴───────┴───────────┴──────────────┴──────────────┴─────────┘

Modos de ataque usados: Dicionário │ Dicionário+Regras │ Brute-force PIN │
                        Brute-force Padrão │ Híbrido (wordlist+dígitos)
```

**HENRIQUE:**
> "108 de 200 — 54%. Os 5 modos de ataque em conjunto são muito mais eficazes que só o dicionário. As regras de mutação apanharam variações como 'summer2024', o híbrido apanhou passwords com dígitos no final. Mas as 15 passwords fortes resistiram a tudo — em qualquer algoritmo."

> "A diferença de velocidade é brutal: MD5 com GPU — 2 segundos para 5 ataques. Argon2 com CPU — nem terminou. Uma password que demoraria 1 hora a crackar com MD5 demoraria 3 anos com Argon2. E um PIN de 4 dígitos — 10 mil combinações — cai em menos de 1 segundo."

---

## 27:00 — CONCLUSÕES

**HENRIQUE:**
> "Resumindo o que demonstrámos:
>
> **WiFi** — Password crackeada em 3 segundos. Proteção: passwords longas e aleatórias, mínimo 16 caracteres.
>
> **Telnet** — Credenciais visíveis em texto claro. Proteção: usar SSH.
>
> **Hashes (50 passwords × 4 algoritmos × 5 modos de ataque):**
> - **5 ataques combinados** (dicionário, regras, brute-force, padrão, híbrido) são muito mais eficazes que dicionário sozinho — crackeámos 54% em vez de ~40%.
> - MD5 é **16x mais rápido** na GPU — completamente inadequado para passwords.
> - Argon2 é **26 milhões de vezes** mais lento que MD5, neutralizando a vantagem da GPU.
> - Mas **nenhum algoritmo** salva uma password fraca — '123456' cai sempre.
>
> A conclusão é clara: **segurança = algoritmo forte + password forte**. Sem os dois, estamos vulneráveis.
>
> Obrigado. Perguntas?"

---

# PARTE IV — PLANO B

| Problema | Solução Imediata |
|----------|-----------------|
| WiFi não captura handshake | Usar ficheiro pré-capturado: `hashes/wifi_sample.hc22000` |
| GPU não detectada | Correr só com CPU: editar YAML → `gpu.enabled: false` |
| Wireshark sem tráfego | `tcpdump -i any tcp port 23 -A` no terminal |
| Rede cai | Fazer só demo GPU standalone (não precisa de rede) |
| Import error | `pip install -r requirements.txt` |
| Argon2 timeout no CPU | Normal — explicar que isso prova o ponto |
| Hashcat erro OpenCL | `hashcat -I` → verificar drivers → `sudo pacman -S opencl-nvidia` |

---

# PARTE V — REFERÊNCIA TÉCNICA

## Configs Disponíveis

```bash
# 1. Teste rápido (<30s) — verificar que tudo funciona
python orchestrator.py --config config/quick_test.yaml

# 2. Apresentação final (50 hashes, CPU vs GPU) — DIA DA APRESENTAÇÃO
python orchestrator.py --config config/apresentacao_final.yaml

# 3. Mundo real (100 hashes, 5 modos de ataque, costs reais)
python orchestrator.py --config config/real_world.yaml

# Dry-run (sem cracking, só validação)
python orchestrator.py --config config/apresentacao_final.yaml --dry-run
```

## Ver Resultados

```bash
# Último relatório
LAST=$(ls -td results/*/ | head -1)
cat "$LAST/REPORT.md"

# Passwords crackeadas por algoritmo e dispositivo
cat "$LAST/cracked/md5_gpu/cracked_md5_dictionary.pot"
cat "$LAST/cracked/md5_cpu/cracked_md5_dictionary.pot"
```

## Troubleshooting

```bash
# GPU não detectada
hashcat -I
sudo pacman -S opencl-nvidia   # Arch

# WiFi não entra em monitor
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# Dependências Python
pip install -r requirements.txt

# Benchmark rápido
hashcat -b -m 0    # MD5
hashcat -b -m 3200 # Bcrypt
```
