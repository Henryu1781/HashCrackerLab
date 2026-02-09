# Hash Cracker Lab - Projeto Final

Este repositório contém a infraestrutura completa para o projeto de Segurança Ofensiva.

**Equipa:**
- **Henrique** (Arch Linux): Orchestration & GPU Cracking
- **Ferro** (Kali Linux): WiFi Penetration Testing
- **Duarte & Francisco** (Windows): Network Traffic Analysis & Generation

---

## 🚀 Guia de Início Rápido

### 1. Instalação / Validação
Cada membro deve correr o script de validação no seu OS.

**Arch (Henrique) / Kali (Ferro):**
```bash
source venv/bin/activate
python tools/validate_environment.py
```

**Windows (Duarte/Francisco):**
```powershell
.\venv\Scripts\Activate.ps1
python tools\validate_environment.py
```

### 2. Execução (Por Papel)

#### 🔵 Henrique (Líder/GPU)
Usa o orquestrador para gerir a demo. O novo modo interativo inclui demonstração de força bruta visual.
```bash
python full_integration_orchestrator.py --mode lab
```
Para teste de GPU isolado (inclui benchmark WPA2 e Demo Visual de Força Bruta):
```bash
python orchestrator.py --config config/projeto_final_ciberseguranca.yaml
```

#### 🟡 Ferro (WiFi)
Ataca a rede `LAB-SERVERS`.
```bash
sudo airmon-ng start wlan0
python wifi_cracker.py --network "LAB-SERVERS" --monitor wlan0mon
```

#### 🟣 Francisco (Servidor + Analista)
Inicia o servidor Telnet fake e usa o **Wireshark** para validar o tráfego em claro.
```powershell
python telnet_authenticated_traffic.py --server --port 23
```

#### 🟢 Duarte (Gerador Telnet)
Envia credenciais de teste para o servidor do Francisco.
```powershell
# Substituir IP_DO_FRANCISCO pelo IP real do Francisco (ex: 192.168.1.50)
python telnet_authenticated_traffic.py --target IP_DO_FRANCISCO --user duarte --password Cibersegura --hash-algo plaintext
```

---

## 📄 Documentação Relevante
- **Guia de Apresentação (Setup + Guião)**: [GUIA_DA_APRESENTACAO.md](GUIA_DA_APRESENTACAO.md)
- **Guia Técnico Completo**: [FULL_INTEGRATION_GUIDE.md](FULL_INTEGRATION_GUIDE.md)
- **Setup de Rede**: [docs/NETWORK_SETUP.md](docs/NETWORK_SETUP.md)

---
*HashCrackerLab - Build Final Verified*
