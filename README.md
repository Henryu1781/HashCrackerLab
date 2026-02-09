# 🔐 HashCrackerLab — Projeto Final de Cibersegurança

**Unidade Curricular:** Cibersegurança
**Grupo de Alunos:** Henrique · Ferro · Francisco · Duarte
**Duração da Apresentação:** 30 minutos

---

## 👥 Grupo

| Aluno | Sistema | Função |
|------|---------|--------|
| **Henrique** | Arch Linux | GPU Cracking + Coordenação |
| **Ferro** | Kali Linux | WiFi WPA2 Penetration Testing |
| **Francisco** | Windows | Servidor Telnet + Wireshark |
| **Duarte** | Windows | Cliente Telnet (tráfego de teste) |

---

## 📚 Documentação

| Documento | Para Quê |
|-----------|----------|
| **[GUIA_EXECUCAO.md](GUIA_EXECUCAO.md)** | Apresentação 30min + Setup técnico |

---

## ⚡ Setup Rápido (15 minutos)

### 1. Clonar Repositório
```bash
git clone https://github.com/Henryu1781/HashCrackerLab
cd HashCrackerLab
```

### 2. Setup por Sistema

**Arch Linux (Henrique):**
```bash
./setup_arch.sh
source venv/bin/activate
python tools/validate_environment.py
```

**Kali Linux (Ferro):**
```bash
./setup_kali.sh
source venv/bin/activate
sudo airmon-ng start wlan0  # Criar wlan0mon
```

**Windows (Francisco/Duarte):**
```powershell
.\setup_windows.ps1
.\venv\Scripts\Activate.ps1
wireshark --version  # Validar Wireshark
```

---

## 🎯 Execução Rápida (5 minutos)

### Demonstração GPU + CPU (Henrique)
```bash
cd ~/Projects/HashCrackerLab
source venv/bin/activate
python orchestrator.py --config config/apresentacao_final.yaml
```

**Output esperado:** 200 hashes (50×4 algoritmos) → ~98 crackeadas (49%) com comparação CPU vs GPU

### WiFi Cracking (Ferro)
```bash
python wifi_cracker.py --capture --ssid LAB-SERVERS
# Após captura do handshake:
python wifi_cracker.py --crack --hash hashes/wifi_sample.hc22000
```

### Tráfego Telnet (Francisco + Duarte)
```powershell
# Francisco (servidor):
python telnet_authenticated_traffic.py --server --port 23

# Duarte (cliente):
telnet 192.168.100.30 23
# Login: admin / SecurePass123
```

---

## 📊 Capabilities

### ✅ Hash Cracking
- **Algoritmos:** MD5, SHA-256, Bcrypt, Argon2id
- **Amostra:** 50 passwords × 4 algoritmos = 200 hashes
- **Comparação:** CPU vs GPU (hashcat -D flag)
- **GPU:** 16.5x speedup vs CPU (MD5)

### ✅ WiFi Security
- **WPA2 Handshake Capture** via aircrack-ng
- **Offline Cracking** com hashcat mode 22000
- **Demo:** Rede `LAB-SERVERS` password `Cibersegura`

### ✅ Network Traffic
- **Telnet Plaintext** credential capture
- **Wireshark** packet analysis
- **Demo:** Mostrar credenciais em texto claro

---

## 🛠️ Requisitos

### Hardware
- **Henrique:** GPU NVIDIA (OpenCL)
- **Ferro:** WiFi com modo monitor
- **Todos:** 4GB RAM, 10GB disco

### Software
- **Python:** 3.10+
- **Hashcat:** v6.0+
- **Aircrack-ng:** WiFi tools suite
- **Wireshark:** Network analyzer

---

## 📈 Resultados Esperados

```
┌──────────┬───────┬───────────┬──────────────┬──────────────┬─────────┐
│ Algoritmo│ Total │ Crackeadas│   Tempo GPU  │  Tempo CPU   │ Speedup │
├──────────┼───────┼───────────┼──────────────┼──────────────┼─────────┤
│ MD5      │  50   │    30     │    0.3s      │    4.8s      │  16.5x  │
│ SHA-256  │  50   │    28     │    1.2s      │   12.0s      │   9.9x  │
│ Bcrypt   │  50   │    22     │   18.0s      │   95.0s      │   5.2x  │
│ Argon2   │  50   │    18     │   45.0s      │  timeout     │   6.1x  │
├──────────┼───────┼───────────┼──────────────┼──────────────┼─────────┤
│ WiFi WPA2│   1   │     1     │    3.2s      │     —        │    —    │
│ Telnet   │   —   │     —     │  plaintext   │  plaintext   │    —    │
└──────────┴───────┴───────────┴──────────────┴──────────────┴─────────┘
```

---

## 🆘 Troubleshooting

| Problema | Solução |
|----------|---------|
| GPU não detectada | `hashcat -I` → verificar OpenCL |
| WiFi não captura | `sudo airmon-ng check kill` |
| Wireshark sem packets | Verificar interface (deve estar em modo promíscuo) |
| Import errors | `pip install -r requirements.txt` |

---

## 📄 Licença

MIT License - Ver [LICENSE](LICENSE)

---

**Status:** ✅ Pronto para Apresentação | **Última atualização:** 2026-02-09
