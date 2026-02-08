# 🎭 GUIA MESTRE DA APRESENTAÇÃO (Cronograma & Guião)

Este é o documento único que devem seguir durante a apresentação. Contém o timeline, as falas sugeridas e os comandos exatos.

---

## 👥 O Elenco (Papéis)

| Nome | OS | Função | Tarefa Chave |
| :--- | :--- | :--- | :--- |
| **HENRIQUE** | Arch Linux | **Narrador & Orquestrador** | Comanda a demo e corre o GPU Cracking. |
| **FERRO** | Kali Linux | **Hacker WiFi** | Instala o caos na rede wireless (Deauth + Crack). |
| **DUARTE** | Windows | **Utilizador Descuidado** | Envia a password em texto claro (Telnet). |
| **FRANCISCO** | Windows | **Analista de Rede** | Corre o servidor e mostra a falta de encriptação no Wireshark. |

---

## 🗣️ FALAS POR PESSOA (Texto pronto a ler)

### HENRIQUE (Narrador)
- **Abertura (início):**
   > "Bom dia. Vamos demonstrar como uma rede mal configurada pode ser comprometida rapidamente."
- **Antes do WiFi:**
   > "Ferro, podes avançar com a injeção de pacotes?"
- **Transição para Telnet:**
   > "Agora que estamos na rede, vamos observar tráfego inseguro com Telnet."
- **Transição para GPU:**
   > "Para terminar, vamos comparar CPU vs GPU no cracking de hashes."
- **Fecho:**
   > "Conclusão: WPA2 fraco, Telnet e hashes simples não oferecem proteção real. Obrigado."

### FERRO (WiFi)
- **Após iniciar o ataque:**
   > "A capturar o handshake da rede LAB-SERVERS..."
- **Quando encontrar a chave:**
   > "Handshake capturado e crackeado! A password da rede é **Cibersegura**."

### DUARTE (Utilizador Descuidado)
- **Antes de executar o script:**
   > "Vou fazer um login via Telnet como se fosse um utilizador normal."
- **Depois de enviar tráfego:**
   > "Credenciais enviadas."

### FRANCISCO (Analista)
- **Ao iniciar captura:**
   > "Estou a capturar tráfego Telnet na porta 23."
- **Ao abrir o stream:**
   > "Confirmado: o user 'duarte' e a password 'Cibersegura' aparecem em texto claro."

## 🔧 GUIA DE SETUP INDIVIDUAL (Preparação Inicial)

**⚠️ IMPORTANTE: Executar isto no dia anterior ou assim que chegarem ao laboratório!**

### 1) Henrique (Arch Linux - Orquestrador)
*Objetivo: Instalar drivers GPU, Hashcat e dependências do sistema.*
1. Abre um terminal na pasta do projeto.
2. Corre o script:
   ```bash
   ./setup_arch.sh
   ```
3. Confirma no ecrã que **não há erros** de NVIDIA/OpenCL.
4. Fecha o terminal.

### 2) Ferro (Kali Linux - WiFi Cracker)
*Objetivo: Preparar ferramentas de auditoria WiFi (Aircrack-ng) e Python.*
1. Abre um terminal na pasta do projeto.
2. Corre o script:
   ```bash
   ./setup_kali.sh
   ```
3. Testa o modo monitor:
   ```bash
   sudo airmon-ng start wlan0
   ```
4. Confirma que apareceu a interface `wlan0mon`.
5. Fecha o terminal.

### 3) Duarte (Windows - Cliente)
*Objetivo: Instalar Python e configurar o ambiente.*
1. Abre o PowerShell como **Administrador**.
2. Vai à pasta do projeto.
3. Corre o script:
   ```powershell
   .\setup_windows.ps1
   ```
4. Confirma no ecrã que terminou sem erros.
5. Fecha o PowerShell.

### 4) Francisco (Windows - Servidor/Analista)
*Objetivo: Instalar Wireshark e preparar captura.*
1. Abre o PowerShell como **Administrador**.
2. Vai à pasta do projeto.
3. Corre o script:
   ```powershell
   .\setup_windows.ps1
   ```
4. Abre o Wireshark e confirma que consegues selecionar a interface correta.
5. Fecha o Wireshark.

---

## ⏱️ CRONOGRAMA PASSO-A-PASSO

### 🟢 FASE 0: PREPARAÇÃO (5 Minutos Antes)

**Checklist rápido (todos fazem isto pela ordem):**
1. Ligar o PC.
2. Abrir um terminal na raiz do projeto.
3. Ativar o ambiente Python:
   - **Linux:** `source venv/bin/activate`
   - **Windows:** `.\venv\Scripts\Activate.ps1`
4. Validar ambiente: `python tools/validate_environment.py`.

**Henrique (Arch) — passos exatos:**
1. Liga o projetor.
2. Escreve este comando **mas não carregues ENTER**:
   ```bash
   python full_integration_orchestrator.py --mode lab
   ```
3. Espera pelo sinal do Ferro.

**Ferro (Kali) — passos exatos:**
1. Abre terminal.
2. Ativa modo monitor:
   ```bash
   sudo airmon-ng start wlan0
   ```
3. Confirma `wlan0mon` aparece.

**Francisco (Windows) — passos exatos:**
1. Abre PowerShell.
2. Inicia o servidor fake (deixa a janela aberta):
   ```powershell
   python telnet_authenticated_traffic.py --server --port 23
   ```
3. Abre o Wireshark.
4. Seleciona a interface correta.
5. Define o filtro: `tcp.port == 23` (não carregar Enter ainda).

---

### 🟡 FASE 1: INTRODUÇÃO & WIFI (Minutos 0-3)

**Henrique (Falando):**
> "Bom dia. Vamos demonstrar a total falta de segurança em redes mal configuradas. Vamos começar por invadir a rede WiFi 'LAB-SERVERS' e obter a chave de acesso."

**1. Henrique:** Dá **ENTER** no orquestrador.
   *O script vai parar e pedir confirmação para a fase WiFi.*

**2. Henrique:** "Ferro, podes avançar com a injeção de pacotes."

**3. Ferro (Kali):** Executa o ataque:
   ```bash
   python wifi_cracker.py --network "LAB-SERVERS" --monitor wlan0mon
   ```
   *O script vai scanear -> fazer deauth -> capturar handshake -> crackear.*

**4. Ferro (Ao ver "KEY FOUND"):**
> "Handshake capturado e crackeado! A password da rede é **Cibersegura**."

**Henrique:** Insere "s" (sim) no orquestrador para confirmar o sucesso.

---

### 🟠 FASE 2: CAPTURA DE TRÁFEGO (Minutos 3-6)

**Henrique (Falando):**
> "Agora que estamos na rede, vamos ver o que passa. O Duarte vai simular um acesso corporativo via Telnet, um protocolo antigo e inseguro."

**1. Henrique:** Avança para a próxima fase no orquestrador.

**2. Francisco (Windows):**
   1. Confirma que o servidor python está a correr (janela aberta).
   2. No Wireshark, clica no botão azul ("Start").

**3. Duarte (Windows):** Gera o tráfego vulnerável (Apontando para o Francisco):
   ```powershell
   # Substituir IP_DO_FRANCISCO pelo IP real do Francisco (ex: 192.168.1.50)
   python telnet_authenticated_traffic.py --target IP_DO_FRANCISCO --user duarte --password Cibersegura --hash-algo plaintext --count 20
   ```
   *(Nota: O IP de Broadcast NÃO funciona para Telnet TCP. Usem o IP direto.)*

**4. Francisco (Olhando para o Wireshark):**
   1. Vê os pacotes vermelhos/verdes.
   2. Clica com o botão direito num pacote "Telnet" (ou DATA).
   3. Seleciona *Follow TCP Stream*.
   4. Aponta para o ecrã:
   > "Confirmado. Consigo ler o user 'duarte' e a password 'Cibersegura' totalmente em texto claro."

---

### 🔴 FASE 3: GPU CRACKING FINAL (Minutos 6-8)

**Henrique (Falando):**
> "Para terminar, vamos ver a diferença entre crackear com CPU (como o Ferro fez no WiFi) e usar uma GPU dedicada."

**1. Henrique (Arch):** O orquestrador deve estar na fase final. Se não, corre este comando específico:
   ```bash
   python orchestrator.py --config config/projeto_final_ciberseguranca.yaml
   ```

**2. Henrique:**
   1. Diz: "O script vai correr o WPA2 Cracking (Dicionário)."
   2. Diz: "Logo a seguir, há uma Simulação de Força Bruta."
   3. Explica: "Enquanto o dicionário testa palavras conhecidas, a Força Bruta é **Tentativa e Erro** pura. Testamos 0000, 0001, 0002... até abrir. Com esta GPU, faríamos milhões por segundo."

**3. FIM:** Mostra o relatório final gerado no terminal.
> "Conclusão: WPA2 fraco, Telnet e Hashes simples não oferecem proteção real. Obrigado."

---

## 🆘 EMERGÊNCIA (Se tudo falhar)

*   **Não há WiFi?** O Henrique avança o orquestrador simulando sucesso ("Demo Mode").
*   **Problema no Telnet?** Se o Duarte não conseguir ligar, o Francisco apenas *explica* o conceito ou mostra um print antigo.
*   **Wireshark não apanha nada?** O Duarte mostra o log do seu terminal a dizer "Sent password: Cibersegura".
*   **Comando de Limpeza Rápida:** `python tools/cleanup.py`
