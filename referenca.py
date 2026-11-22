"""Referencë ekzakte për raste të vogla; llogaritja e energjisë është e pavarur."""
import csv
from pathlib import Path

from proteina import beam_search, simulated_annealing, sekuenca_e_sakte


def strukturat_ekzakte(n):
    if type(n) is not int or not 1 <= n <= 8:
        raise ValueError('Referenca ekzakte mbështet gjatësi 1–8, për kosto praktike.')
    pikat = [(0, 0, 0)] if n == 1 else [(0, 0, 0), (1, 0, 0)]
    zena = set(pikat)

    def vizito():
        if len(pikat) == n:
            yield tuple(pikat)
            return
        x, y, z = pikat[-1]
        for d in ((1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)):
            p = (x+d[0], y+d[1], z+d[2])
            if p not in zena:
                pikat.append(p)
                zena.add(p)
                yield from vizito()
                zena.remove(p)
                pikat.pop()
    yield from vizito()


def energjia_e_pavarur(s, pikat):
    # Kontrollo çiftet drejtpërdrejt, pa dict dhe pa funksionin kontaktet.
    h = 'AVILMFWYC'
    return -sum(s[i] in h and s[j] in h and
                sum(abs(a-b) for a,b in zip(pikat[i], pikat[j])) == 1
                for i in range(len(s)) for j in range(i+2, len(s)))


def analizo_ekzakt(s, prefikset=()):
    s = sekuenca_e_sakte(s)
    te_hequra = {tuple(p) for p in prefikset if len(p) < len(s)}
    total = hequr = 0
    minimumi = 0
    for pikat in strukturat_ekzakte(len(s)):
        total += 1
        minimumi = min(minimumi, energjia_e_pavarur(s, pikat))
        hequr += any(pikat[:k] in te_hequra for k in range(2, len(s)))
    return {'struktura_valide': total, 'optimumi': minimumi,
            'hequr_globale': hequr, 'pruning_global_perqind': 100*hequr/total}


def krijo_referencat(folder):
    rows = []
    for familja, model in (('hidrofobike','AVILMFWYC'),
                          ('përzier','ACDEFGHIKLMNPQRSTVWY'), ('polare','DEGHKNPQRST')):
        for n in (4, 6, 8):
            s = (model*2)[:n]
            bs = beam_search(s, 1, 30000, 30, 20, gjurmo_pruning=True)
            ref = analizo_ekzakt(s, bs.prefikse_te_hequra)
            if bs.arsyeja != 'Kërkimi përfundoi.':
                raise RuntimeError('Referenca Beam nuk përfundoi; rrit buxhetin.')
            if ref['struktura_valide'] != ref['hequr_globale'] + bs.plota_te_gjeneruara:
                raise AssertionError('Ndarja ekzakte e hapësirës nuk përputhet.')
            for r in (simulated_annealing(s, 1, 3000, 30, 1), bs):
                if r.energjia != energjia_e_pavarur(s, r.pikat) or r.energjia < ref['optimumi']:
                    raise AssertionError('Energjia nuk përputhet me referencën e pavarur.')
                rows.append({'familja': familja, 'gjatesia': n, 'algoritmi': r.algoritmi,
                             'energjia': r.energjia, 'optimumi': ref['optimumi'],
                             'hendeku': r.energjia-ref['optimumi'],
                             'struktura_valide': ref['struktura_valide'],
                             'hequr_globale': ref['hequr_globale'] if r is bs else '',
                             'pruning_global_perqind': ref['pruning_global_perqind'] if r is bs else ''})
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    with (folder/'referenca_ekzakte.csv').open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


if __name__ == '__main__':
    print('Referenca të ruajtura:', len(krijo_referencat(Path(__file__).resolve().parent/'rezultate')))
