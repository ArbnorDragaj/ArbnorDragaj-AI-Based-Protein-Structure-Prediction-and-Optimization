"""Eksport i rezultateve pa ndryshuar strukturat e llogaritura."""
import csv
import io
import os
from pathlib import Path
import tempfile
from proteina import valide, sekuenca_e_sakte


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
