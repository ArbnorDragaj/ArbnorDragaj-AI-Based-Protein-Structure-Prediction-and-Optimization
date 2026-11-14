"""Eksperimente reale me gjatësi dhe përbërje të ndryshme."""
import csv
from pathlib import Path
from statistics import mean
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from proteina import simulated_annealing, beam_search, valide, energjia
from matja import mat_memorien

def main():
    folder = Path(__file__).resolve().parent / 'rezultate'
    folder.mkdir(exist_ok=True)
    gjatesite = (6, 10, 14, 18)
    familjet = {'hidrofobike':'AVILMFWYC', 'përzier':'ACDEFGHIKLMNPQRSTVWY', 'polare':'DEGHKNPQRST'}
    rreshta = []
    historite = {}
    for familja, model in familjet.items():
        for n in gjatesite:
            s = (model * (n//len(model)+1))[:n]
            print(f'{familja}, n={n}', flush=True)
            mem = {key: mat_memorien(key,s,1.0,3000,2.0,20) for key in ('SA','Beam')}
            punet = [('SA', seed, simulated_annealing(s,1.0,3000,2.0,seed)) for seed in (1,2,3)]
            punet.append(('Beam', None, beam_search(s,1.0,3000,2.0,20)))
            for k, seed, r in punet:
                assert valide(r.pikat,n) and energjia(s,r.pikat,1.0) == r.energjia
                assert r.gjeneruar == r.valide + r.invalide
                rreshta.append({'familja':familja,'gjatesia':n,'sekuenca':s,'algoritmi':k,
                    'seed': seed, 'energjia':r.energjia,'koha_s':r.koha,'kandidate':r.gjeneruar,'valide':r.valide,
                    'invalide':r.invalide,'hequr_beam':r.hequr,
                    'pruning_perqind':100*r.hequr/r.valide if r.valide else 0,
                    'memoria_kib':mem[k]['bajte']/1024,'memoria_kandidate':mem[k]['kandidate'],
                    'tentativa_me_e_mire':r.tentativa_me_e_mire,'rezerve':r.rezerve})
                if familja == 'përzier' and n == 18 and k not in historite:
                    historite[k] = r.historia
    with (folder/'rezultatet.csv').open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rreshta[0])); w.writeheader(); w.writerows(rreshta)
    for fusha, titulli in [('energjia','Energjia'),('koha_s','Koha (s)'),('memoria_kib','Memoria Python (KiB)'),('kandidate','Kandidatët')]:
        fig, axes = plt.subplots(1,3,figsize=(12,4),sharex=True)
        for ax, familja in zip(axes,familjet):
            for algoritmi in ('SA','Beam'):
                vlerat = [mean(r[fusha] for r in rreshta if r['familja']==familja and r['gjatesia']==n and r['algoritmi']==algoritmi) for n in gjatesite]
                ax.plot(gjatesite,vlerat,marker='o',label=algoritmi)
            ax.set_title(familja); ax.set_xlabel('Gjatësia'); ax.grid(alpha=.25)
        axes[0].set_ylabel(titulli); axes[-1].legend(); fig.tight_layout()
        fig.savefig(folder/(fusha+'.png'),dpi=130); plt.close(fig)
    fig, ax = plt.subplots()
    for emri, histori in historite.items():
        ax.step([p[0] for p in histori],[p[1] for p in histori],where='post',label=emri)
    ax.set(xlabel='Kandidatët',ylabel='Energjia më e mirë',title='Konvergjenca, n=18, përzier')
    ax.legend(); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(folder/'konvergjenca.png',dpi=130); plt.close(fig)
    print(f'U ruajtën {len(rreshta)} rezultate te {folder}')

if __name__ == '__main__':
    main()
