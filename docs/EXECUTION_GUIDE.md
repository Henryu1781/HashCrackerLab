# Guia de Execução (Resumo)

## ⚖️ Uso Autorizado (LAB)

Uso exclusivo em LAB isolado e autorizado. Não utilizar contra redes/sistemas reais.

## 1) Preparação do LAB (pré-requisitos)

- Router sem WAN (isolado)
- SSID do LAB configurado
- IPs estáticos e sem gateway
- Máquinas com setup executado e `venv` funcional

## 2) Validação (em cada máquina)

```bash
python tools/validate_environment.py
```

Se algo falhar, ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## 3) Execução Imediata (Orquestrador)

```bash
python tools/run_immediate.py
```

## 4) Testes LAB (opcionais)

Notas:
- Execute apenas com autorização e em rede isolada.
- Guarde os artefactos apenas o tempo necessário e faça limpeza no fim.

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

## 6) Pós-execução (recomendado)

- Rever se existem ficheiros sensíveis temporários em `results/*/hashes/`.
- Executar limpeza conforme política do LAB (ver [SECURITY_GUIDE.md](SECURITY_GUIDE.md)).
