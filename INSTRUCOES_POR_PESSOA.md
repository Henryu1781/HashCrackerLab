# 👥 GUIA DE INSTRUÇÕES POR EQUIPA

Este documento define exatamente quem faz o quê durante a apresentação.

---

## 🔵 HENRIQUE (ARCH LINUX - ORCHESTRATOR)
**Função:** Líder da Demo, GPU Cracking e Coordenação.
**Máquina:** Arch Linux (GPU NVIDIA)

### 1. Preparação (Antes da Demo)
```bash
# Navegar para a pasta e ativar ambiente
cd ~/HashCrackerLab
source venv/bin/activate

# Verificar se a GPU está detetada
hashcat -I

# Validar ambiente
python tools/validate_environment.py
```

### 2. Executar o Orquestrador (Mestre)
O Henrique comanda o fluxo. Ele dirá aos outros quando atuar.
```bash
python full_integration_orchestrator.py --mode lab
```
*Este script vai pausar e pedir confirmação para avançar nas fases.*

### 3. Fase de Cracking (GPU)
Quando chegar à fase de Hash Cracking, o script pode rodar automaticamente, ou se preferires rodar isolado:
```bash
python orchestrator.py --config config/projeto_final_ciberseguranca.yaml
```

---

## 🟡 FERRO (KALI LINUX - WIFI OPS)
**Função:** Ataque à Rede WiFi (Packet Injection).
**Máquina:** Kali Linux (Wordlist + Antena WiFi)

### 1. Preparação
```bash
# Verificar interface
iwconfig
# (Deve ver wlan0 ou similar)

# Matar processos que interferem
sudo airmon-ng check kill
```

### 2. Ataque (Quando o Henrique der o sinal)
O alvo é a rede `LAB-SERVERS`. O Ferro vai injetar pacotes para forçar o handshake.
```bash
# 1. Iniciar Monitor Mode
sudo airmon-ng start wlan0

# 2. Iniciar o Cracker (Automático: Scan -> Deauth -> Crack)
python wifi_cracker.py --network "LAB-SERVERS" --monitor wlan0mon
```
*Sucesso esperado: "KEY FOUND! [ Cibersegura ]"*

---

## 🟢 DUARTE (WINDOWS - TELNET TRAFFIC)
**Função:** Gerar tráfego vulnerável na rede.
**Máquina:** Windows (PowerShell)

### 1. Preparação
```powershell
# Ativar venv
.\venv\Scripts\Activate.ps1
```

### 2. Ação (Quando o Henrique/Francisco pedir)
O Duarte vai simular um login inseguro via Telnet.
```powershell
# Enviar credenciais em texto claro repetidamente
python telnet_authenticated_traffic.py --target 192.168.100.255 --user duarte --password Cibersegura --hash-algo plaintext --count 20
```
*Nota: O target pode ser o IP do Francisco ou Broadcast, o importante é que passe na rede.*

---

## 🟣 FRANCISCO (WINDOWS - ANALISTA)
**Função:** Intercetar e validar a captura de credenciais.
**Máquina:** Windows (Wireshark instalado)

### 1. Preparação
- Abrir **Wireshark**.
- Selecionar a interface de rede principal (Ethernet/WiFi).

### 2. Ação de Captura
- Aplicar o filtro: `tcp.port == 23` (Telnet).
- Avisar o Duarte: "Podes enviar o tráfego".
- **Observar:** Deverá aparecer pacotes "Telnet Data".
- **Demonstrar:** Clicar num pacote -> "Follow TCP Stream" -> Mostrar a password `Cibersegura` em vermelho (texto claro).

---

## 🆘 TROUBLESHOOTING RÁPIDO

**Henrique (Arch):**
- *Erro:* "No opencl devices found" -> Verifica se instalaste `cuda` e `hashcat`.
- *Fix:* `sudo pacman -S cuda hashcat`

**Ferro (Kali):**
- *Erro:* "wlan0mon not found" -> Corre `sudo airmon-ng start wlan0` novamente.
- *Erro:* "No handshake" -> Aproxima-te do router ou tenta de novo (o script faz deauth automático).

**Duarte/Francisco (Windows):**
- *Erro:* "Script execution disabled" -> `Set-ExecutionPolicy -Scope Process Unrestricted`.
- *Erro:* Python não reconhecido -> Verifica se ativaste o `.venv`.
