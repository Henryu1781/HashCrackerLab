# Projeto Final - Hash Cracker

![License](https://img.shields.io/github/license/Henryu1781/HashCrackerLab)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Last Commit](https://img.shields.io/github/last-commit/Henryu1781/HashCrackerLab)

## ⚠️ Aviso Importante (Windows)

Este projeto utiliza ferramentas de segurança (Hashcat, Aircrack-ng) que são frequentemente detetadas como **falsos positivos** por antivírus.

**Antes da instalação no Windows:**
1. Execute `Set-ExecutionPolicy -Scope Process Bypass` no PowerShell (Admin).
2. Execute o script de exclusões: `.\add_exclusions.ps1` (Admin).
3. Ou adicione exclusões manuais para `C:\hashcat`, `C:\tools` e a pasta do projeto.

---

## Autoria
**Henrique Carvalho (2024047)** | **Gonçalo Ferro (2024091)**  
**Duarte Vilar (2024187)** | **Francisco Silva (2024095)**

---

## Índice

1. [Instalação Rápida](#-instalação-rápida)
2. [Implementação da Solução](#11-implementação-da-solução)
   - [Componentes Implementados](#componentes-implementados)
3. [Testes Realizados](#12-testes-realizados)
   - [Testes Unitários](#121-testes-unitários)
   - [Testes de Integração](#122-testes-de-integração)
   - [Testes de Aceitação (UAT)](#123-testes-de-aceitação-uat)
   - [Testes de Segurança e Limpeza](#124-testes-de-segurança-e-limpeza)
4. [Resultados Obtidos](#13-resultados-obtidos)
5. [Manual de Instalação e Utilização](#14-manual-de-instalação-e-utilização-resumo)
6. [Changelog](#15-changelog-decisões-técnicas-relevantes)
7. [Documentação](#-documentação-importante)

### 📚 Documentação Importante

- **[QUICKSTART.md](QUICKSTART.md)** - 🚀 Guia rápido para começar (Ler Primeiro!)
- **[TUTORIAL.md](TUTORIAL.md)** - 📖 Tutorial passo-a-passo detalhado
- **[AUDIT_REPORT.md](AUDIT_REPORT.md)** - Auditoria completa do projeto
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - 🔧 Resolução de problemas comuns
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Arquitetura e sistema de configuração
- **[docs/SECURITY_GUIDE.md](docs/SECURITY_GUIDE.md)** - Guia de segurança e dados sensíveis

---

## 🚀 Instalação Rápida

Consulte o [QUICKSTART.md](QUICKSTART.md) para instruções detalhadas.

### Windows (PowerShell Admin)
```powershell
# 1. Configurar Exclusões (Vital para Hashcat/Aircrack)
.\add_exclusions.ps1

# 2. Instalar Dependências e Ferramentas
.\setup_windows.ps1

# 3. Ativar e Validar
.\venv\Scripts\Activate.ps1
python tools/validate_environment.py
```

### Linux (Arch/Kali)
```bash
chmod +x setup_arch.sh setup_kali.sh
./setup_arch.sh  # ou ./setup_kali.sh
source venv/bin/activate
python tools/validate_environment.py
```

---

## Overview

O Hash Cracker Lab é um ambiente educacional para estudar segurança de passwords em LAB isolado.
Inclui geração controlada de hashes, cracking automatizado, métricas e limpeza segura.

### Screenshots

- Adicione capturas em `docs/assets/` (ex.: `docs/assets/report.png`).
- Referencie-as aqui para demonstrar o relatório e as métricas.

---

## 1.1 Implementação da Solução

Nesta fase foi implementada a solução definida nas fases anteriores, respeitando os requisitos funcionais e não-funcionais, bem como as políticas de segurança, isolamento e ética.

A implementação foi realizada num ambiente LAB isolado, recorrendo exclusivamente a máquinas virtuais e dados sintéticos ou autorizados, garantindo total conformidade legal e institucional.

### Arquitetura da Rede LAB

Para isto criámos uma rede LAN que consistiu em **3 máquinas virtuais**:

1. **VM Orquestrador + GPU** (Henrique Carvalho)
   - Coordenação e gestão de experiências
   - Testes de cracking acelerados por GPU
   
2. **VM Monitorização + CPU Tester** (Gonçalo Ferro)
   - Testes de cracking baseados em CPU
   - Monitorização e captura (Kali)
   
3. **VM Comunicação (Windows + VM Kali)** (Duarte Vilar + Francisco Silva)
   - Comunicação/geração de tráfego no LAB
   - Apoio aos testes e validação

### Topologia Atual (3 PCs)

1. **Arch (Orquestrador + GPU) — Henrique**
   - Execução do orquestrador
   - Geração de hashes e cracking acelerado

2. **Kali (Monitorização + Deauth) — Ferro**
   - Antena WiFi RTL8812AU em modo monitor
   - Captura de handshakes e deauth controlado (LAB)

3. **Windows + VM Kali (Comunicação) — Duarte + Francisco**
   - Geração de comunicações na rede LAB
   - VM Kali dedicada a comunicações e validação de captura (LAB)

### Componentes Implementados

#### Orquestrador

**Scripts em Python e Bash:**
- Wordlists
- Parsing de configuração (YAML) e agregação automática de métricas
- Exportação de resultados em `.cap`

#### Geração de Hashes

Implementação de geração controlada de hashes para:
- Argon2
- bcrypt
- scrypt
- PBKDF2
- SHA-256
- SHA-1
- MD5

Cada hash inclui metadados:
- algoritmo
- salt
- cost factor / iterações
- timestamp
- identificador anónimo

#### Execução de Cracking

Integração com:
- **Hashcat**
- **Aircrack/Airodump**

Modos implementados:
- Dictionary attack
- Rule-based attack
- Brute-force (limitado)
- GPU-accelerated cracking (quando disponível)
- Execução em VMs separadas (CPU / GPU) *(ainda a implementar)*

#### Gestão de Wordlists

Wordlists tratadas e controladas:
- Geração com CEWL
- Remoção de dados reais (emails, nomes próprios)
- Aplicação automática de regras de mutação

#### Monitorização e Logging

- Captura de tráfego em LAB Wi-Fi com Wireshark
- Logging detalhado:
  - comandos executados
  - parâmetros usados
  - tempos de execução
  - percentagem de recuperação
- Logs exportados em CSV/JSON para auditoria

---

## 1.2 Testes Realizados

Os testes foram executados conforme o Plano de Testes definido na Fase 2, cobrindo testes unitários, integração, aceitação e segurança.

**Nota:** Ainda estamos com um problema menor na captura do handshake, durante o deauth. Está atualmente a ser resolvido.

Comparamos a performance do `wifite` com `aircrack`, e por agora mantemo-nos com o segundo.

### 1.2.1 Testes Unitários

**Objetivo:** validar componentes isolados.

**Exemplos executados:**
- Geração de N hashes com parâmetros válidos
- Validação de schema dos ficheiros YAML
- Parsing correto dos outputs do Hashcat/John

**Resultados:**
- Nenhuma falha crítica detetada
- Quase perfeito ✓

### 1.2.2 Testes de Integração

**Objetivo:** validar o fluxo completo do sistema.

**Fluxos testados:**
- Geração de hashes → cracking → recolha de métricas → exportação
- Execução em CPU e GPU (quando disponível)
- Integração entre Orquestrador e Cracking VMs
- Captura de tráfego em ambiente Wi-Fi LAB

**Resultados:**
- Pipeline executado corretamente sem perda de dados ✓
- Resultados consistentes entre execuções com mesma seed/configuração ✓
- Isolamento de rede confirmado (sem acesso à Internet) ✓

### 1.2.3 Testes de Aceitação (UAT)

**Objetivo:** validar as user stories definidas.

**Cenário principal:**
```bash
run_experiment --config ex1.yaml
```

**Critérios verificados:**
- Geração automática de hashes ✓
- Execução controlada de cracking ✓
- Relatório final com métricas claras ✓
- Logs e artefactos armazenados corretamente ✓
- Execução bloqueada quando não existe consentimento (quando aplicável) ✓

**Resultado:**
Todas as user stories consideradas satisfeitas.

### 1.2.4 Testes de Segurança e Limpeza

#### Isolamento
- Verificação de rotas (`route -n`) e firewall (`iptables`)
- Confirmação de ausência de tráfego externo

#### Limpeza
- Execução do script `cleanup.sh`
- Remoção segura de:
  - hashes originais
  - logs sensíveis
  - artefactos temporários
- Geração de checksum e log de auditoria da limpeza

---

## 1.3 Resultados Obtidos

Os testes demonstraram claramente que:

- **Algoritmos modernos** com salt e cost elevado (Argon2, bcrypt, scrypt) apresentam resistência significativamente superior
- **Algoritmos obsoletos** (MD5, SHA-1) são rapidamente comprometidos
- **Rule-based attacks** aumentam substancialmente a taxa de sucesso face a dictionary simples
- A utilização de **GPU** reduz drasticamente o tempo de cracking
- Políticas de complexidade e **MFA** são fundamentais para mitigação

---

## 1.4 Manual de Instalação e Utilização (Resumo)

### Instalação
```bash
./setup_lab.sh
```

### Execução imediata (1 comando)
```bash
python tools/run_immediate.py
```
Se o Hashcat não estiver instalado, a execução passa automaticamente para `--dry-run`.

### Testes LAB (WiFi + Tráfego)

**Captura de handshake (Kali):**
```bash
sudo tools/capture_handshake.sh -s "LAB-SERVERS" -i wlan0 -t 60 -d 10
```

**Tráfego tipo Telnet:**
Servidor:
```bash
python tools/generate_telnet_traffic.py --server --host 0.0.0.0 --port 2323
```
Cliente:
```bash
python tools/generate_telnet_traffic.py --client --host 192.168.100.10 --port 2323 --user labuser --password labpass
```

### Execução
```bash
run_experiment --config ex1.yaml
```

### Automatização e Reprodutibilidade

- Use sempre configurações YAML versionadas em [config/](config/)
- Defina `seed` e, se necessário, `deterministic_salts: true` para resultados reprodutíveis
- Execute validações e testes unitários antes de cada experimento

### Limpeza
```bash
./cleanup.sh
```

### Testes Unitários

```bash
pytest
```

---

## 1.5 Changelog (Decisões Técnicas Relevantes)

- Adoção de YAML para garantir reprodutibilidade
- Separação física de VMs para cracking e orquestração
- Limitação de brute-force para evitar consumo excessivo
- Logging detalhado para auditabilidade e avaliação académica
- Implementação obrigatória de limpeza pós-testes

---

**Data de conclusão:** Fevereiro 2026

## Documentação

- [docs/README.md](docs/README.md)
- [docs/LAB_SETUP_4PCS.md](docs/LAB_SETUP_4PCS.md)
- [docs/EXECUTION_GUIDE.md](docs/EXECUTION_GUIDE.md)
- [docs/CHECKLIST.md](docs/CHECKLIST.md)
- [docs/NETWORK_DIAGRAM.md](docs/NETWORK_DIAGRAM.md)
- [docs/FAQ.md](docs/FAQ.md)
- [docs/SECURITY.md](docs/SECURITY.md)
