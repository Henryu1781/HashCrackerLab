# FAQ

## Posso usar isto fora do LAB?
Não. Este projeto é apenas para uso educacional em ambiente LAB isolado.

## Preciso de GPU?
Não. A GPU acelera o cracking, mas o modo CPU funciona.

## Não tenho Hashcat. O que fazer?
Use `python tools/run_immediate.py`. Ele entra automaticamente em `--dry-run`.

## Como validar o ambiente?
Execute `python tools/validate_environment.py` em cada máquina.

## Onde ficam os resultados?
Em `results/*/REPORT.md` e `results/*/metrics/`.
