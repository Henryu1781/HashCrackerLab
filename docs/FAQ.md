# FAQ

## Posso usar isto fora do LAB?
Não. Este projeto é apenas para uso educacional em ambiente LAB isolado e autorizado.

## Preciso de GPU?
Não. A GPU acelera o cracking, mas o modo CPU funciona.

## Não tenho Hashcat. O que fazer?
Use `python tools/run_immediate.py`. Ele entra automaticamente em `--dry-run`.

## No Windows dá erro de antivírus / bloqueio. O que fazer?

1. Execute PowerShell como Administrador.
2. Corra `add_exclusions.ps1`.
3. Reabra PowerShell e volte a validar com `python tools/validate_environment.py`.

## Como validar o ambiente?
Execute `python tools/validate_environment.py` em cada máquina.

## Onde ficam os resultados?
Em `results/*/REPORT.md` e `results/*/metrics/`.

## Como sei se a rede está mesmo isolada?

- Linux: `ip route` não deve ter `default via`.
- Windows: `route print | findstr 0.0.0.0` deve estar vazio (ou não apontar para Internet).
