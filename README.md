<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Hashcat-6.0%2B-red?logo=hack-the-box&logoColor=white" alt="Hashcat">
  <img src="https://img.shields.io/badge/Aircrack--ng-Suite-green?logo=wifi&logoColor=white" alt="Aircrack-ng">
  <img src="https://img.shields.io/badge/Wireshark-Packet%20Analysis-1679A7?logo=wireshark&logoColor=white" alt="Wireshark">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

> Autor: Henrique Carvalho.

# HashCrackerLab

**Plataforma Integrada de Cibersegurança Ofensiva**

Orquestra três vetores de ataque — cracking de hashes (benchmark CPU vs GPU), captura e cracking de handshakes WPA2, e harvesting de credenciais Telnet — em um laboratório de rede isolado, reprodutível e seguro.

> **Projeto Final — Cibersegurança (Fevereiro 2026)**  
> **Autor:** Henrique Carvalho

---

## Sumário

- [Visão Geral](#visão-geral)
- [Diferenciais do Projeto](#diferenciais-do-projeto)
- [Arquitetura e Topologia](#arquitetura-e-topologia)
 - [Saber o Projeto](docs/SABER_O_PROJETO.md)
- [Instalação e Setup](#instalação-e-setup)
- [Utilização](#utilização)
- [Algoritmos e Modos de Ataque](#algoritmos-e-modos-de-ataque)
- [Resultados de Referência](#resultados-de-referência)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Histórico de Desenvolvimento](#histórico-de-desenvolvimento)
- [Troubleshooting](#troubleshooting)
- [Licença](#licença)

---


## Visão Geral

O HashCrackerLab é uma plataforma acadêmica de cibersegurança ofensiva, projetada para experimentação, ensino e demonstração de ataques reais em ambiente controlado. Automatiza todo o ciclo: geração de hashes, ataques multi-dispositivo, coleta de métricas e geração de relatórios, com foco em reprodutibilidade e segurança.

## Diferenciais do Projeto

- **Automação Completa:** Pipeline orquestrado via Python, do início ao fim, sem etapas manuais.
- **Reprodutibilidade Científica:** Seed e salts determinísticos garantem experimentos idênticos.
- **Segurança Operacional:** Isolamento de rede, limpeza segura de dados, anonimização de logs e separação de dados sensíveis.
- **Multi-vetor Integrado:** Ataques coordenados a hashes, WiFi WPA2 e Telnet, com fallback automático.
- **Extensível e Documentado:** Estrutura modular, fácil de adaptar para novos vetores ou algoritmos.

---

---


## Arquitetura e Topologia

```mermaid
graph TB
    subgraph ISOLATED["Rede Isolada — 192.168.100.0/24"]
        direction TB

        ROUTER["<b>Router TP-Link</b><br/>192.168.100.1<br/>SSID: LAB-SERVERS<br/>WPA2-PSK AES"]

        subgraph ATTACK["Vetores de Ataque"]
            ARCH["<b>Arch Linux</b> — Henrique<br/>192.168.100.10<br/>Orchestrator + GPU Cracking<br/>NVIDIA OpenCL"]
            KALI["<b>Kali Linux</b> — Ferro<br/>192.168.100.20<br/>WiFi Monitor Mode<br/>Aircrack-ng Suite"]
        end

        subgraph TELNET_NET["Captura de Tráfego"]
            WIN_SRV["<b>Windows</b> — Francisco<br/>192.168.100.30<br/>Telnet Server + Wireshark"]
            WIN_CLI["<b>Windows</b> — Duarte<br/>192.168.100.40<br/>Telnet Client"]
        end

        ARCH -- "Ethernet" --> ROUTER
        KALI -. "WiFi Monitor Mode" .-> ROUTER
        WIN_SRV -- "WiFi / Ethernet" --> ROUTER
        WIN_CLI -- "WiFi / Ethernet" --> ROUTER
        WIN_CLI -- "TCP/23 Telnet" --> WIN_SRV
    end

    INTERNET["Internet"] -. "Bloqueado — sem rota default" .-> ROUTER
```


### Mapeamento de Portas e Protocolos

| Serviço | Porta | Protocolo | Origem | Destino | Finalidade |
|---------|-------|-----------|--------|---------|------------|
| Telnet | TCP/23 | Telnet (plaintext) | Win Client (.40) | Win Server (.30) | Demonstrar captura de credenciais em texto claro |
| WiFi WPA2 | — | IEEE 802.11 | Kali (.20) | Router (.1) | Captura de 4-way handshake via monitor mode |
| DHCP | UDP/67-68 | DHCP | Router (.1) | Todos | Atribuição automática de IPs (range .100–.200) |
| DNS | — | — | — | — | **Desativado** — rede sem acesso à Internet |

> [!IMPORTANT]
> A rede **não possui rota default**. O `NetworkManager` valida automaticamente que `ip route` não contém `default via` antes de iniciar qualquer experiência com `isolated_network: true`.


### Pipeline de Execução

```mermaid
flowchart LR
    CONFIG["Config YAML"] --> ORCH["Orchestrator"]
    ORCH --> HASHGEN["Hash Generator<br/>MD5 · SHA-256<br/>Bcrypt · Argon2"]
    HASHGEN --> |"N passwords × 4 algos"| CM_GPU["Cracking Manager<br/>GPU -D 2"]
    HASHGEN --> |"N passwords × 4 algos"| CM_CPU["Cracking Manager<br/>CPU -D 1"]
    CM_GPU --> METRICS["Metrics Collector"]
    CM_CPU --> METRICS
    METRICS --> REPORT["REPORT.md + CSV + JSON"]
    ORCH --> CLEANUP["Cleanup Manager<br/>3-pass secure delete"]
```

---


## Instalação e Setup

### Pré-requisitos

| Componente | Versão Mínima | Verificação |
|------------|--------------|-------------|
| Python | 3.10+ | `python --version` |
| Hashcat | 6.0+ | `hashcat --version` |
| Aircrack-ng | 1.7+ | `aircrack-ng --version` |
| Wireshark/tshark | 4.0+ | `wireshark --version` |
| GPU NVIDIA (opcional) | Driver 525+ | `hashcat -I` |
| Adaptador WiFi com monitor mode | — | `iw dev <iface> info` |


### Passo 1 — Clonar o Repositório

```bash
git clone https://github.com/Henryu1781/HashCrackerLab
cd HashCrackerLab
```


### Passo 2 — Setup por Sistema Operacional

**Arch Linux:**
```bash
chmod +x setup_arch.sh && ./setup_arch.sh
source venv/bin/activate
```

**Kali Linux / Debian:**
```bash
chmod +x setup_kali.sh && ./setup_kali.sh
source venv/bin/activate
```

**Windows (PowerShell como Administrador):**
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
.\setup_windows.ps1
.\.venv\Scripts\Activate.ps1
```

> [!IMPORTANT]
> O script de setup cria o virtual environment, instala dependências Python (`requirements.txt`), descarrega a wordlist `rockyou.txt` (14.3M passwords), e copia as regras do Hashcat.


### Passo 3 — Validar Ambiente

```bash
python tools/validate_environment.py
```

---


## Utilização


### Perfis de Configuração

| Config | Passwords | Algoritmos | Ataques | Dispositivos | Tempo |
|--------|-----------|------------|---------|-------------|-------|
| `quick_test.yaml` | 3 | 4 | 1 (dicionário) | GPU | < 30s |
| `apresentacao_final.yaml` | 15 | 4 | 5 (dict, rules, brute, pattern, hybrid) | GPU + CPU | ~3 min |
| `real_world.yaml` | 100 | 4 | 5 | GPU + CPU | ~15 min |


### Execução dos Experimentos

```bash
source venv/bin/activate

# Validação rápida (<30s)
python orchestrator.py --config config/quick_test.yaml

# Experiência completa CPU vs GPU
python orchestrator.py --config config/apresentacao_final.yaml

# Simulação de auditoria real (100 hashes, costs de produção)
python orchestrator.py --config config/real_world.yaml

# Dry-run (validar config sem executar cracking)
python orchestrator.py --config config/apresentacao_final.yaml --dry-run
```


### Ataques WiFi WPA2

```bash
# Scan de redes
python wifi_cracker.py --scan-only --interface wlan00mon

# Captura + cracking automático
python wifi_cracker.py --network "LAB-SERVERS" --interface wlan00mon

# Deauth standalone (forçar reconexão)
python wifi_cracker.py --deauth --network "LAB-SERVERS" --interface wlan00mon

# Crackar handshake existente
python wifi_cracker.py --crack captures/handshake_LAB-SERVERS_*.cap
```


### Captura de Credenciais Telnet

```bash
# Servidor (máquina Francisco)
python telnet_authenticated_traffic.py --server --target 0.0.0.0 --port 23

# Cliente (máquina Duarte)
python telnet_authenticated_traffic.py --target 192.168.100.30 --user admin --password SecurePass123 --verbose
```


### Consulta de Resultados

```bash
LAST=$(ls -td results/*/ | head -1)
cat "$LAST/REPORT.md"                         # Relatório
cat "$LAST/metrics/metrics.json"              # Métricas JSON
cat "$LAST/metrics/metrics_by_algorithm.csv"  # CSV por algoritmo
```

---


## Algoritmos e Modos de Ataque

### Algoritmos de Hashing

| Algoritmo | Hashcat Mode | Tipo | Resistência | Uso Real |
|-----------|-------------|------|-------------|----------|
| **MD5** | 0 / 20 (salted) | Hash simples | Muito baixa | Legado — não usar para passwords |
| **SHA-256** | 1400 / 1420 (salted) | Hash com salt | Baixa | Comum mas inadequado isolado |
| **Bcrypt** | 3200 | Adaptativo (cost factor) | Alta | Standard atual para web apps |
| **Argon2id** | 34000 | Memory-hard | Muito alta | Estado da arte (vencedor PHC 2015) |

### Modos de Ataque

| Modo | Hashcat Flag | Descrição | Keyspace |
|------|-------------|-----------|----------|
| Dicionário | `-a 0` | Wordlist direta (rockyou.txt) | 14.3M |
| Dicionário + Rules | `-a 0 -r best66.rule` | Mutações (P→p, a→@, +123) | ~950M |
| Brute-force PIN | `-a 3 ?d?d?d?d` | Combinações numéricas 0000–9999 | 10K |
| Brute-force Padrão | `-a 3 ?u?l?l?l?d?d` | Maiúscula + 3 min + 2 dígitos | ~11.8M |
| Híbrido | `-a 6 wordlist ?d?d?d` | Wordlist + sufixo 000–999 | ~14.3B |

---


## Resultados de Referência

Configuração `apresentacao_final.yaml` — 15 passwords × 4 algoritmos × 5 modos de ataque:

| Algoritmo | Total | Crackeadas | Taxa | Tempo GPU | Tempo CPU | Speedup |
|-----------|-------|-----------|------|-----------|-----------|---------|
| MD5 | 15 | 10 | 66.7% | 1.8s | 12.0s | 6.7× |
| SHA-256 | 15 | 9 | 60.0% | 4.2s | 28.0s | 6.7× |
| Bcrypt | 15 | 7 | 46.7% | 12.0s | 85.0s | 7.1× |
| Argon2id | 15 | 6 | 40.0% | 28.0s | timeout | >6× |
| **Total** | **60** | **32** | **53.3%** | **~46s** | **>180s** | — |

> [!IMPORTANT]
> As 5 passwords fortes (ex: `X7k#mP9$vL2@`) resistiram a **todos** os 5 modos de ataque em **todos** os 4 algoritmos. Segurança requer **algoritmo forte + password forte** em simultâneo.

---


## Estrutura do Projeto

```
HashCrackerLab/
├── orchestrator.py                  # Motor principal — pipeline completo
├── full_integration_orchestrator.py # Orquestrador multi-vetor (WiFi+Telnet+Hashes)
├── wifi_cracker.py                  # Captura e cracking WPA2
├── telnet_authenticated_traffic.py  # Servidor/cliente Telnet para captura
├── config/
│   ├── quick_test.yaml              # Validação rápida (<30s)
│   ├── apresentacao_final.yaml      # 15 pw × 4 algo × 5 modos (CPU+GPU)
│   └── real_world.yaml              # 100 pw, costs de produção
├── src/
│   ├── hash_generator.py            # Geração determinística (7 algoritmos)
│   ├── cracking_manager.py          # Interface hashcat (dict, brute, hybrid)
│   ├── metrics_collector.py         # Agregação e exportação (CSV/JSON)
│   ├── network_manager.py           # Isolamento de rede + captura WiFi
│   ├── cleanup_manager.py           # 3-pass secure delete + anonimização
│   ├── config_validator.py          # Validação de schema YAML
│   ├── safe_hashes.py               # Separação hashes/passwords
│   └── logger.py                    # Logging centralizado
├── tools/
│   ├── validate_environment.py      # Validação de dependências e hardware
│   └── cleanup.py                   # Limpeza interativa de resultados
├── setup_arch.sh                    # Setup Arch Linux
├── setup_kali.sh                    # Setup Kali/Debian
├── setup_windows.ps1                # Setup Windows
├── wordlists/                       # rockyou.txt + rockyou-small.txt
├── rules/                           # Regras de mutação hashcat
├── results/                         # Relatórios gerados
├── docs/
│   ├── ARCHITECTURE.md              # Arquitetura técnica detalhada
│   └── DEVELOPMENT_TIMELINE.md      # Historial de desenvolvimento
└── requirements.txt                 # Dependências Python
```

---


## Histórico de Desenvolvimento

| Fase | Data | Marco |
|------|------|-------|
| **v0.1 — Fundação** | 2026-02-02 | Estrutura inicial, setup scripts, hash generator, WiFi cracker, Telnet module |
| **v0.2 — Hardening** | 2026-02-06 | Exclusões Windows Defender, validação de ambiente, documentação 4-PC |
| **v0.3 — Integração** | 2026-02-07–08 | Regras hashcat, merge WiFi+Telnet+Hashes, SHA-256 salted, brute-force demo |
| **v0.4 — Apresentação** | 2026-02-09 | 15 passwords × 5 modos, rockyou.txt 14.3M, deauth mode, bug fixes WiFi |

Historial completo: [docs/DEVELOPMENT_TIMELINE.md](docs/DEVELOPMENT_TIMELINE.md)

---


## Troubleshooting

| Problema | Diagnóstico | Solução |
|----------|-------------|---------|
| GPU não detectada | `hashcat -I` | `sudo pacman -S opencl-nvidia` (Arch) |
| WiFi não captura handshake | `iwconfig wlan00mon` | `sudo airmon-ng check kill && sudo airmon-ng start wlan00` |
| Wireshark sem pacotes | Interface errada | Selecionar interface correta + modo promíscuo |
| Import errors Python | Pacote em falta | `pip install -r requirements.txt` |
| Argon2 timeout no CPU | Esperado | Prova que Argon2 neutraliza ataques sem GPU |
| Hashcat erro OpenCL (Win) | Path errado | `$env:HASHCAT_PATH = "C:\hashcat"` |
| Telnet connection refused | Firewall Windows | `netsh advfirewall set allprofiles state off` (temporário) |

---


## Licença

MIT License — ver [LICENSE](LICENSE)
