# 🚀 REFERÊNCIA RÁPIDA - HashCrackerLab

## ⚡ Comandos Essenciais

### Inicialização
```bash
cd ~/Projects/HashCrackerLab
source venv/bin/activate
```

### Demo Simples (1 minuto) ⭐
```bash
python orchestrator.py --config config/advanced_encryption_test.yaml
```

### Teste Rápido (30 segundos)
```bash
python orchestrator.py --config config/quick_test.yaml
```

### Validação do Sistema
```bash
python tools/validate_environment.py
```

---

## 📊 Resultados Esperados

**Taxa de Sucesso:** 80% (16/20 hashes)

**Passwords Crackeadas:**
- `123456`
- `password`
- `qwerty`
- `letmein`

**Benchmark GPU vs CPU:**
- MD5: **16.5x** mais rápido
- SHA-256: **9.9x** mais rápido
- Bcrypt: **5.2x** mais rápido

---

## 📂 Ficheiros Importantes

**Para Executar:**
- `orchestrator.py` - Script principal
- `config/advanced_encryption_test.yaml` - Config recomendada

**Documentação:**
- `README.md` - Documentação completa
- `GUIA_EXECUCAO.md` - Passo-a-passo detalhado
- `SUMARIO_EXECUTIVO.md` - Resumo do projeto

**Resultados:**
```bash
results/[experimento]_[timestamp]/
├── REPORT.md
├── cracked/*.pot
├── metrics/*.csv
└── logs/orchestrator.log
```

---

## 🛠️ Troubleshooting 1-Linha

**"ModuleNotFoundError: yaml"**
```bash
pip install -r requirements.txt
```

**"Hashcat not found"**
```bash
sudo pacman -S hashcat
```

**"GPU not detected"**
```bash
hashcat -I
```

---

## 🎯 Configurações

| Config | Hashes | Tempo | Uso |
|--------|--------|-------|-----|
| `quick_test.yaml` | 10 | 30s | Validação |
| `advanced_encryption_test.yaml` | 20 | 1min | **Demo ⭐** |
| `projeto_final_ciberseguranca.yaml` | Variável | 3-5min | Apresentação completa |

---

## 📞 Em Caso de Problema

```bash
# Ver logs
cat results/*/logs/orchestrator.log

# Limpar e recomeçar
rm -rf results/*
python orchestrator.py --config config/quick_test.yaml
```

---

**Última atualização:** 9 Fevereiro 2026
