# Checklist Rápido (Execução do LAB)

## Antes de Começar

- [ ] Router sem Internet (WAN desligada)
- [ ] Sub-rede `192.168.100.0/24` configurada
- [ ] IPs estáticos definidos
- [ ] Gateway/DNS vazios
- [ ] Antena WiFi ligada ao Kali
- [ ] Modo monitor ativo

## Instalação

- [ ] `setup_arch.sh` executado no Arch
- [ ] `setup_kali.sh` executado no Kali
- [ ] `setup_windows.ps1` executado nos Windows
- [ ] `python tools/validate_environment.py` OK

## Execução

- [ ] `python tools/run_immediate.py` no Arch
- [ ] Relatório gerado em `results/*/REPORT.md`

## Testes LAB

- [ ] Handshake capturado (Kali)
- [ ] Tráfego Telnet simulado (Windows)

## Limpeza

- [ ] `./cleanup.sh` executado
