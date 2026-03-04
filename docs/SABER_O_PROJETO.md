# Saber o Nosso Projeto — HashCrackerLab

Este documento resume, de forma concisa, o propósito do projeto, o papel de cada ficheiro importante e como os componentes se interconectam para formar a plataforma completa.

## Visão Geral

O HashCrackerLab é uma plataforma de laboratório para demonstração, ensino e benchmark de ataques de cracking de hashes, captura/cracking de WPA2 e colheita de credenciais Telnet. O objectivo principal é oferecer um pipeline reprodutível, seguro e mensurável que compare desempenho CPU vs GPU e documente resultados experimentais.

## O que o projeto faz (resumo curto)

- Gera hashes determinísticos a partir de passwords de teste.
- Executa ataques com `hashcat` em modos variados (dicionário, regras, brute-force, híbrido) em CPU e GPU.
- Captura handshakes WPA2 com ferramentas `aircrack-ng` e tenta crackar esses handshakes.
- Gera tráfego Telnet controlado para demonstrar colheita de credenciais plaintext.
- Agrega métricas e gera relatórios (REPORT.md, CSV, JSON). 

## Ficheiros principais e propósito

- `README.md` — Documentação principal e instruções rápidas.
- `docs/ARCHITECTURE.md` — Documentação técnica mais detalhada (arquitetura, topologia).
- `docs/DEVELOPMENT_TIMELINE.md` — História do desenvolvimento e entregáveis.
- `orchestrator.py` — Motor principal que coordena a geração, cracking, métricas e limpeza.
- `full_integration_orchestrator.py` — Orquestrador multi-vetor (modo lab / real-world / pentest).
- `wifi_cracker.py` — Scripts de captura e cracking WPA2 (scan, deauth, crack).
- `telnet_authenticated_traffic.py` — Gerador de tráfego Telnet / servidor para demonstração e captura.
- `src/hash_generator.py` — Gera hashes (MD5, SHA-1, SHA-256, bcrypt, Argon2, etc.) de forma determinística.
- `src/cracking_manager.py` — Interface com `hashcat` para executar modos de ataque e gerir dispositivos (CPU/GPU).
- `src/metrics_collector.py` — Consolida métricas e formata exportações (CSV/JSON).
- `src/network_manager.py` — Valida e aplica o isolamento de rede necessário para execuções seguras.
- `src/cleanup_manager.py` — Limpeza segura (3-pass), anonimização e geração de `CLEANUP_REPORT.json`.
- `src/config_validator.py` — Validação do schema YAML de configuração.
- `tools/validate_environment.py` — Script de checagem das dependências e hardware.
- `tools/cleanup.py` — Utilitário interativo de limpeza de resultados.
- `config/*.yaml` — Perfis de execução (`quick_test.yaml`, `apresentacao_final.yaml`, `real_world.yaml`).
- `rules/` — Regras do Hashcat usadas em ataques.
- `wordlists/` — Wordlists (ex: `rockyou.txt`). **Não incluir em submissões públicas se contiver dados sensíveis**.

## Como os ficheiros se conectam (fluxo de alto nível)

1. O utilizador escolhe um ficheiro de configuração YAML (ex: `config/apresentacao_final.yaml`) e invoca o `orchestrator.py` ou o `full_integration_orchestrator.py` para cenários multi-vetor.
2. O `orchestrator.py` chama `config_validator` para validar a configuração e `network_manager` para garantir isolamento.
3. O `hash_generator.py` gera o conjunto de hashes e escreve ficheiros de entrada para o `cracking_manager.py`.
4. O `cracking_manager.py` invoca `hashcat` em cada modo e dispositivo (CPU/GPU); cada execução produz arquivos `.pot` com os passwords encontrados.
5. O `metrics_collector.py` lê os resultados, compila métricas (tempos, taxas de sucesso, speedup GPU/CPU) e escreve `REPORT.md`, CSV e JSON.
6. O `cleanup_manager.py` executa a limpeza segura dos ficheiros sensíveis (se configurado) e gera auditoria.
7. Para o vetor WiFi, `wifi_cracker.py` opera em paralelo ou como etapa separada: captura com `airodump-ng`, deauth com `aireplay-ng`, e crack com `aircrack-ng`/`hashcat` (formato hccapx/hc22000 quando aplicável).
8. Para Telnet, `telnet_authenticated_traffic.py` gera tráfego e grava capturas que podem ser analisadas com `Wireshark` ou processadas pelo orquestrador para extração de credenciais.

## Diagrama lógico (resumo)

Orquestrador -> Config Validator -> Network Manager
Orquestrador -> Hash Generator -> Cracking Manager -> Hashcat -> .pot files
Cracking Manager -> Metrics Collector -> REPORT.md / CSV / JSON
Wifi Cracker (se habilitado) -> airodump/aireplay -> capture.cap -> crack
Telnet module -> tráfego -> captura -> análise

## Como executar (comandos rápidos)

```bash
source .venv/bin/activate
python orchestrator.py --config config/apresentacao_final.yaml
# ou para demo completa
python full_integration_orchestrator.py --mode lab
```

## Outputs esperados

- `results/{experiment_name}_{timestamp}/REPORT.md`
- `results/.../metrics/metrics.json` e `metrics_by_algorithm.csv`
- `.pot` files por algoritmo e modo (Hashcat)

## Notas de segurança e boas práticas

- Sempre executar com rede isolada (`isolated_network: true`) para evitar exposição.
- Nunca commitar ficheiros `.passwords` ou resultados com plaintext. Use `cleanup_manager`.
- Regenerar `rockyou.txt` localmente em vez de incluir listas de palavras sensíveis no repositório público.

---

Se quiser, posso:  
- Adicionar este ficheiro ao ZIP de entrega e ao sumário do README;  
- Gerar um diagrama Mermaid mais detalhado para incluir em `docs/ARCHITECTURE.md`;  
- Ou expandir a secção de cada ficheiro com exemplos de entradas/saídas.
