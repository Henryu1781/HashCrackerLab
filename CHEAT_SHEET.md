# Cheat Sheet - Resumo da Apresentação

| Quem | OS | Função Principal | Comando Chave |
| :--- | :--- | :--- | :--- |
| **Henrique** | Arch | **Orquestrador / GPU** | `python full_integration_orchestrator.py --mode lab` |
| **Ferro** | Kali | **WiFi (Cracking)** | `python wifi_cracker.py --network "LAB-SERVERS"` |
| **Duarte** | Win | **Gerar Tráfego (Telnet)** | `python telnet_authenticated_traffic.py ... --hash-algo plaintext` |
| **Francisco** | Win | **Capturar (Wireshark)** | Filtro: `tcp.port == 23` |

---

## ⏱️ Timeline da Demo (Modo Lab)

### T-0: Setup
1. **Henrique**: Inicia `full_integration_orchestrator.py`.
2. **Setup**: Todos confirmam que têm `venv` ativo e ferramentas prontas.

### T+1: WiFi (Ferro)
1. Henrique o comando para Fase 1.
2. **Ferro** executa `wifi_cracker.py`.
3. Ferro confirma: "Handshake capturado. Senha é Cibersegura".
4. Henrique regista sucesso no orquestrador.

### T+3: Telnet (Duarte & Francisco)
1. Henrique dá o comando para Fase 2.
2. **Francisco** inicia captura no Wireshark.
3. **Duarte** corre o script de tráfego (`telnet...`).
4. Francisco confirma vizualização da senha em *plaintext*.

### T+5: GPU Hash Cracking (Henrique)
1. Henrique executa a Fase 3 (localmente no Arch).
2. O script `orchestrator.py` corre na GPU NVIDIA.
3. Mostra velocidade de cracking e estatísticas finais.

---

## 🚨 Comandos de Emergência

**Limpar tudo (Genérico):**
`python tools/cleanup_manager.py`

**Reset placa WiFi (Kali):**
`sudo airmon-ng stop wlan0mon && sudo NetworkManager start`

**Validar Instalação:**
`python tools/validate_environment.py`
