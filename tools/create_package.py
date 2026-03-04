#!/usr/bin/env python3
import zipfile
from pathlib import Path
import fnmatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / f"HashCrackerLab_delivery_{__import__('datetime').datetime.now().strftime('%Y%m%d')}.zip"
EXCLUDE = [
    'wordlists', '.venv', 'venv', '__pycache__', '.git', '.gitignore', 'results', '*.pyc', '*.pyo'
]
INCLUDE = ['README.md', 'CHANGES.md', 'LICENSE', 'requirements.txt', 'setup_arch.sh', 'setup_kali.sh', 'setup_windows.ps1', 'docs', 'src', 'config', 'rules', 'tools', 'orchestrator.py', 'full_integration_orchestrator.py', 'wifi_cracker.py', 'telnet_authenticated_traffic.py']

with zipfile.ZipFile(OUT, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for item in INCLUDE:
        path = ROOT / item
        if not path.exists():
            continue
        if path.is_file():
            z.write(path, path.relative_to(ROOT))
        else:
            for p in path.rglob('*'):
                rel = p.relative_to(ROOT)
                skip = False
                for ex in EXCLUDE:
                    if fnmatch.fnmatch(str(rel), ex) or ex in str(rel).split('/'):
                        skip = True
                        break
                if skip:
                    continue
                if p.is_file():
                    z.write(p, rel)
print('Pacote gerado em', OUT)
