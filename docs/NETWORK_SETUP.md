# 📡 Configuração de Rede & Hardware

Este documento detalha o setup físico e lógico necessário para reproduzir os ataques de WiFi e captura de tráfego.

## 🛠️ Hardware Necessário

### 1. Router Alvo
*   **Modelo:** TP-Link Archer C20 v6 (ou equivalente AC750/AC1200)
*   **Função:** Ponto de Acesso (AP) alvo para o ataque WPA2.
*   **Configuração:**
    *   **SSID:** `LAB-SERVERS`
    *   **Password:** `Cibersegura`
    *   **Segurança:** WPA2-PSK (AES)
    *   **WPS:** Desativado (Opcional, mas recomendado para focar no handshake)
    *   **IP LAN:** 192.168.100.1
    *   **DHCP:** Ativado (Range: 192.168.100.100 - 192.168.100.200)

### 2. Adaptador WiFi (Atacante)
*   **Requisito Crítico:** Deve suportar **Packet Injection** e **Monitor Mode**.
*   **Chipsets Recomendados:** Atheros AR9271, Ralink RT3070, Realtek RTL8812AU.
*   **Exemplo:** Alfa AWUS036NHA ou similar.
*   **Uso:** Ligado ao Kali Linux (Ferro) para executar o `airodump-ng` e `aireplay-ng`.

### 3. Switch / Cablagem (Opcional)
*   Os PCs "Duarte" (Windwos) e "Francisco" (Windows) devem estar ligados à mesma rede que o Router, seja via WiFi ou Cabo Ethernet, para que os pacotes Telnet trafeguem e possam ser sniffados.

---

## 🌐 Topologia da Rede

```mermaid
graph TD
    Router[TP-Link Archer C20<br/>SSID: LAB-SERVERS<br/>Pass: Cibersegura]
    
    Kali[Kali Linux (Ferro)<br/>WiFi Setup<br/>Antena Monitor Mode] -.- Router
    
    Win1[Windows (Duarte)<br/>Gera Tráfego Telnet<br/>IP: 192.168.100.30] --- Router
    
    Win2[Windows (Francisco)<br/>Analisa Wireshark<br/>IP: 192.168.100.31] --- Router
    
    Arch[Arch Linux (Henrique)<br/>Orchestrator<br/>GPU Cracking] -.- Router
```

## ⚙️ Procedimento de Configuração

1.  **Reset ao Router:** Garanta que o router está com configurações limpas.
2.  **Configurar SSID:** Aceda a `192.168.0.1` (ou padrão) e mude o nome da rede wireless para `LAB-SERVERS`.
3.  **Definir Senha:** Aceda a Wireless Security e defina WPA/WPA2 - Personal, com password `Cibersegura`.
4.  **Conectar Clientes:**
    *   Duarte e Francisco conectam-se à rede `LAB-SERVERS`.
    *   Faz ping entre as máquinas para validar visibilidade (`ping 192.168.100.x`).

## 🛑 Validação
Para confirmar que o hardware está pronto:
1.  **No Kali:** `iwconfig` deve mostrar a interface wlan0.
2.  **No Kali:** `sudo airmon-ng start wlan0` deve ativar o modo monitor.
3.  **No Windows:** Conectividade estável com o Router.

