# 🔒 Guia de Segurança - Hash Cracker Lab

## ⚠️ Dados Sensíveis

Este projeto maneja dados sensíveis (passwords em plaintext durante testes). Esta é uma solução educacional para LAB ISOLADO apenas.

---

## 📁 Estrutura de Ficheiros de Segurança

### Ficheiros Sensíveis Gerados

```
results/experiment_TIMESTAMP/
├── hashes/
│   ├── generated_hashes.json      ⚠️ CONTÉM PASSWORDS EM PLAINTEXT
│   ├── hashes_safe.json           ✅ SEM PASSWORDS (USE ISTO)
│   ├── .passwords                 ⚠️ PASSWORDS SEPARADAS (DELETE APÓS USAR)
│   ├── md5_hashes.txt             ✅ Apenas hashes para hashcat
│   ├── sha256_hashes.txt          ✅ Apenas hashes para hashcat
│   └── ...
└── ...
```

---

## 🔐 Boas Práticas

### 1. **NÃO Usar `generated_hashes.json` em Produção**

O ficheiro contém passwords em plaintext:
```json
{
  "password": "password000",  // ⚠️ SENSÍVEL!
  "hash": "5f4dcc3b5aa765d61d8327deb882cf99"
}
```

**Solução:** Use `hashes_safe.json` que remove todas as passwords.

### 2. **Deletar `.passwords` Imediatamente**

O ficheiro `.passwords` é criado apenas para validação:
```bash
# Após validação, deletar:
rm -f results/*/hashes/.passwords

# Ou usar cleanup automático:
bash cleanup.sh
```

### 3. **Nunca Commitir Passwords em Git**

Já está no `.gitignore`:
```gitignore
results/
hashes/
*.pot
.passwords
```

Verificar:
```bash
git grep -i "password" -- '*.json' '*.py'  # Não deve encontrar
```

### 4. **Criptografar Passwords se Necessário**

Para armazenamento de longa duração:
```python
from src.safe_hashes import SafeHashesManager

SafeHashesManager.create_password_file(
    hashes,
    Path('results/hashes/.passwords'),
    encrypt=True,
    encryption_key='sua-chave-secreta'
)
```

---

## 🧹 Limpeza Automática

Usar o cleanup manager para remover dados sensíveis:

```python
# Em YAML (orchestrator):
experiment:
  security:
    auto_cleanup: true
    cleanup_delay: 0  # Delay em segundos antes de limpar
```

Ou executar manualmente:
```bash
bash cleanup.sh
```

O script:
- ✅ Remove passwords sensíveis
- ✅ Anonimiza IPs e MACs em logs
- ✅ Sobrescreve com random (3 passes)
- ✅ Cria relatório de auditoria

---

## 🔍 Validação de Segurança

### 1. Verificar Passwords Não Vazam

```bash
# Procurar por passwords em logs
grep -r "password" results/*/logs/

# Procurar por IPs privados em resultados
grep -r "192.168\|10.0\|172.1[6-9]" results/*/
```

### 2. Verificar Integridade de Limpeza

```bash
# Ver relatório de cleanup
cat CLEANUP_*.txt

# Verificar se ficheiros foram removidos
find results/ -name "*.passwords" -o -name "*generated_hashes.json"  # Não deve encontrar nada
```

### 3. Auditoria de Ficheiros

```bash
# Ver o que foi limpo
ls -la results/*/CLEANUP_REPORT.json
cat results/*/CLEANUP_REPORT.json | jq '.actions | length'
```

---

## 🌐 Isolamento de Rede

Para LAB seguro, garantir isolamento:

### Verificar Isolamento (Linux/Mac)

```bash
# Ver rotas
ip route

# Se houver "default via", a rede NÃO está isolada
sudo ip route del default  # Remover rota de Internet (⚠️ cuidado!)

# Verificar com orchestrator
python orchestrator.py --config config/quick_test.yaml
# [1/6] Verificando isolamento de rede...
# ✓ Nenhuma rota default - rede isolada
```

### Verificar Isolamento (Windows)

```powershell
# Ver rotas
route print

# Ver apenas default gateway
route print | findstr "0.0.0.0"
```

---

## 📋 Checklist de Segurança

- [ ] Projeto guardado em partition criptografada (LAB)
- [ ] Rede isolada (sem acesso à Internet)
- [ ] `auto_cleanup: true` em configuração
- [ ] Nenhum `.passwords` ou `generated_hashes.json` commitido em git
- [ ] Dados removidos com `cleanup.sh` antes de desligar VM
- [ ] Relatório de cleanup (`CLEANUP_*.txt`) verificado
- [ ] Nenhuma password visível em logs
- [ ] Nenhuma IP privada em relatórios públicos

---

## 🚨 Casos de Emergência

### Esqueceu de Limpar Dados

```bash
# Limpeza de emergência
bash cleanup.sh

# Remover todos os resultados
rm -rf results/
rm -rf hashes/
rm -rf captures/
rm -rf logs/

# Resetar git (se commitiu por erro)
git reset --hard HEAD~1
git push --force  # ⚠️ Cuidado!
```

### Detectou Password em Git

```bash
# Ver commit com password
git log -p --all | grep -i password

# Remover de histórico (BFG Repo-Cleaner)
brew install bfg
bfg --delete-files .passwords repo.git

# Ou recriar repo
git reset --hard
rm -rf .git
git init
git add .
git commit -m "Initial commit"
```

---

## 📚 Referências

- [OWASP - Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [CWE-256: Cleartext Storage of Password](https://cwe.mitre.org/data/definitions/256.html)
- [Git - Removing Sensitive Data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

---

**Última Atualização:** Fevereiro 2026

⚠️ **LEMBRETE:** Este é um LAB educacional. NUNCA usar em produção ou com dados reais!
