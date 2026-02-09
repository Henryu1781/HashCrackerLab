# Script para adicionar exclusoes ao Windows Defender
# Requer execucao como Administrador

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Configurando exclusoes do Windows Defender" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

$paths = @(
    "${env:USERPROFILE}\HashCrackerLab",
    "${env:USERPROFILE}\HashCrackerLab\hashcrackerlab",
    "C:\hashcat",
    "C:\tools",
    "C:\aircrack-ng",
    "C:\Program Files\Wireshark"
)

foreach ($path in $paths) {
    if (Test-Path $path) {
        Write-Host "Adicionando exclusao para: $path" -ForegroundColor Yellow
        try {
            Add-MpPreference -ExclusionPath $path -ErrorAction Stop
            Write-Host "Sucesso" -ForegroundColor Green
        } catch {
            Write-Host "Erro: $_" -ForegroundColor Red
            Write-Host "Certifique-se de executar este script como ADMINISTRADOR." -ForegroundColor Red
        }
    } else {
        Write-Host "Ignorando (caminho nao existe): $path" -ForegroundColor DarkGray
    }
}

Write-Host ""
Write-Host "Configuracao concluida." -ForegroundColor Cyan
pause