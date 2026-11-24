"""Kontrolli për dorëzim: sintaksa, testet dhe rezultatet eksperimentale të ruajtura."""
import argparse
import ast
from pathlib import Path
import subprocess
import sys


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pa-gui',action='store_true',help='Mos ekzekuto testet që kërkojnë ekran.')
    args=parser.parse_args()
    folder=Path(__file__).resolve().parent
    for path in sorted(folder.glob('*.py')):
        ast.parse(path.read_text(encoding='utf-8-sig'),filename=str(path))
    print('Sintaksa e skedarëve Python është në rregull.',flush=True)
    modules=[p.stem for p in sorted(folder.glob('test_*.py'))
             if not args.pa_gui or p.stem!='test_gui']
    result=subprocess.run([sys.executable,'-B','-m','unittest','-v',*modules],cwd=folder)
    if result.returncode:
        return result.returncode
    result=subprocess.run([sys.executable,'-B',str(folder/'verifiko_rezultatet.py')],cwd=folder)
    if result.returncode:
        return result.returncode
    print('Kontrolli përfundoi me sukses. Eksperimentet nuk u riekzekutuan dhe të dhënat nuk u mbishkruan.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
