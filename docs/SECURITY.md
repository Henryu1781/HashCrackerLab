# Segurança e Ética

## Princípios

- Uso exclusivo em LAB isolado e autorizado.
- Nunca utilizar em redes reais/produção.
- Utilizar apenas dados sintéticos/consentidos.
- Minimizar retenção de artefactos sensíveis.
- Executar limpeza após os testes.

## Leitura recomendada

- Para detalhe sobre dados sensíveis, limpeza e auditoria: [SECURITY_GUIDE.md](SECURITY_GUIDE.md)

## Checklist de Isolamento

- Router sem WAN
- Sem gateway/DNS configurados
- `ip route` sem rota default (Linux)
