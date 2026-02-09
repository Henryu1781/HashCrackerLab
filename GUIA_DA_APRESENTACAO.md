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
   - Para o benchmark CPU vs GPU, confirmar que existe OpenCL CPU (POCL):
     ```bash
     clinfo | grep -i "Device Type" | head
     ```

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

## 🌐 SETUP DO ROUTER + IPs (Antes da apresentação)

### Router (AP de laboratório)
1. Ligar o router à corrente.
2. Ligar um cabo de rede do router para o portátil do Henrique (LAN do router → porta Ethernet do PC).
3. Aguardar 1–2 minutos até as luzes ficarem estáveis.
4. No PC do Henrique, abrir o navegador.
5. No navegador, escrever o IP do router (normalmente `192.168.0.1` ou `192.168.1.1`) e carregar ENTER.
6. Fazer login no painel do router.
   - Se pedirem user/pass e não souberes, usar o que está na etiqueta do router.
7. Ir ao menu **Wireless** / **Wi‑Fi**.
8. Definir o **SSID** exatamente como: `LAB-SERVERS`.
9. Definir **Security / Encryption** como **WPA2-PSK (AES)**.
10. Definir a **Password/Key** exatamente como: `Cibersegura`.
11. Guardar/Apply/Save.
12. Se o router pedir para reiniciar, confirmar o reinício.
13. Aguardar 1–2 minutos até a rede Wi‑Fi voltar a aparecer.
14. Ir ao menu **LAN** / **Network**.
15. Definir o **IP do router (Gateway)** como: `192.168.100.1`.
16. Definir a **Máscara** como: `255.255.255.0`.
17. Guardar/Apply/Save.
18. Ir ao menu **DHCP Server**.
19. Confirmar que o DHCP está **ON**.
20. Definir o range DHCP (para não bater com os IPs fixos):
   - Start: `192.168.100.100`
   - End: `192.168.100.200`
21. Guardar/Apply/Save.
22. Se o router reiniciar, voltar a entrar no painel usando `http://192.168.100.1`.

### IPs fixos (ou DHCP reservado)
**Opção A — DHCP reservado (preferido no router):**
1. No painel do router, ir a **LAN** → **DHCP** → **Address Reservation** (ou “Reserva DHCP”).
2. Para cada máquina, adicionar uma reserva com **MAC Address** e **IP**:
   - Henrique (Arch): `192.168.100.10`
   - Ferro (Kali): `192.168.100.20`
   - Duarte (Windows1): `192.168.100.30`
   - Francisco (Windows2): `192.168.100.31`
3. Guardar/Apply/Save.
4. Desligar e voltar a ligar o Wi‑Fi em cada máquina para receber o IP reservado.

**Opção B — IP fixo manual (se não houver reserva):**
1. Confirmar o **Gateway** do router (ex.: `192.168.100.1`).
2. Em cada máquina, definir IP fixo, máscara e gateway:
   - **IP:** conforme tabela acima
   - **Máscara:** `255.255.255.0`
   - **Gateway:** `192.168.100.1`
   - **DNS:** `1.1.1.1` ou `8.8.8.8`

**Comandos para IP fixo no Windows (Duarte/Francisco):**
1. Abrir PowerShell como **Administrador**.
2. Ver o nome da interface Wi‑Fi:
   ```powershell
   Get-NetAdapter | Where-Object {$_.Status -eq "Up"}
   ```
3. Definir IP fixo (substituir `Wi-Fi` se o nome for diferente):
   ```powershell
   # Duarte (Windows1)
   New-NetIPAddress -InterfaceAlias "Wi-Fi" -IPAddress 192.168.100.30 -PrefixLength 24 -DefaultGateway 192.168.100.1
   Set-DnsClientServerAddress -InterfaceAlias "Wi-Fi" -ServerAddresses 1.1.1.1,8.8.8.8

   # Francisco (Windows2)
   New-NetIPAddress -InterfaceAlias "Wi-Fi" -IPAddress 192.168.100.31 -PrefixLength 24 -DefaultGateway 192.168.100.1
   Set-DnsClientServerAddress -InterfaceAlias "Wi-Fi" -ServerAddresses 1.1.1.1,8.8.8.8
   ```

**Comandos para IP fixo no Arch/Kali (Henrique/Ferro):**
1. Confirmar a ligação Wi‑Fi ativa (deve ser `LAB-SERVERS`):
   ```bash
   nmcli -t -f NAME,DEVICE con show --active
   ```
2. Definir IP fixo (a ligação chama-se `LAB-SERVERS`):
   ```bash
   # Henrique (Arch)
   nmcli con mod "LAB-SERVERS" ipv4.addresses 192.168.100.10/24 ipv4.gateway 192.168.100.1 ipv4.dns "1.1.1.1 8.8.8.8" ipv4.method manual
   nmcli con down "LAB-SERVERS" && nmcli con up "LAB-SERVERS"

   # Ferro (Kali)
   nmcli con mod "LAB-SERVERS" ipv4.addresses 192.168.100.20/24 ipv4.gateway 192.168.100.1 ipv4.dns "1.1.1.1 8.8.8.8" ipv4.method manual
   nmcli con down "LAB-SERVERS" && nmcli con up "LAB-SERVERS"
   ```

### Verificação rápida da rede
1. Em cada máquina, confirmar o IP:
   - **Windows (PowerShell):**
     ```powershell
     ipconfig
     ```
   - **Linux (Terminal):**
     ```bash
     ip a
     ```
2. Confirmar que o IP, máscara e gateway batem com o definido.
3. No PC do Henrique, testar ping para todos:
   ```bash
   ping -c 2 192.168.100.20
   ping -c 2 192.168.100.30
   ping -c 2 192.168.100.31
   ```
4. Se algum ping falhar, desligar e ligar o Wi‑Fi dessa máquina e repetir.
5. Confirmar que todos os IPs estão na mesma sub-rede `192.168.100.0/24`.

### Transferência do ficheiro `.hc22000` (Ferro → Henrique)
**Objetivo:** o Henrique ficar com o ficheiro em `hashes/wifi_sample.hc22000` (é o nome que o `orchestrator.py` procura para a demo WPA2).

**No Ferro (Kali):**
1. Confirmar o IP do Kali:
   ```bash
   ip a
   ```
2. Garantir que o SSH está ativo (para permitir `scp`):
   ```bash
   sudo systemctl enable --now ssh
   sudo systemctl status ssh --no-pager
   ```
3. Encontrar o `.hc22000` gerado (o caminho pode variar):
   ```bash
   find "$PWD" -maxdepth 5 -type f -name "*.hc22000" -o -name "*.22000" 2>/dev/null
   ```
   - Se o `wifi_cracker.py` gerar um output com caminho, usar esse.

**No Henrique (Arch):**
1. Criar a pasta de destino (se não existir):
   ```bash
   mkdir -p hashes
   ```
2. Copiar do Ferro para o nome esperado (substituir `CAMINHO_NO_KALI`):
   ```bash
   scp ferro@192.168.100.20:CAMINHO_NO_KALI hashes/wifi_sample.hc22000
   ```
3. Confirmar que o ficheiro existe:
   ```bash
   ls -lh hashes/wifi_sample.hc22000
   ```

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
   .\venv\Scripts\Activate.ps1
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
   *(Ação: carregar ENTER)*
2. Ferro executa o ataque.
   **Comando:**
   ```bash
   python wifi_cracker.py --network "LAB-SERVERS" --monitor wlan0mon
   ```
3. Ao surgir **KEY FOUND**, Henrique confirma no orquestrador.
   *(Ação: escrever `s` e carregar ENTER)*

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
   > "Agora que temos acesso à rede, vamos mostrar duas coisas: (1) como credenciais podem vazar em protocolos inseguros e (2) por que GPU acelera cracking em hashes rápidos."

### 🟠 EXTRA — Benchmark CPU vs GPU (30–60s, automático)
**Objetivo:** mostrar números reais de throughput (sem crackear passwords reais).

**O que acontece:** o `orchestrator.py` executa `hashcat -b` para CPU e para GPU, e imprime o rácio GPU/CPU em MD5/SHA-256/bcrypt.

**Nota de compatibilidade:** em alguns Linux, o hashcat pode não listar *CPU OpenCL* por defeito. Nesse caso aparece `CPU=n/a` e a demo foca-se no throughput da GPU (que continua válido). Para medir CPU com hashcat, instalar um runtime OpenCL CPU (ex.: `pocl-opencl-icd`).

**Falas (Henrique):**
> "Isto não é força bruta num alvo real. É um benchmark do motor de hashing. Em hashes rápidos, a GPU é dezenas/centenas de vezes mais rápida. Em hashes lentos como bcrypt, a diferença reduz porque o algoritmo é desenhado para ser caro por tentativa."

**Onde ver os ficheiros:**
- CSV: `results/.../metrics/benchmark_cpu_gpu.csv`
- Relatório: `results/.../REPORT.md`
   > "Avançamos para a análise de tráfego."

### 🟠 FASE 2 — Captura de Tráfego (3:00–6:00)
**Passos:**
1. Henrique avança para a fase Telnet no orquestrador.
   *(Ação: carregar ENTER)*
2. Francisco inicia a captura no Wireshark.
3. Duarte executa (com o IP real do Francisco).
   **Comando:**
   ```powershell
   python telnet_authenticated_traffic.py --target 192.168.100.31 --user duarte --password Cibersegura --hash-algo plaintext --count 20
   ```
4. Francisco abre **Follow TCP Stream** e aponta o ecrã.

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
