# LAB Setup (4 PCs + Router + Antena)

Este guia descreve a montagem e execução do LAB com 4 portáteis, 1 router e 1 antena WiFi.

## ⚖️ Uso autorizado

Montagem e testes apenas em ambiente isolado e autorizado.

## Roles e Máquinas

- **PC1 (Arch)**: Orquestrador + GPU Tester
- **PC2 (Kali)**: Monitorização + Antena + CPU Tester
- **PC3 (Windows)**: Comunicação + VM Kali
- **PC4 (Windows)**: Comunicação + VM Kali

## Topologia de Rede (LAB Isolado)

- Router **sem ligação WAN/Internet**.
- SSID do LAB (ex.: `LAB-SERVERS`).
- Sub-rede: `192.168.100.0/24`.
- Gateway e DNS **vazios** em todas as máquinas.

### Verificação rápida de isolamento

- Linux: `ip route` não deve ter `default via ...`
- Windows: `route print | findstr 0.0.0.0`

### IPs Estáticos

- PC1 (Arch): `192.168.100.10`
- PC2 (Kali): `192.168.100.20`
- PC3 (Windows): `192.168.100.30`
- PC4 (Windows): `192.168.100.40`

## Instalação por PC

### PC1: Arch (Orquestrador + GPU)

```bash
chmod +x setup_arch.sh
./setup_arch.sh
source venv/bin/activate
python tools/validate_environment.py
```

### PC2: Kali (Monitorização + CPU + Antena)

```bash
chmod +x setup_kali.sh
./setup_kali.sh
source venv/bin/activate
python tools/validate_environment.py
```

### PC3/PC4: Windows (Comunicação + VM Kali)

```powershell
# PowerShell como Administrador
.\add_exclusions.ps1
.\setup_windows.ps1

# Depois, normal
.\venv\Scripts\Activate.ps1
python tools/validate_environment.py
```

## Isolamento de Rede

**Linux (Arch/Kali):**
```bash
sudo ip route del default
ip route
```

**Windows:**
- Propriedades IPv4 → Gateway em branco.

## Checklist Pré-Execução

- [ ] Router sem Internet (WAN desligada)
- [ ] IPs estáticos configurados
- [ ] Sem rota default
- [ ] Antena em modo monitor (Kali)
- [ ] Wordlists disponíveis
- [ ] Ambiente Python ativo

## Execução Rápida

**No Arch (Orquestrador):**
```bash
python tools/run_immediate.py
```

## Teste de Captura de Handshake (Kali)

```bash
sudo tools/capture_handshake.sh -s "LAB-SERVERS" -i wlan0 -t 60 -d 10
```

## Teste de Tráfego (Telnet Simulado)

**Servidor (PC1 ou PC3):**
```bash
python tools/generate_telnet_traffic.py --server --host 0.0.0.0 --port 2323
```

**Cliente (PC4):**
```bash
python tools/generate_telnet_traffic.py --client --host 192.168.100.10 --port 2323 \
  --user labuser --password labpass
```

## Pós-Execução

- Relatório: `results/*/REPORT.md`
- Métricas: `results/*/metrics/`
- Logs: `results/*/logs/`

## Notas Éticas e Legais

- Uso exclusivo em ambiente LAB isolado e autorizado.
- Nunca usar em redes reais/produção.
