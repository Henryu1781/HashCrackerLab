# 🎭 GUIA MESTRE DA APRESENTAÇÃO (Cronograma & Guião)

Este é o documento único que devem seguir durante a apresentação. Contém o timeline, as falas sugeridas e os comandos exatos.

---

## 👥 O Elenco (Papéis)

| Nome | OS | Função | Tarefa Chave |
| :--- | :--- | :--- | :--- |
| **HENRIQUE** | Arch Linux | **Narrador & Orquestrador** | Comanda a demo e corre o GPU Cracking. |
| **FERRO** | Kali Linux | **Hacker WiFi** | Instala o caos na rede wireless (Deauth + Crack). |
| **DUARTE** | Windows | **Utilizador Descuidado** | Envia a password em texto claro (Telnet). |
| **FRANCISCO** | Windows | **Analista de Rede** | Mostra a falta de encriptação no Wireshark. |

---

## ⏱️ CRONOGRAMA PASSO-A-PASSO

### 🟢 FASE 0: PREPARAÇÃO (5 Minutos Antes)

**Todos:**
1. Liguem os PCs.
2. Abram os terminais.
3. Ativem o ambiente Python (`source venv/bin/activate` ou `.\venv\Scripts\Activate.ps1`).
4. **Validem:** Corram `python tools/validate_environment.py`.

**Henrique (Arch):**
- Garante que tens o projetor ligado (se houver).
- Prepara o comando principal, mas não dês ENTER ainda:
  ```bash
  python full_integration_orchestrator.py --mode lab
  ```

**Ferro (Kali):**
- Garante o modo monitor:
  ```bash
  sudo airmon-ng start wlan0
  ```

**Francisco (Windows):**
- Abre o Wireshark e prepara o filtro `tcp.port == 23`.

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

**2. Francisco (Windows):** Clica no botão azul ("Start") do Wireshark.

**3. Duarte (Windows):** Gera o tráfego vulnerável:
   ```powershell
   python telnet_authenticated_traffic.py --target 192.168.100.255 --user duarte --password Cibersegura --hash-algo plaintext --count 20
   ```
   *(Nota: Usa o IP de Broadcast ou o IP do Francisco)*

**4. Francisco (Olhando para o Wireshark):**
   - Vê os pacotes vermelhos aparecerem.
   - Clica com o botão direito num pacote "Telnet" -> *Follow TCP Stream*.
   - Aponta para o ecrã:
   > "Confirmado. Consigo ler o user 'duarte' e a password 'Cibersegura' totalmente em texto claro."

---

### 🔴 FASE 3: GPU CRACKING FINAL (Minutos 6-8)

**Henrique (Falando):**
> "Para terminar, vamos ver a diferença entre crackear com CPU (como o Ferro fez no WiFi) e usar uma GPU dedicada."

**1. Henrique (Arch):** O orquestrador deve estar na fase final. Se não, corre este comando específico para impressionar:
   ```bash
   python orchestrator.py --config config/projeto_final_ciberseguranca.yaml
   ```

**2. Henrique:**
   - O Script vai correr o WPA2 Cracking (Dicionário).
   - **NOVIDADE:** Logo a seguir, vai correr uma "Simulação de Força Bruta".
   - Explica: "Enquanto o dicionário testa palavras conhecidas, a Força Bruta é **Tentativa e Erro** pura. Testamos 0000, 0001, 0002... até abrir. Com esta GPU, faríamos milhões por segundo."

**3. FIM:** Mostra o relatório final gerado no terminal.
> "Conclusão: WPA2 fraco, Telnet e Hashes simples não oferecem proteção real. Obrigado."

---

## 🆘 EMERGÊNCIA (Se tudo falhar)

*   **Não há WiFi?** O Henrique avança o orquestrador simulando sucesso ("Demo Mode").
*   **Wireshark não apanha nada?** O Duarte mostra o log do seu terminal a dizer "Sent password: Cibersegura".
*   **Comando de Limpeza Rápida:** `python tools/cleanup.py`
