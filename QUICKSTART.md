# Hash Cracker Lab - Quick Start 🚀

## Instalação Rápida

### Arch Linux (Henrique)
```bash
chmod +x setup_arch.sh
./setup_arch.sh
source venv/bin/activate
python tools/validate_environment.py
```

### Kali Linux (Ferro - Monitorização + CPU Tester)
```bash
chmod +x setup_kali.sh
./setup_kali.sh
source venv/bin/activate
python tools/validate_environment.py
```

### Windows + VM Kali (Duarte + Francisco - Comunicação)
```powershell
# Como Administrador
.\setup_windows.ps1

# Depois, normal:
.\venv\Scripts\Activate.ps1
python tools/validate_environment.py
```

## Execução Imediata (1 comando)

```bash
python tools/run_immediate.py
```

Se o Hashcat não estiver instalado, a execução passa automaticamente para `--dry-run`.

## Teste Rápido

```bash
# 1. Ativar ambiente
source venv/bin/activate  # ou .\venv\Scripts\Activate.ps1

# 2. Executar teste
python orchestrator.py --config config/quick_test.yaml

# 3. Ver resultados
cd results/quick_test_*/
cat REPORT.md
```

## Testes LAB (WiFi + Tráfego)

### Captura de Handshake (Kali)
```bash
sudo tools/capture_handshake.sh -s "LAB-SERVERS" -i wlan0 -t 60 -d 10
```

### Tráfego tipo Telnet (Windows/Arch)
Servidor:
```bash
python tools/generate_telnet_traffic.py --server --host 0.0.0.0 --port 2323
```
Cliente:
```bash
python tools/generate_telnet_traffic.py --client --host 192.168.100.10 --port 2323 --user labuser --password labpass
```

## Testes Unitários

```bash
pytest
```

## Reprodutibilidade

Em configs YAML, defina `seed` e `deterministic_salts: true` para resultados determinísticos.

## Estrutura do Projeto

```
HashCrackerLab/
├── orchestrator.py          # Orquestrador principal
├── setup_arch.sh            # Setup para Arch Linux
├── setup_kali.sh            # Setup para Kali Linux
├── setup_windows.ps1        # Setup para Windows
├── cleanup.sh               # Script de limpeza
├── requirements.txt         # Dependências Python
├── README.md                # Este ficheiro
├── TUTORIAL.md              # Tutorial completo
│
├── src/                     # Código fonte
│   ├── hash_generator.py    # Gerador de hashes
│   ├── cracking_manager.py  # Gestor de cracking
│   ├── metrics_collector.py # Coletor de métricas
│   ├── network_manager.py   # Gestor de rede/WiFi
│   └── cleanup_manager.py   # Gestor de limpeza
│
├── config/                  # Configurações YAML
│   ├── experiment_example.yaml
│   ├── quick_test.yaml
│   └── full_test.yaml
│
├── tools/                   # Ferramentas auxiliares
│   ├── wordlist_generator.py
│   └── validate_environment.py
│
├── wordlists/               # Wordlists (criado no setup)
├── rules/                   # Regras Hashcat (criado no setup)
├── captures/                # Capturas WiFi (criado no setup)
├── results/                 # Resultados (criado no setup)
├── hashes/                  # Hashes temporários (criado no setup)
└── logs/                    # Logs (criado no setup)
```

## Comandos Essenciais

### Gerar Wordlists
```bash
# Padrão simples
python tools/wordlist_generator.py pattern \
  -o wordlists/custom.txt \
  -p "password{}" \
  -n 100

# Com mutações
python tools/wordlist_generator.py mutate \
  -i wordlists/custom.txt \
  -o wordlists/custom_mutated.txt \
  -r upper lower append_123 leet
```

### Executar Experimentos
```bash
# Teste rápido
python orchestrator.py --config config/quick_test.yaml

# Teste completo
python orchestrator.py --config config/full_test.yaml

# Configuração customizada
python orchestrator.py --config config/my_config.yaml
```

### Validação
```bash
# Validar ambiente
python tools/validate_environment.py

# Verificar GPU
hashcat -I

# Verificar isolamento de rede
ip route  # Não deve ter "default via"
ping 8.8.8.8  # Deve falhar
```

### Limpeza
```bash
# Limpeza completa
./cleanup.sh

# Ou manualmente
rm -rf results/* hashes/* captures/* logs/* temp/*
```

## Configuração de Rede LAB

### IPs Estáticos

| VM | Role | OS | IP |
|----|------|----|----|
| VM1 | Orchestrator + GPU Tester | Arch Linux | 192.168.100.10 |
| VM2 | Monitorização + CPU Tester | Kali Linux | 192.168.100.20 |
| VM3 | Comunicação | Windows + VM Kali | 192.168.100.30 |

### Configurar Isolamento

**Linux:**
```bash
sudo ip route del default
ip route  # Verificar
```

**Windows:**
```
Painel de Controle > Rede > Propriedades IPv4
Gateway: (deixar vazio)
```

## Exemplos de Uso

### 1. Comparar Algoritmos
```yaml
# config/algo_comparison.yaml
hash_generation:
  count: 50
  algorithms:
    - name: "md5"
    - name: "sha256"
    - name: "bcrypt"
      cost: 10
    - name: "argon2"
      cost: 16
```

### 2. Testar Wordlists
```yaml
cracking:
  modes:
    - type: "dictionary"
      wordlist: "wordlists/rockyou-small.txt"
    - type: "dictionary"
      wordlist: "wordlists/custom_mutated.txt"
```

### 3. Benchmark GPU vs CPU
```yaml
workers:
  gpu:
    enabled: true
    host: "192.168.100.10"
  cpu:
    enabled: true
    host: "192.168.100.20"
```

## Métricas Disponíveis

Após cada experimento, acesse:

- **JSON:** `results/*/metrics/metrics.json`
- **CSV:** `results/*/metrics/metrics_by_algorithm.csv`
- **Relatório:** `results/*/REPORT.md`
- **Logs:** `results/*/logs/orchestrator.log`

## Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| GPU não detectada | `hashcat -I` e instalar drivers |
| Wordlist não encontrada | Verificar caminho em `wordlists/` |
| Erro de permissão WiFi | `sudo usermod -a -G wireshark $USER` |
| Ambiente Python | `rm -rf venv && python3 -m venv venv` |
| Rede não comunica | Verificar IPs e firewall |

## Documentação Completa

📖 Ver [`TUTORIAL.md`](TUTORIAL.md) para documentação completa com:
- Instalação detalhada por OS
- Configuração de rede passo-a-passo
- Uso avançado
- FAQ completo
- Troubleshooting extensivo

## Equipa

- **Henrique Carvalho** (2024047) - Orquestrador (Arch) + GPU Tester
- **Gonçalo Ferro** (2024091) - Monitorização (Kali) + CPU Tester
- **Duarte Vilar** (2024187) - Comunicação (Windows + VM Kali)
- **Francisco Silva** (2024095) - Comunicação (Windows + VM Kali)

---

**Projeto Final - Hash Cracker Lab**  
**Data:** Fevereiro 2026

