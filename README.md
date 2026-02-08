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

#### 🟢 Duarte (Gerador Telnet)
Envia credenciais de teste constantemente.
```powershell
python telnet_authenticated_traffic.py --target 192.168.100.255 --user duarte --password Cibersegura --hash-algo plaintext
```

#### 🟣 Francisco (Analista)
Usa o **Wireshark** para validar que as credenciais do Duarte estão a passar em claro na rede.

---

## 📄 Documentação Relevante
- **Instruções Detalhadas por Pessoa**: [INSTRUCOES_POR_PESSOA.md](INSTRUCOES_POR_PESSOA.md)
- **Cheat Sheet da Apresentação**: [CHEAT_SHEET.md](CHEAT_SHEET.md)
- **Guia Técnico Completo**: [FULL_INTEGRATION_GUIDE.md](FULL_INTEGRATION_GUIDE.md)

---
*HashCrackerLab - Build Final Verified*
