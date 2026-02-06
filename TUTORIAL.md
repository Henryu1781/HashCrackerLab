# Hash Cracker Lab - Tutorial Completo

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Instalação por Sistema Operativo](#instalação-por-sistema-operativo)
3. [Configuração da Rede LAB](#configuração-da-rede-lab)
4. [Uso Básico](#uso-básico)
5. [Uso Avançado](#uso-avançado)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## 🎯 Visão Geral

O Hash Cracker Lab é um ambiente educacional para estudar segurança de passwords através de:

- **Geração controlada de hashes** (Argon2, bcrypt, scrypt, PBKDF2, SHA-256, SHA-1, MD5)
- **Cracking automatizado** com Hashcat e Aircrack-ng
- **Captura WiFi** em ambiente LAB isolado
- **Métricas detalhadas** de performance e segurança
- **Limpeza automática** de dados sensíveis

### Arquitetura

```
┌─────────────────────────────────────┐
│  VM1: Orchestrator + GPU            │
│  (Henrique - Arch Linux)            │
│  - Coordenação                      │
│  - GPU Cracking                     │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┐
       │   LAN LAB     │
       │  (Isolada)    │
       └───┬───────┬───┘
           │       │
    ┌──────┴──┐ ┌─┴──────────────┐
    │ VM2:    │ │ VM3:           │
    │ Monitor │ │ Comunicação    │
    │ + CPU   │ │ (Duarte+       │
    │ Tester  │ │  Francisco-    │
    │ (Ferro  │ │  Windows +     │
    │  Kali)  │ │  VM Kali)      │
    └─────────┘ └────────────────┘
```

---

## 🖥️ Instalação por Sistema Operativo

### VM1: Arch Linux (Henrique - Orquestrador + GPU)

```bash
# 1. Clonar repositório
cd ~
git clone <repo-url> HashCrackerLab
cd HashCrackerLab

# 2. Tornar script executável
chmod +x setup_arch.sh

# 3. Executar instalação
./setup_arch.sh

# 4. Ativar ambiente Python
source venv/bin/activate

# 5. Validar instalação
python tools/validate_environment.py

# 6. Configurar isolamento de rede (importante!)
sudo ip route del default  # Remove acesso à Internet
ip route  # Verificar que não há rota default
```

**Pós-instalação:**
- Faça logout/login para ativar grupo `wireshark`
- Verifique GPU: `hashcat -I`

---

### VM2: Kali Linux (Ferro - Monitorização + CPU Tester)

```bash
# 1. Clonar repositório
cd ~
git clone <repo-url> HashCrackerLab
cd HashCrackerLab

# 2. Tornar script executável
chmod +x setup_kali.sh

# 3. Executar instalação
./setup_kali.sh

# 4. Ativar ambiente Python
source venv/bin/activate

# 5. Validar instalação
python tools/validate_environment.py

# 6. Configurar isolamento de rede
sudo ip route del default
ip route
```

**Nota:** Kali já vem com muitas ferramentas pré-instaladas.

---

### VM3: Windows + VM Kali (Duarte + Francisco - Comunicação)

```powershell
# 1. Baixar projeto (Git Bash ou download ZIP)
cd C:\Users\<user>
git clone <repo-url> HashCrackerLab
cd HashCrackerLab

# 2. Executar PowerShell como Administrador
# Botão direito > "Executar como Administrador"

# 3. Executar instalação
Set-ExecutionPolicy Bypass -Scope Process
.\setup_windows.ps1

# 4. Fechar e reabrir PowerShell (normal, não admin)

# 5. Ativar ambiente Python
.\venv\Scripts\Activate.ps1

# 6. Validar instalação
python tools/validate_environment.py

# 7. Configurar isolamento de rede
# Painel de Controle > Rede > Propriedades do Adaptador
# Desativar IPv4 Gateway ou desconectar da Internet
```

---

## 🌐 Configuração da Rede LAB

### Passo 1: Configurar Rede LAB (Router)

- Ligar todos os 4 PCs ao **router LAB** (WAN desligada).
- SSID recomendado: `LAB-SERVERS`.
- Não configurar gateway/DNS.

### Passo 2: Atribuir IPs Estáticos

**PC1 (Arch - Orquestrador + GPU):**
```bash
sudo ip addr add 192.168.100.10/24 dev enp0s3
sudo ip link set enp0s3 up
```

**PC2 (Kali - Monitorização + CPU + Antena):**
```bash
sudo ip addr add 192.168.100.20/24 dev eth0
sudo ip link set eth0 up
```

**PC3 (Windows - Comunicação + VM Kali):**
```powershell
# Painel de Controle > Rede > Propriedades IPv4
IP: 192.168.100.30
Máscara: 255.255.255.0
Gateway: (deixar vazio)
```

**PC4 (Windows - Comunicação + VM Kali):**
```powershell
# Painel de Controle > Rede > Propriedades IPv4
IP: 192.168.100.40
Máscara: 255.255.255.0
Gateway: (deixar vazio)
```

### Passo 3: Testar Conectividade

```bash
# Do Orchestrator (VM1)
ping 192.168.100.20  # Kali
ping 192.168.100.30  # Windows

# Verificar isolamento
ping 8.8.8.8  # Deve FALHAR (sem Internet)
```

### Checklist de Prontidão (Antes de Executar)

- Isolamento de rede confirmado (sem rota default)
- Antena RTL8812AU em modo monitor (na VM Kali)
- SSID do AP de teste: LAB-SERVERS (password: Cibersegura)
- Wordlists e regras disponíveis
- Ambiente Python ativo
- Testes unitários a passar

---

## 🚀 Uso Básico

### 1. Validar Ambiente

```bash
# Em todas as VMs
source venv/bin/activate  # ou .\venv\Scripts\Activate.ps1 no Windows
python tools/validate_environment.py
```

### 1.1 Execução Imediata (1 comando)

```bash
python tools/run_immediate.py
```

Se o Hashcat não estiver instalado, a execução passa automaticamente para `--dry-run`.

### 1.2 Testes Unitários

```bash
pytest
```

### 2. Teste Rápido (Orchestrator)

```bash
# Gerar wordlist customizada
python tools/wordlist_generator.py pattern \
  -o wordlists/custom.txt \
  -p "password{}" \
  -n 100

# Executar teste rápido
python orchestrator.py --config config/quick_test.yaml
```

### 3. Teste de Captura de Handshake WiFi (LAB)

**Na máquina Kali (Monitorização):**

```bash
sudo tools/capture_handshake.sh -s "LAB-SERVERS" -i wlan0 -t 60 -d 10
```

**Validação do ficheiro capturado:**

```bash
aircrack-ng captures/handshake_LAB-SERVERS_*.cap
```

### 4. Geração de Tráfego tipo Telnet (LAB)

Este passo cria tráfego de rede autêntico para ser capturado.

**Servidor (ex.: Arch ou Windows #1):**

```bash
python tools/generate_telnet_traffic.py --server --host 0.0.0.0 --port 2323
```

**Cliente (ex.: Windows #2 - Aquele que envia a password):**

```bash
python tools/generate_telnet_traffic.py --client --host <IP_DO_SERVIDOR> --port 2323 \
  --user admin --password sup3rs3cr3t
```

> **Nota:** Use apenas em LAB isolado e com autorização.

### 5. Captura de Credenciais Telnet (Kali + Wireshark)

Uma vez que o Telnet transmite dados em texto claro (cleartext), é possível intercetar as credenciais se estiver na mesma rede (Wi-Fi ou com ARP Spoofing).

**No Kali Linux (Monitorização):**

1. **Abrir Wireshark:**
   ```bash
   sudo wireshark
   ```
2. **Selecionar Interface:** Escolha `wlan0` (se Wi-Fi) ou `eth0` (se cabo/VM).
3. **Filtrar Tráfego:**
   Na barra de topo, escreva:
   ```
   tcp.port == 2323
   ```
4. **Iniciar Captura:** Clique no ícone do tubarão azul.
5. **Gerar Tráfego:** Execute o comando do **Cliente** (Passo 4) no Windows.
6. **Analisar:**
   - Pare a captura (botão vermelho).
   - Clique com o botão direito num pacote (PSH/ACK).
   - Selecione **Follow** > **TCP Stream**.
   - A password aparecerá a vermelho/azul em texto limpo.

### 6. Ver Resultados

```bash
# Navegar até diretório de resultados
cd results/quick_test_<timestamp>/

# Ver relatório
cat REPORT.md

# Ver métricas
cat metrics/metrics.json
```

### 7. Limpeza

```bash
# Limpar resultados
./cleanup.sh

# Ou via Python (com logging)
python orchestrator.py --config config/quick_test.yaml
# (limpeza automática se configurado)
```

---

## 🔬 Uso Avançado

### Experimento Completo

```bash
# 1. Criar configuração customizada
cp config/experiment_example.yaml config/my_experiment.yaml
nano config/my_experiment.yaml  # Editar

# 2. Gerar wordlist com mutações
python tools/wordlist_generator.py pattern \
  -o wordlists/base.txt \
  -p "Test{:04d}" \
  -n 500

python tools/wordlist_generator.py mutate \
  -i wordlists/base.txt \
  -o wordlists/custom_mutated.txt \
  -r upper lower capitalize append_123 append_! leet

# 3. Executar experimento
python orchestrator.py --config config/my_experiment.yaml
```

### Captura WiFi (LAB apenas!)

**Pré-requisitos:**
- Access Point de teste configurado (SSID: LAB-SERVERS, password: Cibersegura)
- Antena WiFi com chipset RTL8812AU (modo monitor)
- Interface WiFi em modo monitor

**Configuração:**
```yaml
# config/wifi_test.yaml
experiment:
  name: "wifi_handshake_test"
  wifi:
    enabled: true
    interface: "wlan0"
    target_ssid: "LAB-SERVERS"
    capture_time: 60
    handshake_output: "captures/handshake.cap"

### Reprodutibilidade

Para resultados determinísticos durante testes (apenas LAB), use:

```yaml
experiment:
  seed: 42
  deterministic_salts: true
```
```

**Execução:**
```bash
# Verificar interface
iwconfig

# Executar captura
sudo python orchestrator.py --config config/wifi_test.yaml

# Verificar handshake capturado
ls -lh captures/
```

### Geração de Tráfego (Windows + VM Kali - LAB)

Use a VM Windows como cliente para gerar tráfego controlado na rede LAB.
Quando necessário, utilize a VM Kali (na mesma máquina) para comunicações
e validação adicional da captura (ex.: sessão Telnet para um servidor de teste dentro do LAB).

### Cracking Distribuído (Em desenvolvimento)

```yaml
cracking:
  workers:
    gpu:
      enabled: true
      host: "192.168.100.10"  # Orchestrator
      device: 0
    cpu:
      enabled: true
      host: "192.168.100.20"  # Kali
      threads: 4
```

---

## 🔧 Troubleshooting

### Hashcat não detecta GPU

```bash
# Verificar drivers
hashcat -I

# Arch: Instalar drivers NVIDIA/AMD
sudo pacman -S nvidia opencl-nvidia  # NVIDIA
sudo pacman -S opencl-mesa           # AMD

# Testar
hashcat -b  # Benchmark
```

### Erro "Permission denied" em captura WiFi

```bash
# Adicionar utilizador ao grupo
sudo usermod -a -G wireshark $USER

# Logout/login

# Verificar
groups
```

### Ambiente Python não ativa

```bash
# Recriar ambiente
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Wordlist não encontrada

```bash
# Verificar caminho
ls -lh wordlists/

# Rockyou no Kali
gunzip -c /usr/share/wordlists/rockyou.txt.gz > wordlists/rockyou.txt

# Criar pequena para testes
head -n 1000 wordlists/rockyou.txt > wordlists/rockyou-small.txt
```

### Rede LAB não comunica

```bash
# Verificar IPs
ip addr show

# Testar ping
ping 192.168.100.10

# Verificar firewall
sudo iptables -L
sudo ufw status  # Se usar UFW
```

---

## ❓ FAQ

### Q: Posso usar em rede com Internet?

**R:** Não! O lab DEVE estar isolado. Remova a rota default:
```bash
sudo ip route del default
```

### Q: Quanto tempo demora um experimento?

**R:** Depende:
- Teste rápido (10 hashes MD5): ~1 minuto
- Teste completo (50x7 algoritmos): ~30-60 minutos
- Bcrypt/Argon2 com custo alto: horas

### Q: Posso pausar uma execução?

**R:** Sim, `Ctrl+C`. Resultados parciais são salvos.

### Q: Como adicionar novo algoritmo?

**R:** Editar [`src/hash_generator.py`](src/hash_generator.py) e adicionar no método `_generate_hash()`.

### Q: Resultados são reprodutíveis?

**R:** Sim! Use o mesmo `seed` no YAML:
```yaml
experiment:
  seed: 42  # Mesmo seed = mesmos hashes
```

### Q: Onde ficam os logs?

**R:** `results/<experimento>/logs/orchestrator.log`

### Q: Como comparar performance entre VMs?

**R:** Execute o mesmo experimento em cada uma e compare as métricas em `metrics/metrics.json`.

---

## 📚 Próximos Passos

1. **Executar teste rápido** em cada VM
2. **Configurar rede LAB** e validar comunicação
3. **Executar experimento completo** no Orchestrator
4. **Analisar métricas** e gerar relatório
5. **Documentar resultados** no relatório final

---

## 🆘 Suporte

**Problemas?**
- Verificar logs: `results/*/logs/orchestrator.log`
- Executar validação: `python tools/validate_environment.py`
- Consultar documentação do Hashcat: `man hashcat`

**Equipa:**
- Henrique Carvalho (Orquestrador - Arch + GPU Tester) - 2024047
- Gonçalo Ferro (Monitorização + CPU Tester) - 2024091
- Duarte Vilar & Francisco Silva (Comunicação - Windows + VM Kali) - 2024187 & 2024095

---

**Data:** Fevereiro 2026
