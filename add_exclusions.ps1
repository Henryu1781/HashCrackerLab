# Script para adicionar exclusões ao Windows Defender
# Requer execução como Administrador

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Configurando Exclusões do Windows Defender" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

$paths = @(
    "C:\Users\duart\HashCrackerLab",
    "C:\hashcat",
    "C:\tools",
    "C:\aircrack-ng",
    "C:\Program Files\Wireshark"
)

foreach ($path in $paths) {
    if (Test-Path $path) {
        Write-Host "Adicionando exclusão para: $path" -ForegroundColor Yellow
        try {
            Add-MpPreference -ExclusionPath $path -ErrorAction Stop
            Write-Host "✓ Sucesso" -ForegroundColor Green
        } catch {
            Write-Host "✗ Erro: $_" -ForegroundColor Red
            Write-Host "Certifique-se de executar este script como ADMINISTRADOR." -ForegroundColor Red
        }
    } else {
        Write-Host "Ignorando (caminho não existe): $path" -ForegroundColor DarkGray
    }
}

Write-Host ""
Write-Host "Configuração concluída." -ForegroundColor Cyan
pause