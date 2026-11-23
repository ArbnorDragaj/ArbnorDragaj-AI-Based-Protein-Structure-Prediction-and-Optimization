"""Eksport i rezultateve pa ndryshuar strukturat e llogaritura."""
import csv
import io
import json
from dataclasses import asdict
from datetime import datetime, timezone
import os
from pathlib import Path
import tempfile
from proteina import valide, sekuenca_e_sakte, energjia


def shkruaj_atomik(path, text):
    path = Path(path)
    with tempfile.NamedTemporaryFile(dir=path.parent, mode='w', encoding='utf-8',
                                     newline='', delete=False) as f:
        temporary = Path(f.name)
        try:
            f.write(text)
        except BaseException:
            f.close()
            temporary.unlink(missing_ok=True)
            raise
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def kontrollo_rezultatet(results):
    if not results:
        raise ValueError('Nuk ka rezultate për eksport.')
    for r in results:
        sekuenca_e_sakte(r.sekuenca)
        if not valide(r.pikat, len(r.sekuenca)):
            raise ValueError('Struktura e pavlefshme nuk eksportohet.')


def eksporto_koordinatat(path, results):
    kontrollo_rezultatet(results)
    buffer = io.StringIO(newline='')
    writer = csv.writer(buffer)
    writer.writerow(('algoritmi','indeksi','aminoacidi','x','y','z'))
    for r in results:
        for i,(aa,p) in enumerate(zip(r.sekuenca,r.pikat),1):
            writer.writerow((r.algoritmi,i,aa,*p))
    shkruaj_atomik(path, buffer.getvalue())


def eksporto_json(path, results, config, memories=None):
    kontrollo_rezultatet(results)
    for r in results:
        if r.energjia != energjia(r.sekuenca,r.pikat,config['pesha']):
            raise ValueError('Energjia nuk përputhet me strukturën dhe peshën e ruajtur.')
    payload = {'versioni':1, 'modeli':'HP në rrjetë kubike 3D',
               'koha_eksportit_utc':datetime.now(timezone.utc).isoformat(),
               'parametrat':config,'rezultatet':[asdict(r) for r in results],
               'memoria_python':memories,
               'shenim':'Model edukativ; memoria matet në ekzekutim të veçantë.'}
    shkruaj_atomik(path,json.dumps(payload,ensure_ascii=False,indent=2,allow_nan=False))
