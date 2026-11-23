"""Lexim i sekuencave lokale; nuk hiqen aminoacide të panjohura në heshtje."""
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
