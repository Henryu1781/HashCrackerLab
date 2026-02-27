# WiFi Handshake Capture - Melhorias Implementadas

## Data: 27 Fevereiro 2026

### Problemas Identificados
1. **Airodump não salvava em formato CAP** - estava usando CSV format
2. **Deauth ineficaz** - pacotes insuficientes e sem broadcast correto
3. **Timing inadequado** - intervalos muito curtos entre ações
4. **Detecção de handshake fraca** - validação incompleta do arquivo capturado

### Soluções Implementadas

#### 1. **Melhor Captura de Arquivo CAP**
```
✓ Adicionado --output-format cap ao airodump-ng
✓ Caminho correto do arquivo: {capture_file}.cap
✓ Sanitização de nomes de rede para evitar erros de ficheiro
```

#### 2. **Deauth Attack Melhorado**
```
✓ Novo método detect_clients() - encontra MACs dos clientes conectados
✓ Deauth broadcast + deauth direcionado para cada cliente
✓ 4 rondas de ataque (antes era 3) com 15 pacotes cada
✓ Timing otimizado: espera incremental entre rondas (3s, 4s, 5s)
✓ Melhor feedback visual do progresso
```

#### 3. **Captura Estruturada em Fases**
```
Fase 1: Detectar clientes conectados ao AP
Fase 2: Iniciar captura com airodump-ng  
Fase 3: Enviar deauth attack (broadcast + direcionado)
Fase 4: Aguardar e validar handshake capturado
```

#### 4. **Validação Robusta de Handshake**
```
✓ Verifica tamanho de arquivo (> 5000 bytes)
✓ Usa aircrack-ng com opções específicas para detectar WPA
✓ Reports periódicos do progresso a cada 5 segundos
✓ Sugestões de troubleshooting se falhar
```

#### 5. **Help Melhorado**
```
✓ Timeout padrão aumentado: 120s → 180s
✓ Exemplos práticos de uso
✓ Dicas para melhorar captura:
  - Aproximar-se do router
  - Aumentar potência da interface
  - Timeout maior para redes com poucos clientes
```

### Mudanças no Código

#### Arquivo: `wifi_cracker.py`

**Nova Função: `detect_clients()`**
- Escaneia para encontrar MACs dos clientes conectados ao AP
- Usar esses MACs para deauth mais direcionado

**Função Atualizada: `capture_handshake()`**
- Estrutura em 4 fases bem definidas
- Detecção de clientes antes de deauth
- Validação melhorada de handshake com aircrack-ng
- Mensagens de progresso a cada 5 segundos
- Sugestões de troubleshooting em caso de falha

**Função Atualizada: `deauth_attack()`**
- Novo parâmetro `clients` para deauth direcionado
- Broadcast deauth + deauth para cada cliente
- Logging melhorado do output
- Timing otimizado entre rondas

**Parser Atualizado:**
- Timeout padrão: 180s (antes 120s)
- Help epilog com exemplos e dicas

### Como Usar

#### Captura com Deauth (modo completo):
```bash
# Com timeout aumentado (3min) para maior chance de sucesso
python wifi_cracker.py --full --network "LAB-SERVERS" --timeout 300

# Apenas captura (sem cracking)
python wifi_cracker.py --capture --network "LAB-SERVERS" --timeout 180

# Deauth standalone para testar
python wifi_cracker.py --deauth --bssid AA:BB:CC:DD:EE:FF
```

### Melhorias Esperadas
- ✅ Handshake capturado com mais eficiência
- ✅ Taxa de sucesso aumentada especialmente com clientes conectados
- ✅ Feedback visual melhorado durante a operação
- ✅ Melhor diagnóstico se algo falhar

### Troubleshooting

Se o handshake ainda não for capturado:

1. **Verificar sinal**: Aproximar-se do AP
```bash
sudo iwconfig wlan00mon
```

2. **Aumentar potência**:
```bash
sudo iw dev wlan00mon set txpower fixed 30
```

3. **Usar timeout maior**:
```bash
python wifi_cracker.py --capture --network "LAB-SERVERS" --timeout 600
```

4. **Forçar cliente a conectar**: 
   - Conecte um cliente manualmente à rede WiFi
   - Execute o script durante a reconexão

5. **Testar canal específico**:
```bash
python wifi_cracker.py --capture --network "LAB-SERVERS" --channel 6 --timeout 300
```

### Compatibilidade
- ✅ Python 3.6+
- ✅ aircrack-ng (airodump-ng, aireplay-ng)
- ✅ Linux/Kali com suporte a monitor mode
- ✅ Interface WiFi capaz de monitor mode

---

**Status**: ✅ OPERACIONAL - Testes com sucesso em LAB-SERVERS
