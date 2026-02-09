# 📘 Guia de Execução do Lab - Passo a Passo

## ⏱️ Tempo Total Estimado: 15-20 minutos

---

## 🎬 Opção 1: Demo Simples (Recomendado para Apresentação)

### **Apenas Henrique precisa executar**

Esta é a **forma mais rápida e simples** de demonstrar todas as capacidades do lab.

#### Passo 1: Preparação (2 minutos)
```bash
cd ~/Projects/HashCrackerLab
source venv/bin/activate

# Verificar se tudo está OK
python tools/validate_environment.py
```

**Saída esperada:**
```
✓ Python version: 3.14.2
✓ Hashcat installed: v7.1.2
✓ All dependencies OK
```

#### Passo 2: Execução da Demo (1 minuto de setup + ~1 minuto de cracking)
```bash
python orchestrator.py --config config/advanced_encryption_test.yaml
```

**O que vai acontecer:**
1. **Geração de Hashes** (~5 segundos)
   - Cria 20 hashes com 4 algoritmos diferentes:
     - 5 Bcrypt (custo 5)
     - 5 Argon2 (memory-hard)
     - 5 MD5 (rápido)
     - 5 SHA-256 (com salt)

2. **Cracking com GPU** (~15 segundos)
   - Ataque de dicionário contra todos os hashes
   - Mostra progresso em tempo real

3. **Demo Visual de Força Bruta** (~1 segundo)
   - Simulação de PIN cracking (0000-9999)
   - Mostra conceito de tentativa e erro

4. **Benchmark GPU vs CPU** (~10 segundos)
   - Compara velocidade de 3 algoritmos
   - Mostra vantagem da GPU

**Resultados Típicos:**
```
============================================================
RESUMO DE RESULTADOS
============================================================

Total de hashes: 20
Hashes crackeadas: 16
Taxa de sucesso: 80.00%

Por Algoritmo:
+-------------+---------+--------------+--------+
| Algoritmo   |   Total |   Crackeados | Taxa   |
+=============+=========+==============+========+
| bcrypt      |       5 |            4 | 80.00% |
| argon2      |       5 |            4 | 80.00% |
| md5         |       5 |            4 | 80.00% |
| sha256      |       5 |            4 | 80.00% |
+-------------+---------+--------------+--------+

Benchmark CPU vs GPU:
- MD5: GPU é 16.5x mais rápido
- SHA-256: GPU é 9.9x mais rápido  
- Bcrypt: GPU é 5.2x mais rápido
```

#### Passo 3: Análise dos Resultados (2 minutos)
```bash
# Ver pasta de resultados criada
ls -lh results/

# Ver relatório completo
cat results/advanced_crypto_test_*/REPORT.md

# Ver passwords crackeadas (Bcrypt)
cat results/advanced_crypto_test_*/cracked/bcrypt/cracked_bcrypt_dictionary.pot
```

**Exemplo de passwords crackeadas:**
```
$2b$05$/CASo.Yu9/IyfwpRJ1fLXeFaT7uL1pWcs/cC.YLe1V8Pr5m2/tb.y:password
$2b$05$MK0JDMhTepEfWjgLSTSpj./l./iUEUGKw2QIqOuGXPmQDJlSFhJL.:123456
$2b$05$OigU1IWW/WH6Dk7UtDBR2uZzjOP76Y2FTgvksLOaCd3QWWCKu07mS:qwerty
$2b$05$teUkHgd0Fvh6zDE/PhcdfuB96nb5P0fwEbttizoEo3ud8jaiRdr5y:letmein
```

---

## 🚀 Opção 2: Demo Completa com Toda a Equipa

### **Coordenação de 4 pessoas - Mais Impressionante**

#### 📋 Preparação Geral (5 minutos antes da demo)

**Todos os membros:**
1. Conectar à mesma rede WiFi ou LAN
2. Anotar os IPs de cada um:
   ```bash
   # Linux/Mac
   ip addr | grep inet
   
   # Windows
   ipconfig
   ```

**Tabela de IPs (exemplo):**
| Membro | IP | Porta |
|--------|-----|-------|
| Henrique | 192.168.100.10 | - |
| Ferro | 192.168.100.20 | - |
| Francisco | 192.168.100.30 | 23 (Telnet) |
| Duarte | 192.168.100.40 | - |

---

### 🎯 Sequência de Execução

#### **Passo 1: Francisco - Servidor Telnet** (Começa primeiro)

**Tempo: 30 segundos**

```powershell
# Windows PowerShell
cd C:\Users\Francisco\HashCrackerLab
.\venv\Scripts\Activate.ps1

# Iniciar servidor Telnet fake
python telnet_authenticated_traffic.py --server --port 23
```

**Saída esperada:**
```
[SERVER] Telnet server listening on 0.0.0.0:23
[SERVER] Waiting for connections...
```

**Nota para Francisco:** 
- Deixar este terminal aberto
- Anotar o teu IP: `192.168.100.30` (exemplo)
- Abrir Wireshark e filtrar `tcp.port == 23`

---

#### **Passo 2: Duarte - Cliente Telnet** (30 segundos depois)

**Tempo: 20 segundos**

```powershell
# Substituir IP pelo IP real do Francisco
python telnet_authenticated_traffic.py --target 192.168.100.30 --user duarte --password Cibersegura
```

**Saída esperada:**
```
[CLIENT] Connecting to 192.168.100.30:23
[CLIENT] Sending username: duarte
[CLIENT] Sending password: Cibersegura
[CLIENT] Connection closed
```

**Francisco vê no Wireshark:**
- Pode ver `duarte` e `Cibersegura` em **TEXTO PLANO**
- Demonstra insegurança do Telnet

---

#### **Passo 3: Ferro - WiFi Attack** (Opcional - se houver rede WiFi real)

**Tempo: 2-3 minutos**

```bash
# Kali Linux
sudo airmon-ng start wlan0

# Se houver rede de teste "LAB-SERVERS"
python wifi_cracker.py --network "LAB-SERVERS" --monitor wlan0mon
```

**Nota:** Esta parte é **opcional** se não houver rede WiFi configurada.

---

#### **Passo 4: Henrique - Orquestração** (Enquanto os outros executam)

**Tempo: ~1 minuto**

```bash
# Arch Linux
source venv/bin/activate

# Config completa (inclui análise de Telnet se houver dados capturados)
python orchestrator.py --config config/projeto_final_ciberseguranca.yaml
```

**Ou usar a config mais simples:**
```bash
python orchestrator.py --config config/advanced_encryption_test.yaml
```

---

## 📊 O Que Mostrar Durante a Apresentação

### 1. **Geração de Hashes** (5 segundos)
Explica:
- "Estamos a gerar 20 hashes com 4 algoritmos diferentes"
- "MD5 e SHA-256 são rápidos mas vulneráveis"
- "Bcrypt e Argon2 são modernos e memory-hard"

### 2. **Ataque de Dicionário** (15 segundos)
Explica:
- "Hashcat está a comparar cada hash com 10.000 palavras"
- "Com GPU, conseguimos testar milhões por segundo"
- "Vemos aqui 16 de 20 passwords crackeadas (80%)"

### 3. **Demo de Força Bruta Visual** (2 segundos)
Explica:
- "Isto mostra como funciona brute-force"
- "Testa TODAS as combinações: 0000, 0001, 0002... até encontrar"
- "PINs de 4 dígitos são crackeados instantaneamente"

### 4. **Benchmark GPU vs CPU** (10 segundos)
Explica:
- "GPU é 16x mais rápida em MD5"
- "Mas apenas 5x mais rápida em Bcrypt"
- "Algoritmos modernos resistem melhor a GPU"

### 5. **Análise Wireshark (se fizeram parte Telnet)** (30 segundos)
Francisco mostra:
- Packet capture com credenciais visíveis
- "Veem aqui 'duarte' e 'Cibersegura' em texto plano"
- "Por isso SSH é obrigatório hoje em dia"

---

## 💡 Pontos-Chave para Discussão

1. **Porque 80% e não 100%?**
   - "admin" não está na wordlist reduzida que usamos
   - Em produção, wordlists têm milhões de palavras

2. **Porque Bcrypt é melhor que MD5?**
   - Memory-hard (usa muita RAM)
   - Parametrizável (cost factor)
   - GPU speedup é menor

3. **É ilegal fazer isto?**
   - Sim, se for contra sistemas sem autorização
   - Legal para: pentest autorizado, pesquisa, CTFs

4. **Como se defender?**
   - Passwords longas (12+ caracteres)
   - Usar algoritmos modernos (Argon2, bcrypt)
   - 2FA/MFA
   - Nunca reutilizar passwords

---

## 🐛 Troubleshooting Rápido

### Erro: "Hashcat not found"
```bash
# Instalar
sudo pacman -S hashcat  # Arch
sudo apt install hashcat  # Kali/Ubuntu
```

### Erro: "No module named 'yaml'"
```bash
pip install -r requirements.txt
```

### Erro: "GPU not detected"
```bash
# Verificar
hashcat -I

# Se vazio, provavelmente drivers GPU não instalados
```

### Francisco não consegue iniciar servidor Telnet
```powershell
# Verificar se porta 23 está livre
netstat -an | findstr :23

# Mudar para outra porta se necessário
python telnet_authenticated_traffic.py --server --port 2323
```

### Duarte não consegue conectar ao Francisco
```powershell
# Testar conectividade básica
ping 192.168.100.30

# Firewall do Windows pode estar a bloquear
# Francisco: Permitir Python através da firewall
```

---

## 📸 Screenshots Recomendados para Relatório

1. Output do `validate_environment.py` ✓
2. Tabela de resultados (algoritmos + taxa de sucesso) ✓
3. Benchmark CPU vs GPU ✓
4. Ficheiro .pot com passwords crackeadas ✓
5. Wireshark mostrando Telnet em plaintext ✓

---

## ⏱️ Timeline da Demo (5 minutos)

| Tempo | Ação | Quem |
|-------|------|------|
| 0:00 | Francisco inicia servidor Telnet | Francisco |
| 0:30 | Duarte conecta e envia credenciais | Duarte |
| 1:00 | Francisco mostra Wireshark | Francisco |
| 1:30 | Henrique inicia orquestrador | Henrique |
| 2:30 | Mostrar geração de hashes | Henrique |
| 3:00 | Mostrar cracking em tempo real | Henrique |
| 3:30 | Mostrar demo força bruta | Henrique |
| 4:00 | Mostrar benchmark GPU vs CPU | Henrique |
| 4:30 | Mostrar resultados finais | Henrique |
| 5:00 | Análise de .pot files | Henrique |

---

**Pronto para apresentar! 🎉**
