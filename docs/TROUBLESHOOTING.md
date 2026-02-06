# 🔧 Troubleshooting - Hash Cracker Lab

## Problemas Comuns e Soluções

## ⚖️ Nota de segurança (LAB)

Este guia assume uso educacional em LAB isolado e autorizado. Evite dependências de Internet durante experiências e **não** utilize datasets/leaks reais.

---

## ❌ Erro: `Configuração carregada: ModuleNotFoundError`

**Problema:** Módulo `config_validator` não encontrado

**Solução:**
```bash
# Reinstalar dependências
pip install -r requirements.txt

# Ou reinstalar de zero
rm -rf venv/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ❌ Erro: `FileNotFoundError: hashes.json`

**Problema:** Ficheiro de hashes não existe

**Causas Possíveis:**
1. HashGenerator falhou silenciosamente
2. Diretório de output não tem permissões

**Solução:**
```bash
# Verificar permissões
ls -la results/*/hashes/

# Se vazio, gerar hashes manualmente
python -c "
from src.hash_generator import HashGenerator
from src.logger import setup_logger
from pathlib import Path

logger = setup_logger('Test')
config = {
    'experiment': {
        'hash_generation': {
            'count': 5,
            'algorithms': [{'name': 'md5', 'salt': False}],
            'password_patterns': ['test{}']
        }
    }
}

gen = HashGenerator(config, logger)
hashes = gen.generate_hashes(Path('hashes.json'))
print(f'✓ {len(hashes)} hashes gerados')
"
```

---

## ❌ Erro: `hashcat: not found`

**Problema:** Hashcat não instalado

**Solução:**

### Arch Linux
```bash
sudo pacman -S hashcat
```

### Kali Linux
```bash
sudo apt install hashcat
```

### macOS
```bash
brew install hashcat
```

### Windows
Se o setup do projeto não instalou corretamente, instale e/ou valide:

```powershell
# (1) Confirmar exclusões do Windows Defender (muitos falsos positivos)
.\add_exclusions.ps1

# (2) Re-executar setup
.\setup_windows.ps1

# (3) Validar
python tools/validate_environment.py
```

---

## ❌ Erro: `YAML parsing error`

**Problema:** Ficheiro YAML mal formatado

**Solução:**

Verificar sintaxe YAML online: http://www.yamllint.com/

Ou:
```bash
python -c "import yaml; yaml.safe_load(open('config/quick_test.yaml'))"
```

Se houver erro, será mostrado.

---

## ❌ Erro: `Rede não está isolada`

**Problema:** Rota default para Internet detectada

**Solução (Arch/Kali):**

Verificar rotas:
```bash
ip route
# Deve mostrar apenas rotas locais, SEM "default via"
```

Se houver "default via":
```bash
# Remover rota default (⚠️ cuidado!)
sudo ip route del default

# Ou desabilitar interface de rede
sudo ip link set eth0 down
```

---

## ❌ Erro: `Wordlist not found`

**Problema:** Ficheiro de wordlist não existe

**Solução:**

### Opção 1: Usar wordlist mínima (recomendado)
```bash
python tools/wordlist_generator.py pattern -o wordlists/test.txt -p "test{}" -n 100
```

### Opção 2: Usar a wordlist de teste já incluída

O repositório já inclui `wordlists/rockyou-small.txt` para testes de LAB.

### Opção 3: Gerar wordlist custom (sintética)
```bash
python tools/wordlist_generator.py pattern \
  -o wordlists/custom.txt \
  -p "password{:03d}" \
  -n 1000
```

---

## ❌ Erro: `Permission denied` ao criar diretórios

**Problema:** Sem permissão de escrita

**Solução:**
```bash
# Dar permissões ao utilizador
chmod u+rwx results/ hashes/ logs/ temp/

# Ou mudar dono
sudo chown -R $USER:$USER .

# Ou criar como root (NÃO recomendado)
sudo python orchestrator.py --config config/quick_test.yaml
```

---

## ❌ Erro: `Timeout during cracking`

**Problema:** Hashcat demorou mais que timeout configurado

**Solução:**

### Aumentar timeout em YAML
```yaml
experiment:
  cracking:
    modes:
      - type: dictionary
        wordlist: wordlists/rockyou-small.txt
        max_time: 600  # Aumentar para 600 segundos
```

### Ou reduzir tamanho de teste
```yaml
hash_generation:
  count: 5  # Reduzir número de hashes
```

### Ou usar máquina mais potente
```bash
# Ver status de GPU
hashcat -I

# Se não houver GPU, usar CPU é lento
```

---

## ❌ Erro: `No cracked passwords found`

**Problema:** Nenhuma password foi crackeada

**Causas Possíveis:**
1. Wordlist não contém as passwords
2. Timeout foi atingido
3. Hashcat não conseguiu rodar

**Solução:**

### Verificar configuração
```bash
# Ver hashes gerados
python -c "
import json
with open('results/*/hashes/hashes_safe.json') as f:
    hashes = json.load(f)
    for h in hashes[:3]:
        print(f'{h[\"algorithm\"]}: {h[\"hash\"][:40]}...')
"
```

### Testar hashcat manualmente
```bash
hashcat -m 0 \
  -a 0 \
  --potfile-path=test.pot \
  hashes.txt \
  wordlist.txt
```

### Ver se wordlist tem as passwords
```bash
# Passwords geradas
grep "password" results/*/hashes/.passwords

# Ver wordlist
head wordlists/rockyou-small.txt
```

---

## ❌ Erro: `Cleanup failed`

**Problema:** Script de limpeza não removeu ficheiros

**Solução:**
```bash
# Limpeza manual
rm -rf results/*/hashes/.passwords
rm -rf results/*/hashes/generated_hashes.json
rm -rf results/*/*.pot

# Ou limpeza completa
bash cleanup.sh

# Forçar se bloqueado
sudo rm -rf results/
```

---

## ⚠️ Aviso: `Passwords in plaintext`

**Problema:** Gerador criou ficheiro com passwords visíveis

**Solução:**

Isto é esperado (LAB mode), mas:

1. Nunca commitir `.passwords` em git
2. Deletar após usar:
```bash
rm -f results/*/hashes/.passwords
rm -f results/*/hashes/generated_hashes.json
```

3. Usar versão segura:
```bash
# Usar hashes_safe.json que NÃO tem passwords
cat results/*/hashes/hashes_safe.json | head
```

---

## ⚠️ Aviso: `GPU not detected`

**Problema:** Hashcat não encontrou GPU

**Solução:**

### Verificar GPU
```bash
hashcat -I

# Deve mostrar OpenCL devices ou CUDA devices
```

### Se não houver GPU
```bash
# Usar CPU (mais lento, mas funciona)
# Configurar timeout maior em YAML
```

### Instalar drivers GPU

**NVIDIA:**
```bash
# Arch
sudo pacman -S nvidia nvidia-utils

# Ubuntu/Debian
sudo apt install nvidia-driver-XXX

# Depois
nvidia-smi  # Verificar
```

**AMD:**
```bash
# Arch
sudo pacman -S opencl-mesa

# Ubuntu/Debian
sudo apt install opencl-amd
```

---

## 🐛 Debug Mode

### Ativar logs DEBUG

```bash
# Editar orchestrator.py
# Mudar: console_level=logging.INFO
#     → console_level=logging.DEBUG

# Ou via environment
export LOG_LEVEL=DEBUG
python orchestrator.py --config config/quick_test.yaml
```

### Ver logs em tempo real

```bash
# Terminal 1
tail -f results/*/logs/orchestrator.log

# Terminal 2
python orchestrator.py --config config/quick_test.yaml
```

### Dry-run para validação

```bash
# Não executa cracking, apenas valida
python orchestrator.py --config config/quick_test.yaml --dry-run
```

---

## 📊 Validação de Entrada

### Verificar Configuração

```bash
python -c "
from src.config_validator import ConfigValidator
from pathlib import Path

config, errors = ConfigValidator.load_and_validate(Path('config/quick_test.yaml'))

if errors:
    print('Erros:')
    for error in errors:
        print(f'  ❌ {error}')
else:
    print('✅ Configuração válida')
    print(f'Nome: {config[\"experiment\"][\"name\"]}')
    print(f'Hashes: {config[\"experiment\"][\"hash_generation\"][\"count\"]}')
"
```

### Validar YAML com Schema

```bash
# Instalar jsonschema
pip install jsonschema

# Usar em Python
python -c "
import json
from jsonschema import validate

# Ver schema em src/config_validator.py
"
```

---

## 📈 Performance

### Slow Cracking?

```bash
# Ver se GPU está sendo usada
hashcat -I

# Se não, especificar em YAML
# (atualmente auto-detecta)
```

### Muita memória?

```bash
# Reduzir número de hashes
hash_generation:
  count: 10  # Reduzir

# Ou usar dry-run
python orchestrator.py --config config/quick_test.yaml --dry-run
```

### Limpeza lenta?

A sobrescrita de 3 passes é lenta. Para acelerar:

```python
# Em cleanup_manager.py, reduzir passes:
# f.write(b'\x00' * file_size)  # Pass 1
# f.write(b'\xff' * file_size)  # Pass 2
# # Remover pass 3 para acelerar
```

---

## 🆘 Suporte

Se o problema persiste:

1. **Ler logs completos:**
```bash
cat results/*/logs/orchestrator.log | tail -100
```

2. **Executar testes:**
```bash
pytest -v

# Ou teste simples
python simple_test.py
```

3. **Validar ambiente:**
```bash
python tools/validate_environment.py
```

4. **Procurar em issues:**
https://github.com/Henryu1781/HashCrackerLab/issues

---

**Última Atualização:** Fevereiro 2026
