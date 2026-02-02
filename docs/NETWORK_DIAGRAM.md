# Diagrama de Rede (LAB)

```
                           Router (LAB)
                     (WAN desligada / isolado)
                               |
        -------------------------------------------------
        |                     |               |        |
   PC1 (Arch)            PC2 (Kali)       PC3 (Windows) PC4 (Windows)
 Orquestrador + GPU   Monitorização +     Comunicação   Comunicação
   192.168.100.10      CPU + Antena       192.168.100.30 192.168.100.40
                        192.168.100.20
```

## Notas

- Sem gateway/DNS em todas as máquinas.
- Antena WiFi dedicada no PC2 (Kali).
- Comunicação gerada nos PCs Windows (PC3/PC4).
