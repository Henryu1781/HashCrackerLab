# Historial de Desenvolvimento — HashCrackerLab

Linha do tempo reconstruída a partir do histórico de commits do Git, agrupada por fases lógicas de evolução.

---

## v0.1 — Fundação (2026-02-02)

Criação da estrutura base do projeto, primeiros módulos funcionais e preparação para GitHub.

| Commit | Descrição |
|--------|-----------|
| `3524650` | Preparar projeto para GitHub (estrutura de diretórios, `.gitignore`) |
| `703c0db` | Adicionar licença MIT e README inicial |
| `36dccad` | Implementar módulo WiFi (`wifi_cracker.py`) e Telnet (`telnet_authenticated_traffic.py`) |
| `eb03abc` | Documentação abrangente para laboratório 4-PC |
| `5d3fc28` | **Auditoria completa**: correção de 16 problemas identificados no código |
| `c639a64` | Fix: bloco if/else do Chocolatey no `setup_windows.ps1` |
| `bbd48a4` | Fix: reescrita do script Windows com quotes seguros |

**Entregáveis da fase:**
- Pipeline base: `orchestrator.py` → `hash_generator.py` → `cracking_manager.py` → `metrics_collector.py`
- WiFi cracker com scan, captura e cracking
- Servidor/cliente Telnet com autenticação simulada
- Setup scripts para Arch, Kali e Windows
- Estrutura de configuração YAML

---

## v0.2 — Hardening (2026-02-06)

Endurecimento da plataforma: compatibilidade Windows, exclusões de antivírus, validação de ambiente.

| Commit | Descrição |
|--------|-----------|
| `3aa58b1` | Atualizar setup Windows e wordlists |
| `f1f6c09` | Adicionar script de exclusões Windows Defender (`add_exclusions.ps1`) + melhorar validação |
| `d38ab42` | Documentar instruções de exclusão do Defender |
| `c333b93` | Adicionar secção tutorial de captura de credenciais Telnet |
| `52769e3` | Melhorar clareza da documentação e guidance lab-only |

**Entregáveis da fase:**
- `add_exclusions.ps1` — script dedicado para exclusões do Windows Defender
- `tools/validate_environment.py` — verificação cruzada de todas as dependências
- Documentação orientada para ambiente de laboratório isolado

---

## v0.3 — Integração (2026-02-07 a 2026-02-08)

Unificação dos três vetores de ataque num pipeline coeso, com suporte a SHA-256 salted e demonstração de brute-force.

| Commit | Descrição |
|--------|-----------|
| `b038569` | Atualizar setup scripts, tools, e adicionar regras hashcat |
| `9b5ddfe` | **Merge final**: unificação WiFi + Telnet + Hash Cracking com documentação limpa |
| `5ea57e3` | Substituir guias fragmentados por Master Presentation Guide |
| `ea41cb4` | Integrar demonstração de Brute Force no guia principal |
| `7221128` | **Fix crítico**: habilitar suporte SHA-256 salted (mode 1420) no cracking manager e config |
| `4be452a` | Verificar imports do Orchestrator e estabilizar demo WPA2 |
| `f5b3a5d` | Atualizar guia de apresentação e demo Telnet |
| `a4db532` | Atualizar guia de apresentação com comandos |
| `57ba0ac` | Refinar network setup e guia de demonstração |

**Entregáveis da fase:**
- `full_integration_orchestrator.py` — orquestrador multi-vetor com 3 modos (lab/real-world/pentest)
- Suporte completo para hashes salted (`hash($salt.$pass)` → hashcat modes 20, 120, 1420)
- Demonstração conceptual de brute-force (PIN 0000–9999)
- Regras de mutação hashcat (`rules/`) importadas do repositório oficial

---

## v0.4 — Apresentação (2026-02-09)

Fase final de preparação para a apresentação académica. Refinamento de parâmetros, consolidação documental e resolução de bugs de compatibilidade.

### Sub-fase: Documentação e Guião

| Commit | Descrição |
|--------|-----------|
| `e48a357` | Aprimoramento completo do lab — documentação, correções e otimizações |
| `eeb89b0` | Fix: `setup_windows.ps1` usa `py` launcher e `.venv` |
| `aaec0e7` | Documentação consolidada: 3 guias únicos, timeline 30min |
| `2233f0f` | Merge: apresentação + execução em 1 único guia |
| `5dfa733` | Timeline detalhado com outputs esperados e narração |
| `b653d0e` | Guião reescrito: falas + comandos como script de apresentação |
| `bd92b56` | Adicionar passos de configuração do router ao guia |

### Sub-fase: Features de Ataque

| Commit | Descrição |
|--------|-----------|
| `a3d7a2f` | 50 hashes CPU vs GPU, arquitetura, contexto de alunos |
| `c1a19c5` | **Refactor**: reduzir para 3 ficheiros de config (quick_test, apresentação, real_world) |
| `bba1d9b` | Adicionar modo `--deauth` ao `wifi_cracker.py` para Ferro |
| `f44c3ae` | **5 modos de ataque**: dicionário, rules, brute-force, padrão, híbrido |
| `1467192` | Usar `rockyou.txt` (14.3M) em vez de `rockyou-small.txt` (10K) |
| `891c752` | Reduzir para 15 passwords (5 fracas + 5 médias + 5 fortes) |

### Sub-fase: Bug Fixes (WiFi Compatibility)

| Commit | Descrição |
|--------|-----------|
| `89e9d0b` | Fix: mensagens print quebradas no `wifi_cracker.py` |
| `ae27614` | Fix: substituir `iwconfig` por `iw` para verificação de monitor mode (compatibilidade Kali) |
| `1f60f4e` | Fix: usar `/sys/class/net` para check de monitor (sem dependência de `iw`/`iwconfig`) |
| `b3dcf0d` | Fix: procurar `iw` em `/usr/sbin`, `/sbin`, `/usr/bin` (PATH issue no Kali) |
| `086a0ea` | Fix: CSV parsing do airodump (campo ESSID), aumentar timeout de scan, debug output |
| `08a881b` | **Audit final**: fix de bugs em todos os scripts, configs e docs |

**Entregáveis da fase:**
- Amostra otimizada: 15 passwords × 4 algoritmos = 60 hashes
- 5 categorias de ataque configuradas em YAML
- Wordlist completa RockYou (14.3M entries)
- WiFi deauth standalone para Kali
- Guião de apresentação completo de 30 minutos (GUIA_EXECUCAO.md)
- Compatibilidade WiFi verificada em múltiplas distribuições Linux

---

## Estatísticas do Projeto

| Métrica | Valor |
|---------|-------|
| Total de commits | 35 |
| Período de desenvolvimento | 2026-02-02 a 2026-02-09 (8 dias) |
| Ficheiros de código Python | 12 |
| Linhas de código (estimativa) | ~4500 |
| Ficheiros de configuração YAML | 3 |
| Scripts de setup | 3 (Arch, Kali, Windows) |
| Algoritmos de hashing | 7 (MD5, SHA-1, SHA-256, Bcrypt, Scrypt, PBKDF2, Argon2) |
| Modos de ataque | 4 (Dictionary, Brute-force, Combinator, Hybrid) |
| Sistemas operativos suportados | 3 (Arch Linux, Kali/Debian, Windows) |
