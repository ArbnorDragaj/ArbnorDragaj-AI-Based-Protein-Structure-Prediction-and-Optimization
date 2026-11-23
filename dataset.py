"""Eksperimente me sekuenca CSV/FASTA lokale, me burim të deklaruar."""
import argparse
import csv
import hashlib
import io
import json
from itertools import islice
from pathlib import Path
from te_dhenat import lexo_sekuencat
from proteina import simulated_annealing, beam_search, kontrollo_parametrat
from matja import mat_memorien
from eksportimi import eksporto_json, shkruaj_atomik


def sha256(path):
    digest=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            digest.update(chunk)
    return digest.hexdigest()


def ekzekuto_dataset(path, output, burimi, numri=10, kolona=None,
                     pesha=1, buxheti=3000, sekonda=1, beam=20, seeds=(1,2,3)):
    if not burimi.strip() or type(numri) is not int or numri<=0:
        raise ValueError('Cakto burimin dhe një numër pozitiv sekuencash.')
    if not seeds or len(set(seeds))!=len(seeds) or any(type(s) is not int for s in seeds):
        raise ValueError('Seed-et duhet numra të plotë të ndryshëm.')
    if type(beam) is not int or beam<=0:
        raise ValueError('Beam width duhet pozitiv.')
    kontrollo_parametrat('A',pesha,buxheti,sekonda)
    fingerprint=sha256(path)
    records=list(islice(lexo_sekuencat(path,kolona),numri))
    if sha256(path)!=fingerprint:
        raise ValueError('Skedari ndryshoi gjatë leximit; provo përsëri.')
    folder=Path(output)
    folder.mkdir(parents=True,exist_ok=False)
    metadata={'burimi':burimi,'skedari':str(Path(path).resolve()),'sha256':fingerprint,
              'numri_kerkuar':numri,'numri_lexuar':len(records),'seeds_sa':list(seeds),
              'pesha':pesha,'buxheti':buxheti,'sekonda':sekonda,'beam_width':beam,
              'statusi':'duke punuar','matje_te_perfunduara':0,
              'shenim':'Përdoren sekuencat; nuk matet saktësia kundrejt strukturave biologjike.'}
    def ruaj_metadata():
        shkruaj_atomik(folder/'burimi.json',json.dumps(metadata,ensure_ascii=False,indent=2,allow_nan=False))
    rows=[]
    ruaj_metadata()
    try:
        for index,record in enumerate(records,1):
            s=record['sekuenca']
            results=[]
            memories=[]
            for algo,seed in [('SA',seed) for seed in seeds]+[('Beam',None)]:
                r=(simulated_annealing(s,pesha,buxheti,sekonda,seed) if algo=='SA'
                   else beam_search(s,pesha,buxheti,sekonda,beam))
                m=mat_memorien(algo,s,pesha,buxheti,sekonda,beam,seed if seed is not None else 42)
                results.append(r);memories.append(m)
                rows.append({'id':record['id'],'gjatesia':len(s),'algoritmi':algo,'seed':seed,
                             'energjia':r.energjia,'koha_s':r.koha,'kandidate':r.gjeneruar,
                             'plotesime':r.plotesime_te_vleresuara,'valide':r.valide,'invalide':r.invalide,
                             'memoria_kib':m['bajte']/1024,'memoria_kandidate':m['kandidate'],
                             'memoria_energjia':m['energjia'],'rezerve':r.rezerve,'arsyeja':r.arsyeja})
            config={**metadata,'id':record['id']}
            eksporto_json(folder/f'{index:04d}.json',results,config,memories)
            buffer=io.StringIO(newline='')
            writer=csv.DictWriter(buffer,fieldnames=list(rows[0]))
            writer.writeheader();writer.writerows(rows)
            shkruaj_atomik(folder/'rezultatet.csv',buffer.getvalue())
            metadata['matje_te_perfunduara']=len(rows)
            ruaj_metadata()
            print(f'{index}/{len(records)}: {record["id"]}, n={len(s)}',flush=True)
    except BaseException as error:
        metadata['statusi']='ndërprerë'
        metadata['gabimi']=str(error)
        ruaj_metadata()
        raise
    metadata['statusi']='përfunduar'
    ruaj_metadata()
    return rows


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('skedari',type=Path)
    parser.add_argument('--dalja',required=True,type=Path,help='Dosje e re; nuk mbishkruan rezultate ekzistuese.')
    parser.add_argument('--burimi',required=True,help='URL/emri i dataset-it dhe prejardhja.')
    parser.add_argument('--numri',type=int,default=10,help='Përdor deri në N sekuencat e para, pa shkurtuar gjatësinë.')
    parser.add_argument('--kolona',help='Emri i kolonës së sekuencës në CSV.')
    parser.add_argument('--pesha',type=float,default=1)
    parser.add_argument('--buxheti',type=int,default=3000)
    parser.add_argument('--sekonda',type=float,default=1)
    parser.add_argument('--beam',type=int,default=20)
    parser.add_argument('--seeds',type=int,nargs='+',default=[1,2,3])
    args=parser.parse_args()
    try:
        rows=ekzekuto_dataset(args.skedari,args.dalja,args.burimi,args.numri,args.kolona,
                             args.pesha,args.buxheti,args.sekonda,args.beam,args.seeds)
    except (OSError,ValueError) as error:
        parser.error(str(error))
    print(f'U ruajtën {len(rows)} matje; rezultati është për modelin HP.')
