# Guia de Execução (Resumo)

## 1) Preparação do LAB

- Router sem WAN (isolado)
- SSID do LAB configurado
- IPs estáticos e sem gateway

## 2) Validação

```bash
python tools/validate_environment.py
```

## 3) Execução Imediata (Orquestrador)

```bash
python tools/run_immediate.py
```

## 4) Testes LAB

### Handshake (Kali)
```bash
sudo tools/capture_handshake.sh -s "LAB-SERVERS" -i wlan0 -t 60 -d 10
```

### Tráfego Telnet (Windows)
Servidor:
```bash
python tools/generate_telnet_traffic.py --server --host 0.0.0.0 --port 2323
```
Cliente:
```bash
python tools/generate_telnet_traffic.py --client --host 192.168.100.10 --port 2323 --user labuser --password labpass
```

## 5) Resultados

- Relatório: `results/*/REPORT.md`
- Métricas: `results/*/metrics/`
- Logs: `results/*/logs/`
