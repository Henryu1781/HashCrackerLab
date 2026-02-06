# 🏗️ Arquitetura e Configuração - Hash Cracker Lab

## Como usar este documento

1. Se quer apenas executar o LAB: comece por `QUICKSTART.md` e `docs/EXECUTION_GUIDE.md`.
2. Se quer entender o código/config: veja as secções **Sistema de Configuração** e **Fluxo de Dados**.
3. Se está a mexer em dados sensíveis: leia `docs/SECURITY_GUIDE.md`.

## Estrutura de Módulos

```
src/
├── __init__.py
├── logger.py                    # Logging centralizado
├── config_validator.py          # Validação de configuração YAML
├── safe_hashes.py              # Gestão segura de hashes/passwords
├── hash_generator.py           # Geração de hashes
├── cracking_manager.py         # Execução de cracking
├── metrics_collector.py        # Coleta de métricas
├── network_manager.py          # Gestor de rede/WiFi
└── cleanup_manager.py          # Limpeza de dados sensíveis
```

---

## 🔧 Sistema de Configuração

### Validação de YAML

Usar `ConfigValidator` para carregar e validar:

```python
from src.config_validator import ConfigValidator

config, errors = ConfigValidator.load_and_validate(Path('config/quick_test.yaml'))

if errors:
    print(f"Erros: {errors}")
else:
    config = ConfigValidator.apply_defaults(config)
    # ... usar config
```

### Estrutura de Configuração

**Obrigatório:**
```yaml
experiment:
  name: "meu_teste"
  hash_generation:
    count: 10
    algorithms:
      - {name: md5, salt: false}
      - {name: sha256, salt: true}
    password_patterns:
      - "password{}"
      - "test{}"
  cracking:
    modes:
      - {type: dictionary, wordlist: wordlists/rockyou-small.txt}
```

**Opcional (com defaults):**
```yaml
experiment:
  seed: 42                        # Para reprodutibilidade
  deterministic_salts: true       # Salts determinísticos
  
  output:
    base_dir: "results/{experiment_name}_{timestamp}"
  
  security:
    isolated_network: false       # Verificar isolamento
    auto_cleanup: true            # Limpar após experiência
    cleanup_delay: 10             # Delay em segundos
  
  wifi:
    enabled: false
    interface: wlan0
    target_ssid: "LAB-WiFi"
    target_bssid: "00:11:22:33:44:55"
    capture_time: 60
```

---

## 📊 Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────┐
│ orchestrator.py (Orquestrador Principal)                    │
└────────────────┬────────────────────────────────────────────┘
                 │
        ┌────────┼────────┐
        │        │        │
        ▼        ▼        ▼
   [1] config  [2] log   [3] validate
   loader      setup     config
        │        │        │
        └────────┼────────┘
                 │
        ┌────────▼────────┐
        │  HashGenerator  │ ──► hashes_safe.json (seguro)
        │                 │ ──► .passwords (DELETE!)
        │ (7 algoritmos)  │ ──► *_hashes.txt (for hashcat)
        └────────┬────────┘
                 │
        ┌────────▼──────────────┐
        │  CrackingManager      │
        │  - Dictionary attack  │ ──► results.pot
        │  - Brute-force        │ ──► metrics.json
        └────────┬──────────────┘
                 │
        ┌────────▼────────┐
        │ MetricsCollector│ ──► CSV, JSON, Report
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │ CleanupManager  │
        │ - Remove sensíveis
        │ - Anonimizar logs ──► CLEANUP_REPORT.json
        │ - Sobrescrever
        └─────────────────┘
```

---

## 🔐 Gestão de Dados Sensíveis

### Fluxo de Segurança

```
1. HashGenerator.generate_hashes()
   ├─ Cria: generated_hashes.json (⚠️ com passwords)
   └─ Salva em output_dir/hashes/

2. SafeHashesManager.create_safe_version()
   ├─ Remove passwords
   └─ Salva: hashes_safe.json ✅

3. SafeHashesManager.create_password_file()
   ├─ Extrai passwords
   ├─ Salva: .passwords (chmod 600)
   └─ Aviso: DELETE APÓS USAR

4. CleanupManager.cleanup()
   ├─ Remove generated_hashes.json
   ├─ Remove .passwords
   ├─ Anonimiza logs
   └─ Cria CLEANUP_REPORT.json
```

---

## 📝 Logging Centralizado

### Setup

```python
from src.logger import setup_logger

logger = setup_logger(
    'ModuleName',
    log_file=Path('logs/module.log'),
    level=logging.DEBUG,
    console_level=logging.INFO
)

logger.info("Mensagem")
logger.warning("Aviso")
logger.error("Erro")
```

### Output

```
2026-02-02 14:30:45 - ModuleName - INFO - Mensagem
2026-02-02 14:30:46 - ModuleName - WARNING - Aviso
2026-02-02 14:30:47 - ModuleName - ERROR - Erro
```

---

## 🧪 Exemplos de Uso

### Carregar Configuração com Validação

```python
from src.config_validator import ConfigValidator
from pathlib import Path

config, errors = ConfigValidator.load_and_validate(
    Path('config/quick_test.yaml')
)

if errors:
    for error in errors:
        print(f"❌ {error}")
    exit(1)

config = ConfigValidator.apply_defaults(config)
print(f"✅ Configuração válida")
```

### Criar Versão Segura de Hashes

```python
from src.safe_hashes import SafeHashesManager
import json

# Carregar hashes com passwords
with open('results/hashes/generated_hashes.json', 'r') as f:
    hashes = json.load(f)

# Criar versão segura
count = SafeHashesManager.create_safe_version(
    hashes,
    Path('results/hashes/hashes_safe.json')
)

print(f"✅ {count} hashes salvos (sem passwords)")
```

### Logging em Múltiplos Módulos

```python
# Em cada módulo:
from src.logger import setup_logger

logger = setup_logger('MeuModulo')

class MeuModulo:
    def __init__(self):
        self.logger = logger
    
    def processar(self):
        self.logger.info("Iniciando processamento...")
```

---

## 🔄 Ciclo de Vida da Experiência

```
1. LOAD
   └─ ConfigValidator.load_and_validate()
   └─ ConfigValidator.apply_defaults()

2. SETUP
   └─ Setup logging
   └─ Criar diretórios de output

3. EXECUTE
   ├─ HashGenerator.generate_hashes()
   │  ├─ SafeHashesManager.create_safe_version()
   │  └─ SafeHashesManager.create_password_file()
   │
   ├─ CrackingManager.run_cracking()
   │  └─ Salvar potfiles únicos por (algo + modo)
   │
   ├─ MetricsCollector.collect_metrics()
   │  └─ Exportar JSON/CSV/Report
   │
   └─ NetworkManager.verify_isolation() (opcional)

4. CLEANUP
   └─ CleanupManager.cleanup()
      ├─ Remover passwords
      ├─ Anonimizar logs
      ├─ Sobrescrever ficheiros
      └─ Criar CLEANUP_REPORT.json
```

---

## 📊 Schema de Configuração

```yaml
# Estrutura completa esperada
experiment:
  # Obrigatório
  name: string
  
  # Hash generation
  hash_generation:
    count: int >= 1
    algorithms:
      - name: string (md5|sha1|sha256|bcrypt|scrypt|pbkdf2_sha256|argon2)
        salt: boolean (optional)
        cost: int (optional, para bcrypt/argon2)
        iterations: int (optional, para pbkdf2/argon2)
    password_patterns: list[string]
  
  # Cracking modes
  cracking:
    modes:
      - type: string (dictionary|brute-force)
        wordlist: string (opcional, para dictionary)
        mask: string (opcional, para brute-force)
        max_time: int (segundos)
  
  # Opcional
  seed: int (para reprodutibilidade)
  deterministic_salts: boolean
  
  output:
    base_dir: string (template com {experiment_name}, {timestamp})
  
  security:
    isolated_network: boolean
    auto_cleanup: boolean
    cleanup_delay: int (segundos)
  
  wifi:
    enabled: boolean
    interface: string
    target_ssid: string
    target_bssid: string (MAC address)
    capture_time: int (segundos)
```

---

## 🚀 Performance

### Otimizações Implementadas

1. **Potfiles Únicos**: Cada (algoritmo + modo) tem seu próprio potfile
2. **Logging Async**: FileHandler não bloqueia
3. **Generators**: Hashes processados em memoria

### Bottlenecks Conhecidos

- **Hashcat I/O**: Dependente do armazenamento
- **Network isolation check**: `ip route` é lento em Linux
- **Cleanup sobrescrita**: 3 passes de sobrescrita são lentos

---

## 📈 Monitoramento

Ver logs em tempo real:

```bash
# Logs do orquestrador
tail -f results/experiment_*/logs/orchestrator.log

# Todos os logs
tail -f results/experiment_*/logs/*.log
```

Ver métricas:

```bash
# JSON
cat results/experiment_*/metrics/metrics.json | jq '.success_rate'

# CSV
cat results/experiment_*/metrics/metrics_by_algorithm.csv
```

---

**Última Atualização:** Fevereiro 2026
