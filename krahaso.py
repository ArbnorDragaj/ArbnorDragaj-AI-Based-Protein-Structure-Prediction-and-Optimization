"""Krahaso dy algoritmet nga terminali, pa Tkinter ose Matplotlib."""
import argparse
from pathlib import Path
from proteina import simulated_annealing, beam_search, kontrollo_parametrat
from matja import mat_memorien
from eksportimi import eksporto_json, eksporto_koordinatat


def krahaso(s, folder, pesha=1, buxheti=3000, sekonda=1, beam=20, seed=42, memoria=True):
    s=kontrollo_parametrat(s,pesha,buxheti,sekonda)
    if type(beam) is not int or beam<=0 or type(seed) is not int:
        raise ValueError('Gjerësia Beam duhet pozitive dhe seed duhet numër i plotë.')
    folder=Path(folder)
    folder.mkdir(parents=True,exist_ok=False)
    results=[simulated_annealing(s,pesha,buxheti,sekonda,seed),
             beam_search(s,pesha,buxheti,sekonda,beam)]
    memories=[mat_memorien(k,s,pesha,buxheti,sekonda,beam,seed) for k in ('SA','Beam')] if memoria else [None,None]
    config={'pesha':pesha,'buxheti':buxheti,'koha_s':sekonda,'beam_width':beam,
            'seed_sa':seed,'matje_memorieje':memoria,'burimi':'sekuencë e dhënë nga përdoruesi'}
    eksporto_json(folder/'rezultatet.json',results,config,memories)
    eksporto_koordinatat(folder/'koordinatat.csv',results)
    return results


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sekuenca')
    parser.add_argument('--dalja',required=True,type=Path,help='Dosje e re për JSON dhe CSV.')
    parser.add_argument('--pesha',type=float,default=1)
    parser.add_argument('--buxheti',type=int,default=3000)
    parser.add_argument('--sekonda',type=float,default=1)
    parser.add_argument('--beam',type=int,default=20)
    parser.add_argument('--seed',type=int,default=42)
    parser.add_argument('--pa-memorie',action='store_true')
    args=parser.parse_args()
    try:
        results=krahaso(args.sekuenca,args.dalja,args.pesha,args.buxheti,args.sekonda,
                        args.beam,args.seed,not args.pa_memorie)
    except (OSError,ValueError,RuntimeError) as error:
        parser.error(str(error))
    for r in results:
        print(f'{r.algoritmi}: E={r.energjia:g}; kandidatë={r.gjeneruar}; koha={r.koha:.4f}s; {r.arsyeja}')
