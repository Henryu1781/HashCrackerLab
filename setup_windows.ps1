# Setup script para Windows (Shared Tester)
# Duarte Vilar + Francisco Silva - VM Partilhada

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Hash Cracker Lab - Setup Windows" -ForegroundColor Cyan
Write-Host "Role: Shared Tester" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se e Admin
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "[ERRO] Execute este script como Administrador!" -ForegroundColor Red
    Write-Host "Clique direito no PowerShell e escolha 'Executar como Administrador'" -ForegroundColor Yellow
    pause
    exit 1
}

# Verificar se Chocolatey esta instalado
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "[1/9] Instalando Chocolatey..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
} else {
    Write-Host "[1/9] Chocolatey ja instalado" -ForegroundColor Green
}

Write-Host "[2/9] Instalando Python..." -ForegroundColor Yellow
choco install python -y

Write-Host "[3/9] Instalando Git..." -ForegroundColor Yellow
choco install git -y

Write-Host "[4/9] Instalando Hashcat..." -ForegroundColor Yellow
$hashcatInstalled = $false
try {
    choco install hashcat -y
    $hashcatInstalled = $true
} catch {
    $hashcatInstalled = $false
}

if (-not $hashcatInstalled) {
    $hashcatUrl = "https://hashcat.net/files/hashcat-6.2.6.7z"
    $hashcatZip = "$env:TEMP\hashcat.7z"
    try {
        Invoke-WebRequest -Uri $hashcatUrl -OutFile $hashcatZip -ErrorAction Stop
        choco install 7zip -y
        & "C:\Program Files\7-Zip\7z.exe" x $hashcatZip -o"C:\hashcat" -y 2>$null
        $hashcatInstalled = $true
    } catch {
        Write-Host "Aviso: Falha ao descarregar Hashcat. Pode instalar manualmente depois." -ForegroundColor Yellow
    }
}

if (Test-Path "C:\hashcat") {
    $env:Path += ";C:\hashcat"
    [Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::Machine)
}

Write-Host "[5/9] Instalando Aircrack-ng..." -ForegroundColor Yellow
$aircrackInstalled = $false
try {
    choco install aircrack-ng -y
    if (Get-Command "aircrack-ng" -ErrorAction SilentlyContinue) {
        $aircrackInstalled = $true
    }
} catch {
    $aircrackInstalled = $false
}

if (-not $aircrackInstalled) {
    Write-Host "Tentando instalar Aircrack-ng manualmente via ZIP..." -ForegroundColor Yellow
    $aircrackUrl = "https://download.aircrack-ng.org/aircrack-ng-1.7-win.zip"
    $aircrackZip = "$env:TEMP\aircrack-ng.zip"
    try {
        Invoke-WebRequest -Uri $aircrackUrl -OutFile $aircrackZip -ErrorAction Stop
        if (-not (Test-Path "C:\Program Files\7-Zip\7z.exe")) {
            choco install 7zip -y
        }
        & "C:\Program Files\7-Zip\7z.exe" x $aircrackZip -o"C:\aircrack-ng" -y 2>$null
        
        # Mover binarios para a raiz se estiverem numa subpasta (comum no zip)
        if (Test-Path "C:\aircrack-ng\aircrack-ng-1.7-win\bin") {
             $aircrackBin = "C:\aircrack-ng\aircrack-ng-1.7-win\bin"
             $env:Path += ";$aircrackBin"
             [Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::Machine)
             Write-Host "Aircrack-ng instalado manualmente em $aircrackBin" -ForegroundColor Green
        }
    } catch {
        Write-Host "Aviso: Falha ao descarregar/instalar Aircrack-ng manualmente." -ForegroundColor Yellow
    }
}

Write-Host "[6/9] Instalando Wireshark (inclui tshark)..." -ForegroundColor Yellow
choco install wireshark -y

Write-Host "[7/9] Configurando ambiente Python..." -ForegroundColor Yellow
# Usar --clear para garantir ambiente limpo
python -m venv --clear venv
try {
    & ".\venv\Scripts\Activate.ps1" -ErrorAction Stop
} catch {
    Write-Host "Aviso: Falha ao ativar venv. Pode ativar manualmente depois." -ForegroundColor Yellow
}

try {
    python -m pip install --upgrade pip
} catch {
    Write-Host "Aviso: Falha ao atualizar pip." -ForegroundColor Yellow
}

try {
    pip install -r requirements.txt
} catch {
    Write-Host "Aviso: Falha ao instalar dependencias Python." -ForegroundColor Yellow
}

Write-Host "[8/9] Criando estrutura de diretorios..." -ForegroundColor Yellow
$dirs = @("wordlists", "rules", "captures", "results", "logs", "hashes", "temp")
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

Write-Host "[9/9] Baixando wordlists..." -ForegroundColor Yellow
$rockyouUrl = "https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt"
if (-not (Test-Path "wordlists\rockyou.txt")) {
    try {
        Invoke-WebRequest -Uri $rockyouUrl -OutFile "wordlists\rockyou.txt" -ErrorAction Stop
    } catch {
        Write-Host "Aviso: Falha ao descarregar rockyou.txt. Pode descarregar manualmente depois." -ForegroundColor Yellow
    }
}

if (Test-Path "wordlists\rockyou.txt") {
    try {
        Get-Content "wordlists\rockyou.txt" -Head 10000 | Set-Content "wordlists\rockyou-small.txt" -ErrorAction Stop
    } catch {
        Write-Host "Aviso: Falha ao criar wordlist pequena." -ForegroundColor Yellow
    }
} else {
    Write-Host "Aviso: rockyou.txt nao encontrado." -ForegroundColor Yellow
}

Write-Host ''
Write-Host '========================================' -ForegroundColor Green
Write-Host '   Setup Concluido com Sucesso!        ' -ForegroundColor Green
Write-Host '========================================' -ForegroundColor Green
Write-Host ''
Write-Host 'Proximos passos:' -ForegroundColor Yellow
Write-Host '1. Feche e reabra o PowerShell'
Write-Host '2. Execute: .\venv\Scripts\Activate.ps1'
Write-Host '3. Aguarde instrucoes do orquestrador'
Write-Host ''
Write-Host 'Verificacao Hashcat:' -ForegroundColor Yellow
Write-Host 'C:\hashcat\hashcat.exe -I'
Write-Host ''
pause