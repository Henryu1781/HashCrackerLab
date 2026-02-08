# 🎭 GUIA MESTRE DA APRESENTAÇÃO (Cronograma + Guião)

Documento único com setup, passos e falas — tudo por ordem temporal.

---

## 👥 O Elenco (Papéis)

| Nome | OS | Função | Tarefa Chave |
| :--- | :--- | :--- | :--- |
| **HENRIQUE** | Arch Linux | **Narrador & Orquestrador** | Comanda a demo e corre o GPU Cracking. |
| **FERRO** | Kali Linux | **Hacker WiFi** | Instala o caos na rede wireless (Deauth + Crack). |
| **DUARTE** | Windows | **Utilizador Descuidado** | Envia a password em texto claro (Telnet). |
| **FRANCISCO** | Windows | **Analista de Rede** | Corre o servidor e mostra a falta de encriptação no Wireshark. |

---

## ✅ SETUP INDIVIDUAL (Dia anterior — obrigatório)

### 1) Henrique (Arch)
1. Abrir terminal na pasta do projeto.
2. Executar:
   **Comando:**
   ```bash
   ./setup_arch.sh
   ```
3. Confirmar **sem erros** de NVIDIA/OpenCL.

### 2) Ferro (Kali)
1. Abrir terminal na pasta do projeto.
2. Executar:
   **Comando:**
   ```bash
   ./setup_kali.sh
   ```
3. Testar modo monitor:
   **Comando:**
   ```bash
   sudo airmon-ng start wlan0
   ```
4. Confirmar interface `wlan0mon`.

### 3) Duarte (Windows)
1. Abrir PowerShell como **Administrador**.
2. Na pasta do projeto:
   **Comando:**
   ```powershell
   .\setup_windows.ps1
   ```

### 4) Francisco (Windows)
1. Abrir PowerShell como **Administrador**.
2. Na pasta do projeto:
   **Comando:**
   ```powershell
   .\setup_windows.ps1
   ```
3. Abrir o Wireshark e confirmar a interface correta.

---

## 🗣️ GUIÃO POR TEMPO (Passos → Falas + Comandos)

### 🟢 FASE 0 — Preparação (5 minutos antes)
**Passos:**
1. Ligar os PCs e abrir terminal na raiz do projeto.
2. Ativar ambiente Python.
   **Comando (Linux):**
   ```bash
   source venv/bin/activate
   ```
   **Comando (Windows):**
   ```powershell
   \venv\Scripts\Activate.ps1
   ```
3. Validar ambiente.
   **Comando:**
   ```bash
   python tools/validate_environment.py
   ```
4. Henrique liga o projetor e escreve (sem dar ENTER).
   **Comando:**
   ```bash
   python full_integration_orchestrator.py --mode lab
   ```
5. Ferro ativa modo monitor.
   **Comando:**
   ```bash
   sudo airmon-ng start wlan0
   ```
6. Francisco inicia o servidor Telnet (deixa a janela aberta).
   **Comando:**
   ```powershell
   python telnet_authenticated_traffic.py --server --port 23
   ```
7. Francisco abre o Wireshark e prepara o filtro `tcp.port == 23`.

**Falas:**
> *(Sem fala nesta fase)*

### 🟡 FASE 1 — Introdução & WiFi (0:00–3:00)
**Passos:**
1. Henrique dá ENTER no orquestrador (fase WiFi).
   **Comando:** ENTER
2. Ferro executa o ataque.
   **Comando:**
   ```bash
   python wifi_cracker.py --network "LAB-SERVERS" --monitor wlan0mon
   ```
3. Ao surgir **KEY FOUND**, Henrique confirma no orquestrador.
   **Comando:** s

**Falas:**
- **Henrique (abertura):**
   > "Bom dia. Vamos demonstrar a total falta de segurança em redes mal configuradas. Vamos começar por invadir a rede WiFi 'LAB-SERVERS' e obter a chave de acesso."
- **Henrique (chamada ao Ferro):**
   > "Ferro, podes avançar com a injeção de pacotes?"
- **Ferro (a iniciar):**
   > "A capturar o handshake da rede LAB-SERVERS..."
- **Ferro (quando encontrar a chave):**
   > "Handshake capturado e crackeado! A password da rede é **Cibersegura**."
- **Henrique (confirmação):**
   > "Chave confirmada. Estamos na rede."
- **Henrique (transição):**
   > "Avançamos para a análise de tráfego."

### 🟠 FASE 2 — Captura de Tráfego (3:00–6:00)
**Passos:**
1. Henrique avança para a fase Telnet no orquestrador.
   **Comando:** ENTER
2. Francisco inicia a captura no Wireshark.
3. Duarte executa (com o IP real do Francisco).
   **Comando:**
   ```powershell
   # Substituir IP_DO_FRANCISCO pelo IP real do Francisco (ex: 192.168.1.50)
   python telnet_authenticated_traffic.py --target IP_DO_FRANCISCO --user duarte --password Cibersegura --hash-algo plaintext --count 20
   ```
4. Francisco abre Follow TCP Stream e aponta o ecrã.

**Falas:**
- **Henrique (transição):**
   > "Agora que estamos na rede, vamos ver o que passa. O Duarte vai simular um acesso corporativo via Telnet, um protocolo antigo e inseguro."
- **Duarte (antes do script):**
   > "Vou fazer um login via Telnet como se fosse um utilizador normal."
- **Duarte (depois de enviar):**
   > "Credenciais enviadas."
- **Francisco (a iniciar captura):**
   > "Estou a capturar tráfego Telnet na porta 23."
- **Francisco (no TCP stream):**
   > "Confirmado: o user 'duarte' e a password 'Cibersegura' aparecem em texto claro."

### 🔴 FASE 3 — GPU Cracking Final (6:00–8:00)
**Passos:**
1. Se necessário, Henrique corre.
   **Comando:**
   ```bash
   python orchestrator.py --config config/projeto_final_ciberseguranca.yaml
   ```
2. Henrique comenta as duas fases (dicionário e força bruta).
3. Henrique mostra o relatório final no terminal.

**Falas:**
- **Henrique (transição):**
   > "Para terminar, vamos ver a diferença entre crackear com CPU (como o Ferro fez no WiFi) e usar uma GPU dedicada."
- **Henrique (fecho):**
   > "Conclusão: WPA2 fraco, Telnet e hashes simples não oferecem proteção real. Obrigado."

---

## 🆘 EMERGÊNCIA (Se tudo falhar)

* **Não há WiFi?** Henrique avança o orquestrador simulando sucesso ("Demo Mode").
* **Problema no Telnet?** Se o Duarte não conseguir ligar, o Francisco explica o conceito ou mostra um print antigo.
* **Wireshark não apanha nada?** Duarte mostra o log do terminal: "Sent password: Cibersegura".
* **Limpeza rápida:** `python tools/cleanup.py`
