# ❓ Perguntas & Respostas (Q&A da Apresentação)

Este ficheiro contém perguntas prováveis e respostas curtas e seguras para a demo.

---

## ✅ Perguntas Gerais

**1) O que vocês estão a demonstrar?**
> Estamos a mostrar como configurações fracas (WiFi e Telnet) expõem credenciais e como isso pode ser mitigado.

**2) Isto é um ataque real?**
> É uma demonstração controlada num laboratório, com permissões e credenciais de teste.

**3) Qual é o objetivo educativo?**
> Mostrar o risco prático de protocolos inseguros e a necessidade de boas práticas.

**4) Isto funciona em qualquer rede?**
> Apenas em redes onde há autorização e vulnerabilidades semelhantes.

---

## 📶 WiFi (WPA2 / Handshake)

**5) Como é que a password do WiFi foi obtida?**
> Capturámos o handshake e fizemos um ataque por dicionário. Se a password for fraca, é recuperada.

**6) WPA2 não é seguro?**
> WPA2 é seguro quando a password é forte e o WPS está desativado. O problema é a password fraca.

**7) Como se mitiga isto?**
> Password longa e aleatória, WPS desativado e WPA2/WPA3 com boas políticas.

---

## 🌐 Telnet (Tráfego em Claro)

**8) Porque é que as credenciais aparecem em claro?**
> Porque Telnet não cifra dados. Tudo vai em plaintext na rede.

**9) Qual a alternativa segura ao Telnet?**
> SSH, que cifra o tráfego e protege credenciais.

**10) Como posso verificar se alguém usa Telnet na minha rede?**
> Monitorização de tráfego e deteção de conexões na porta 23.

---

## ⚡ GPU Cracking

**11) Porque é que a GPU é mais rápida?**
> A GPU faz muitos cálculos em paralelo, ideal para operações repetitivas de hashing.

**12) O cracking é sempre rápido?**
> Depende da força da password e do tipo de ataque. Passwords fortes resistem muito mais.

---

## 🛡️ Boas Práticas

**13) O que recomendaram no final?**
> Passwords fortes, protocolos seguros (SSH), WPA2/WPA3 bem configurado e monitorização contínua.

**14) Isto viola leis?**
> Só é ilegal se for feito sem autorização. Aqui é uma demo com permissão explícita.

---

## 🧪 Sobre o Lab

**15) Isto corre em casa?**
> Sim, desde que usem hardware compatível e tenham autorização para testar a rede.

**16) Quanto tempo demora a demo?**
> A versão curta demora ~8 minutos. A versão completa segue o modo lab do orquestrador.
