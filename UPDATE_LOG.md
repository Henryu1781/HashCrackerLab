# Log de Atualizações do Projeto

## [2026-02-08] - Finalização para Apresentação
### Adicionado
- **Demo Visual de Força Bruta**: Implementada no `orchestrator.py` para visualizar a tentativa sequencial de PINs (0000-9999).
- **Benchmark GPU WPA2**: Adicionado modo 22000 (PMKID/EAPOL) ao orchestrator para demonstrar velocidade da GPU.
- **Master Script**: Criado `GUIA_DA_APRESENTACAO.md` com falas e timeline passo-a-passo.

### Corrigido
- **Documentação Telnet**: Alinhado com servidor fake obrigatório e alvo por IP direto.
- **Links de Docs**: Removidos links para ficheiros inexistentes e adicionados os corretos.
- **Typos**: Correção de "Windwos" em `docs/NETWORK_SETUP.md`.

### Alterado
- **Configuração**: `config/projeto_final_ciberseguranca.yaml` atualizado com regras específicas para garantir sucesso na demo.
- **Orquestração**: `full_integration_orchestrator.py` refinado para incluir pausas estratégicas para explicação.
- **Wordlists**: Adicionadas entradas "hashcat!" e "Cibersegura" ao dicionário customizado.
