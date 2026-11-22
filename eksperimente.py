"""Matje të përsëritura, struktura të verifikuara dhe referencë ekzakte."""
import csv
import argparse
import os
import tempfile
import time
import json
import platform
from pathlib import Path
from statistics import mean, stdev
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from proteina import simulated_annealing, beam_search, valide, energjia
from matja import mat_memorien
from referenca import krijo_referencat

GJATESITE = (6, 10, 18, 30, 60, 100)
FAMILJET = {'hidrofobike':'AVILMFWYC', 'përzier':'ACDEFGHIKLMNPQRSTVWY', 'polare':'DEGHKNPQRST'}
SEEDS = (1, 2, 3, 4, 5)
BUXHETI, SEKONDA, GJERESIA = 3000, 1.0, 20


def ruaj_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def verifiko(s, r):
    if not valide(r.pikat,len(s)) or energjia(s,r.pikat) != r.energjia:
        raise AssertionError('Struktura ose energjia është e gabuar.')
    if r.gjeneruar != r.valide+r.invalide or not 0 <= r.hequr <= r.valide:
        raise AssertionError('Numëruesit nuk përputhen.')
    if r.historia[-1] != (r.gjeneruar,r.energjia):
        raise AssertionError('Historia nuk përfundon me rezultatin final.')
    if any(a[0]>b[0] or a[1]<b[1] for a,b in zip(r.historia,r.historia[1:])):
        raise AssertionError('Historia nuk është monotone.')


def ruaj_figuren(fig, path):
    # OneDrive ose një lexues mund ta bllokojë përkohësisht destinacionin.
    with tempfile.NamedTemporaryFile(dir=path.parent, suffix='.png', delete=False) as f:
        temporary = Path(f.name)
    try:
        fig.savefig(temporary, dpi=130)
        for attempt in range(3):
            try:
                os.replace(temporary, path)
                break
            except OSError:
                if attempt == 2:
                    raise
                time.sleep(0.2)
    finally:
        temporary.unlink(missing_ok=True)
        plt.close(fig)


def grafiket(folder, rows, histories, references, widths):
    metrics = [('energjia','Energjia'),('koha_s','Koha (s)'),
               ('memoria_kib','Peak Python (KiB)'),('kandidate','Kandidatët'),
               ('pruning_lokal_perqind','Hequr / validë të gjeneruar (%)')]
    for metric, title in metrics:
        fig, axes = plt.subplots(1,3,figsize=(13,4),sharex=True)
        for ax, family in zip(axes,FAMILJET):
            for algo in ('SA','Beam'):
                if metric == 'pruning_lokal_perqind' and algo == 'SA':
                    continue
                groups = [[r[metric] for r in rows if r['familja']==family and
                           r['gjatesia']==n and r['algoritmi']==algo] for n in GJATESITE]
                ax.errorbar(GJATESITE,[mean(g) for g in groups],
                            yerr=[stdev(g) for g in groups],marker='o',capsize=3,label=algo)
            ax.set_title(family); ax.set_xlabel('Gjatësia'); ax.grid(alpha=.25)
        axes[0].set_ylabel(title); axes[-1].legend(); fig.tight_layout()
        ruaj_figuren(fig, folder/(metric+'.png'))

    fig, axes = plt.subplots(3,len(GJATESITE),figsize=(18,9),squeeze=False)
    checkpoints = list(range(0,BUXHETI+1,100))
    for i, family in enumerate(FAMILJET):
        for j,n in enumerate(GJATESITE):
            ax=axes[i,j]
            for algo in ('SA','Beam'):
                runs=[h['historia'] for h in histories if h['familja']==family and
                      h['gjatesia']==n and h['algoritmi']==algo]
                values=[[next(e for k,e in reversed(h) if k<=c) for c in checkpoints] for h in runs]
                # Pas ndalimit mbahet zgjidhja finale, jo vazhdim i sajuar i kërkimit.
                ax.step(checkpoints,[mean(v[k] for v in values) for k in range(len(checkpoints))],
                        where='post',label=algo)
            ax.set_title(f'{family}, n={n}',fontsize=9); ax.grid(alpha=.25)
            if i==2: ax.set_xlabel('Kandidatët')
            if j==0: ax.set_ylabel('E më e mirë, mesatare')
    axes[0,-1].legend(); fig.tight_layout()
    ruaj_figuren(fig, folder/'konvergjenca.png')

    fig,axes=plt.subplots(1,3,figsize=(13,4))
    for ax,family in zip(axes,FAMILJET):
        for algo in ('Simulated Annealing','Beam Search'):
            points=[r for r in references if r['familja']==family and r['algoritmi']==algo]
            ax.plot([r['gjatesia'] for r in points],[r['hendeku'] for r in points],marker='o',label=algo)
        ax.set_title(family); ax.set_xlabel('Gjatësia'); ax.grid(alpha=.25)
    axes[0].set_ylabel('E − optimumi ekzakt (0 = optimal)'); axes[-1].legend()
    fig.tight_layout(); ruaj_figuren(fig, folder/'referenca_ekzakte.png')

    fig,ax=plt.subplots()
    for family in FAMILJET:
        points=[r for r in references if r['familja']==family and r['algoritmi']=='Beam Search']
        ax.plot([r['gjatesia'] for r in points],[r['pruning_global_perqind'] for r in points],marker='o',label=family)
    ax.set(xlabel='Gjatësia',ylabel='Struktura të hequra nga zgjerimi (%)',title='Pruning global ekzakt; lidhja e parë në +x')
    ax.legend(); ax.grid(alpha=.25); fig.tight_layout()
    ruaj_figuren(fig, folder/'pruning_global.png')

    fig,axes=plt.subplots(1,2,figsize=(10,4))
    for n in (30,60):
        for ax,metric in zip(axes,('energjia','koha_s')):
            ax.plot((5,20,60),[mean(r[metric] for r in widths if r['gjatesia']==n and r['beam_width']==b)
                               for b in (5,20,60)],marker='o',label=f'n={n}')
            ax.set_xlabel('Beam width'); ax.grid(alpha=.25); ax.legend()
    axes[0].set_ylabel('Energjia'); axes[1].set_ylabel('Koha (s)')
    fig.tight_layout(); ruaj_figuren(fig, folder/'beam_width.png')


def main():
    folder=Path(__file__).resolve().parent/'rezultate'
    folder.mkdir(exist_ok=True)
    rows, histories = [], []
    for family, model in FAMILJET.items():
        for n in GJATESITE:
            s=(model*(n//len(model)+1))[:n]
            print(f'{family}, n={n}',flush=True)
            for repeat,seed in enumerate(SEEDS,1):
                for algo in (('SA','Beam') if repeat%2 else ('Beam','SA')):
                    r=(simulated_annealing(s,1,BUXHETI,SEKONDA,seed) if algo=='SA'
                       else beam_search(s,1,BUXHETI,SEKONDA,GJERESIA))
                    verifiko(s,r)
                    memory=mat_memorien(algo,s,1,BUXHETI,SEKONDA,GJERESIA,seed)
                    rows.append({'familja':family,'gjatesia':n,'sekuenca':s,'algoritmi':algo,
                        'perseritja':repeat,'seed':seed if algo=='SA' else '',
                        'energjia':r.energjia,'koha_s':r.koha,'kandidate':r.gjeneruar,
                        'plotesime_te_vleresuara':r.plotesime_te_vleresuara,
                        'kandidate_dhe_plotesime':r.gjeneruar+r.plotesime_te_vleresuara,
                        'valide':r.valide,'invalide':r.invalide,'hequr_beam':r.hequr,
                        'pruning_lokal_perqind':100*r.hequr/r.valide if r.valide else 0,
                        'memoria_kib':memory['bajte']/1024,'memoria_kandidate':memory['kandidate'],
                        'memoria_energjia':memory['energjia'],
                        'tentativa_me_e_mire':r.tentativa_me_e_mire,'koha_me_e_mire_s':r.koha_me_e_mire,
                        'rezerve':r.rezerve,'arsyeja':r.arsyeja})
                    histories.append({'familja':family,'gjatesia':n,'algoritmi':algo,'perseritja':repeat,
                                      'historia':r.historia,'koordinatat':r.pikat})
    ruaj_csv(folder/'rezultatet.csv',rows)
    (folder/'historite.json').write_text(json.dumps(histories,ensure_ascii=False),encoding='utf-8')
    summary=[]
    for family in FAMILJET:
        for n in GJATESITE:
            for algo in ('SA','Beam'):
                group=[r for r in rows if r['familja']==family and r['gjatesia']==n and r['algoritmi']==algo]
                row={'familja':family,'gjatesia':n,'algoritmi':algo,'perseritje':len(group),
                     'energjia_me_e_mire':min(r['energjia'] for r in group),
                     'rezerva':sum(r['rezerve'] for r in group)}
                for metric in ('energjia','koha_s','memoria_kib','kandidate','koha_me_e_mire_s'):
                    row[metric+'_mesatare']=mean(r[metric] for r in group)
                    row[metric+'_std']=stdev(r[metric] for r in group)
                summary.append(row)
    ruaj_csv(folder/'permbledhja.csv',summary)
    references=krijo_referencat(folder)
    widths=[]
    for n in (30,60):
        s=('ACDEFGHIKLMNPQRSTVWY'*3)[:n]
        for width in (5,20,60):
            for repeat in range(1,4):
                r=beam_search(s,1,BUXHETI,SEKONDA,width)
                verifiko(s,r)
                widths.append({'gjatesia':n,'beam_width':width,'perseritja':repeat,
                               'energjia':r.energjia,'koha_s':r.koha,'kandidate':r.gjeneruar,'rezerve':r.rezerve})
    ruaj_csv(folder/'beam_width.csv',widths)
    grafiket(folder,rows,histories,references,widths)
    metadata={'python':platform.python_version(),'platforma':platform.platform(),
              'gjatesite':GJATESITE,'seeds':SEEDS,'kandidate':BUXHETI,'sekonda':SEKONDA,
              'beam_width':GJERESIA,'matja_memories':'tracemalloc, proces i veçantë, i njëjti seed',
              'konvergjenca':'pas ndalimit mbahet energjia finale; boshti është kandidatët, jo koha'}
    (folder/'konfigurimi.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'U ruajtën {len(rows)} matje, {len(references)} referenca dhe {len(widths)} prova Beam width.',flush=True)


def rigjenero_grafiket(folder):
    def lexo(name, numeric):
        with (folder/name).open(encoding='utf-8-sig') as f:
            rows=list(csv.DictReader(f))
        for r in rows:
            for key in numeric:
                if r[key] != '':
                    r[key]=float(r[key])
        return rows
    rows=lexo('rezultatet.csv',('gjatesia','energjia','koha_s','memoria_kib','kandidate','pruning_lokal_perqind'))
    references=lexo('referenca_ekzakte.csv',('gjatesia','hendeku','pruning_global_perqind'))
    widths=lexo('beam_width.csv',('gjatesia','beam_width','energjia','koha_s'))
    histories=json.loads((folder/'historite.json').read_text(encoding='utf-8'))
    grafiket(folder,rows,histories,references,widths)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vetem-grafiket', action='store_true', help='Vizato përsëri nga matjet e ruajtura.')
    args=parser.parse_args()
    if args.vetem_grafiket:
        rigjenero_grafiket(Path(__file__).resolve().parent/'rezultate')
        print('Grafikët u rigjeneruan pa përsëritur matjet.')
    else:
        main()
