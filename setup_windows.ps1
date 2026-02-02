# Setup script para Windows (Shared Tester)
# Duarte Vilar + Francisco Silva - VM Partilhada

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Hash Cracker Lab - Setup Windows" -ForegroundColor Cyan
Write-Host "Role: Shared Tester" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se é Admin
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[ERRO] Execute este script como Administrador!" -ForegroundColor Red
    Write-Host "Clique direito no PowerShell e escolha 'Executar como Administrador'" -ForegroundColor Yellow
    pause
    exit 1
}

# Verificar se Chocolatey está instalado
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "[1/8] Instalando Chocolatey..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
} else {
    Write-Host "[1/8] Chocolatey já instalado ✓" -ForegroundColor Green
}

Write-Host "[2/8] Instalando Python..." -ForegroundColor Yellow
choco install python -y

Write-Host "[3/8] Instalando Git..." -ForegroundColor Yellow
choco install git -y

Write-Host "[4/8] Instalando Hashcat..." -ForegroundColor Yellow
# Download Hashcat
$hashcatUrl = "https://hashcat.net/files/hashcat-6.2.6.7z"
$hashcatZip = "$env:TEMP\hashcat.7z"
Invoke-WebRequest -Uri $hashcatUrl -OutFile $hashcatZip
choco install 7zip -y
& "C:\Program Files\7-Zip\7z.exe" x $hashcatZip -o"C:\hashcat" -y

# Adicionar ao PATH
$env:Path += ";C:\hashcat"
[Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::Machine)

Write-Host "[5/8] Instalando Wireshark..." -ForegroundColor Yellow
choco install wireshark -y

Write-Host "[6/8] Configurando ambiente Python..." -ForegroundColor Yellow
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "[7/8] Criando estrutura de diretórios..." -ForegroundColor Yellow
$dirs = @("wordlists", "rules", "captures", "results", "logs", "hashes", "temp")
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

Write-Host "[8/8] Baixando wordlists..." -ForegroundColor Yellow
$rockyouUrl = "https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt"
if (-not (Test-Path "wordlists\rockyou.txt")) {
    Invoke-WebRequest -Uri $rockyouUrl -OutFile "wordlists\rockyou.txt"
}

# Criar versão pequena
Get-Content "wordlists\rockyou.txt" -Head 10000 | Set-Content "wordlists\rockyou-small.txt"

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   Setup Concluído com Sucesso! ✓      ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "Próximos passos:" -ForegroundColor Yellow
Write-Host "1. Feche e reabra o PowerShell"
Write-Host "2. Execute: .\venv\Scripts\Activate.ps1"
Write-Host "3. Aguarde instruções do orquestrador"
Write-Host ""
Write-Host "Verificação Hashcat:" -ForegroundColor Yellow
Write-Host "C:\hashcat\hashcat.exe -I"
Write-Host ""
pause
