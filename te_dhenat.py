"""Lexim i sekuencave lokale; nuk hiqen aminoacide të panjohura në heshtje."""
import csv
from pathlib import Path
from proteina import sekuenca_e_sakte


def lexo_fasta(path):
    emri, pjeset = None, []
    with open(path, encoding='utf-8-sig') as f:
        for nr, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if emri is not None:
                    yield {'id': emri, 'sekuenca': sekuenca_e_sakte(''.join(pjeset))}
                emri, pjeset = line[1:].strip(), []
                if not emri:
                    raise ValueError(f'FASTA: mungon identifikuesi në rreshtin {nr}.')
            elif emri is None:
                raise ValueError(f'FASTA: pritet titulli > përpara rreshtit {nr}.')
            else:
                pjeset.append(line)
    if emri is None:
        raise ValueError('Skedari FASTA është bosh.')
    yield {'id': emri, 'sekuenca': sekuenca_e_sakte(''.join(pjeset))}


def lexo_csv(path, kolona=None):
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        if len(set(headers)) != len(headers):
            raise ValueError('CSV ka emra kolonash të përsëritur.')
        columns = [h for h in headers if h.strip().lower() in ('sequence','seq','sekuenca')]
        if kolona is None:
            if len(columns) != 1:
                raise ValueError('CSV duhet një kolonë sequence, seq ose sekuenca; ose cakto kolonën.')
            kolona = columns[0]
        if kolona not in headers:
            raise ValueError(f'Kolona {kolona!r} nuk gjendet në CSV.')
        id_col = next((h for h in headers if h.strip().lower() in ('id','pdb_id','name')), None)
        count = 0
        for count, row in enumerate(reader, 1):
            if None in row or row.get(kolona) is None:
                raise ValueError(f'CSV: rreshti {reader.line_num} ka numër të gabuar fushash.')
            try:
                sequence = sekuenca_e_sakte(row[kolona])
            except ValueError as error:
                raise ValueError(f'CSV, rreshti {reader.line_num}: {error}') from error
            yield {'id': (row.get(id_col) or str(count)).strip() or str(count), 'sekuenca': sequence}
        if not count:
            raise ValueError('CSV nuk ka sekuenca.')


def lexo_sekuencat(path, kolona=None):
    suffix = Path(path).suffix.lower()
    if suffix == '.csv':
        yield from lexo_csv(path, kolona)
    elif suffix in ('.fa', '.fasta', '.faa'):
        yield from lexo_fasta(path)
    else:
        raise ValueError('Zgjidh një skedar CSV ose FASTA (.fa, .fasta, .faa).')
