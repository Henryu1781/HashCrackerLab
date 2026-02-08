#!/usr/bin/env python3
"""
Cleanup Script - Platform Independent
Removes results, logs, and temporary files.
"""
import shutil
import os
import sys
from pathlib import Path

def cleanup():
    print("="*40)
    print(" Hash Cracker Lab - Cleanup")
    print("="*40)
    
    confirm = input("Are you sure you want to delete ALL results and captures? (y/N): ")
    if confirm.lower() != 'y':
        print("Cancelled.")
        return

    root = Path(__file__).parent.parent
    targets = [
        root / 'results',
        root / 'captures',
        root / 'logs',
        root / 'hashes',
        root / 'temp'
    ]
    
    pycache_found = list(root.rglob('__pycache__'))
    
    print("\nCleaning directories...")
    for target in targets:
        if target.exists():
            try:
                # Remove content but keep dir
                for item in target.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                print(f"[OK] Cleaned {target.name}/")
            except Exception as e:
                print(f"[ERR] {target.name}: {e}")
        else:
            print(f"[SKIP] {target.name} (not found)")
            
    print("\nCleaning pycache...")
    for p in pycache_found:
        try:
            shutil.rmtree(p)
        except:
            pass
    print(f"[OK] Removed {len(pycache_found)} pycache folders")
    
    print("\nCleanup Complete!")

if __name__ == "__main__":
    cleanup()
