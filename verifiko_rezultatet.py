"""Verifikim i artefakteve reale, përfshirë koordinatat dhe energjinë e pavarur."""
import csv
import json
import math
from pathlib import Path
from statistics import mean, stdev
from proteina import valide
from referenca import energjia_e_pavarur, analizo_ekzakt


def kontrollo(folder):
    folder = Path(folder)
    def lexo(name):
        return list(csv.DictReader((folder/name).open(encoding='utf-8-sig')))
    rows = lexo('rezultatet.csv')
    histories = json.loads((folder/'historite.json').read_text(encoding='utf-8'))
    summary = lexo('permbledhja.csv')
    references = lexo('referenca_ekzakte.csv')
    config = json.loads((folder/'konfigurimi.json').read_text(encoding='utf-8'))
    if len(rows) != 180 or len(histories) != 180 or len(summary) != 36 or len(references) != 18:
        raise AssertionError('Seria nuk është e plotë.')
    keys = lambda r: (r['familja'],int(r['gjatesia']),r['algoritmi'],int(r['perseritja']))
    hist = {keys(h):h for h in histories}
    if len(hist) != len(rows):
        raise AssertionError('Histori të përsëritura ose të paplota.')
    for r in rows:
        h=hist[keys(r)]
        p=[tuple(x) for x in h['koordinatat']]
        n=int(r['gjatesia']); e=float(r['energjia'])
        assert valide(p,n) and e==energjia_e_pavarur(r['sekuenca'],p)
        assert int(r['kandidate'])==int(r['valide'])+int(r['invalide'])
        assert 0<=int(r['hequr_beam'])<=int(r['valide'])
        assert int(r['kandidate'])<=config['kandidate']
        assert int(r['kandidate_dhe_plotesime'])==int(r['kandidate'])+int(r['plotesime_te_vleresuara'])
        assert 0<=float(r['koha_me_e_mire_s'])<=float(r['koha_s'])
        assert h['historia'][-1]==[int(r['kandidate']),e]
        assert all(a[0]<=b[0] and a[1]>=b[1] for a,b in zip(h['historia'],h['historia'][1:]))
        assert all(math.isfinite(float(r[k])) for k in ('energjia','koha_s','memoria_kib','memoria_energjia'))
    for s in summary:
        group=[r for r in rows if (r['familja'],r['gjatesia'],r['algoritmi'])==
               (s['familja'],s['gjatesia'],s['algoritmi'])]
        assert len(group)==5
        if s['algoritmi']=='SA':
            assert {int(r['seed']) for r in group}==set(config['seeds'])
        for metric in ('energjia','koha_s','memoria_kib','kandidate','koha_me_e_mire_s'):
            values=[float(r[metric]) for r in group]
            assert math.isclose(float(s[metric+'_mesatare']),mean(values),abs_tol=1e-12)
            assert math.isclose(float(s[metric+'_std']),stdev(values),abs_tol=1e-12)
    models={'hidrofobike':'AVILMFWYC','përzier':'ACDEFGHIKLMNPQRSTVWY','polare':'DEGHKNPQRST'}
    for r in references:
        ref=analizo_ekzakt((models[r['familja']]*2)[:int(r['gjatesia'])])
        assert int(r['optimumi'])==ref['optimumi']
        assert int(r['struktura_valide'])==ref['struktura_valide']
        assert float(r['hendeku'])==float(r['energjia'])-ref['optimumi']>=0
    assert len(lexo('beam_width.csv'))==18
    for name in ('energjia','koha_s','memoria_kib','kandidate','konvergjenca',
                 'pruning_lokal_perqind','referenca_ekzakte','pruning_global','beam_width'):
        assert (folder/(name+'.png')).stat().st_size>0
    print('Kaluan: 180 struktura/energji me oracle të pavarur, 36 përmbledhje statistikore, '
          '18 referenca ekzakte, 18 prova Beam width dhe 9 grafikë.')


if __name__=='__main__':
    kontrollo(Path(__file__).resolve().parent/'rezultate')
