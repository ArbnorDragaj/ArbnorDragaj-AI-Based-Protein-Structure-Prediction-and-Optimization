"""Modeli i thjeshtë HP dhe dy algoritme kërkimi në rrjetë 3D."""
import math
import random
import time
from dataclasses import dataclass, field

AMINOACIDET = 'ACDEFGHIKLMNPQRSTVWY'
HIDROFOBIKE = set('AVILMFWYC')
DREJTIMET = ((1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1))

def sekuenca_e_sakte(text):
    text = text.strip()
    if not text or any(c not in AMINOACIDET + AMINOACIDET.lower() for c in text):
        raise ValueError('Shkruaj një sekuencë me aminoacide të vlefshme: ' + AMINOACIDET)
    return text.upper()

def zinxhiri(n):
    return [(i, 0, 0) for i in range(n)]

def valide(pikat, n):
    if type(n) is not int or n <= 0 or len(pikat) != n:
        return False
    zena = set()
    for i, pika in enumerate(pikat):
        if (not isinstance(pika, tuple) or len(pika) != 3 or
                any(type(vlera) is not int for vlera in pika)):
            return False
        if pika in zena:
            return False
        if i and sum(abs(pika[k]-pikat[i-1][k]) for k in range(3)) != 1:
            return False
        zena.add(pika)
    return True

def kontaktet(sekuenca, pikat):
    """Numëron kontaktet H-H jo radhazi, secilin një herë."""
    zena = {p: i for i, p in enumerate(pikat)}
    kontakte = 0
    for i, (x, y, z) in enumerate(pikat):
        if sekuenca[i] not in HIDROFOBIKE:
            continue
        for dx, dy, dz in DREJTIMET:
            j = zena.get((x+dx, y+dy, z+dz), -1)
            if j > i + 1 and sekuenca[j] in HIDROFOBIKE:
                kontakte += 1
    return kontakte

def energjia(sekuenca, pikat, pesha=1.0):
    if not valide(pikat, len(sekuenca)):
        raise ValueError('Struktura është e pavlefshme ose gjatësia nuk përputhet.')
    return -pesha * kontaktet(sekuenca, pikat)

def kontrollo_parametrat(sekuenca, pesha, kufiri, sekonda):
    """Kontroll i përbashkët edhe kur algoritmet thirren pa ndërfaqe."""
    sekuenca = sekuenca_e_sakte(sekuenca)
    if type(kufiri) is not int or kufiri <= 0:
        raise ValueError('Tentativat duhet të jenë numër i plotë pozitiv.')
    for emri, vlera in (('Pesha', pesha), ('Koha', sekonda)):
        if isinstance(vlera, bool) or not isinstance(vlera, (int, float)):
            raise ValueError(f'{emri} duhet të jetë numër pozitiv.')
        if not math.isfinite(vlera) or vlera <= 0:
            raise ValueError(f'{emri} duhet të jetë pozitive dhe e fundme.')
    return sekuenca

def rrotullo(pikat, pivot, boshti, shenja):
    qendra = pikat[pivot]
    rezultat = pikat[:pivot+1]
    for pika in pikat[pivot+1:]:
        x, y, z = (pika[k]-qendra[k] for k in range(3))
        if boshti == 0:
            e_re = (x, -shenja*z, shenja*y)
        elif boshti == 1:
            e_re = (shenja*z, y, -shenja*x)
        else:
            e_re = (-shenja*y, shenja*x, z)
        rezultat.append(tuple(e_re[k] + qendra[k] for k in range(3)))
    return rezultat

@dataclass
class Rezultati:
    algoritmi: str
    sekuenca: str
    pikat: list
    energjia: float
    gjeneruar: int = 0
    valide: int = 0
    invalide: int = 0
    hequr: int = 0
    koha: float = 0
    tentativa_me_e_mire: int = 0
    koha_me_e_mire: float = 0
    arsyeja: str = ''
    rezerve: bool = False
    historia: list = field(default_factory=list)

def simulated_annealing(sekuenca, pesha, kufiri, sekonda, seed=42):
    sekuenca = kontrollo_parametrat(sekuenca, pesha, kufiri, sekonda)
    if type(seed) is not int:
        raise ValueError('Seed duhet të jetë numër i plotë.')
    fillimi = time.perf_counter()
    rng = random.Random(seed)
    aktuale = zinxhiri(len(sekuenca))
    me_e_mira = aktuale.copy()
    e_aktuale = e_mire = energjia(sekuenca, aktuale, pesha)
    r = Rezultati('Simulated Annealing', sekuenca, me_e_mira, e_mire, historia=[(0, e_mire)])
    temperatura = 2.0
    if len(sekuenca) > 2:
        while r.gjeneruar < kufiri and time.perf_counter()-fillimi < sekonda:
            kandidat = rrotullo(aktuale, rng.randrange(1, len(sekuenca)-1), rng.randrange(3), rng.choice((-1,1)))
            r.gjeneruar += 1
            if not valide(kandidat, len(sekuenca)):
                r.invalide += 1
            else:
                r.valide += 1
                e_re = energjia(sekuenca, kandidat, pesha)
                delta = e_re-e_aktuale
                if delta <= 0 or rng.random() < math.exp(-delta / temperatura):
                    aktuale, e_aktuale = kandidat, e_re
                    if e_aktuale < e_mire:
                        me_e_mira, e_mire = aktuale.copy(), e_aktuale
                        r.tentativa_me_e_mire = r.gjeneruar
                        r.koha_me_e_mire = time.perf_counter()-fillimi
                        r.historia.append((r.gjeneruar, e_mire))
            temperatura = max(1e-9, temperatura*0.995)
    r.pikat, r.energjia = me_e_mira, e_mire
    r.koha = time.perf_counter()-fillimi
    r.arsyeja = 'U arrit buxheti.' if r.gjeneruar >= kufiri else ('U arrit koha.' if len(sekuenca)>2 else 'Zinxhir i shkurtër.')
    r.historia.append((r.gjeneruar, e_mire))
    return r

def beam_search(sekuenca, pesha, kufiri, sekonda, gjeresia=30):
    sekuenca = kontrollo_parametrat(sekuenca, pesha, kufiri, sekonda)
    if type(gjeresia) is not int or gjeresia <= 0:
        raise ValueError('Gjerësia Beam duhet të jetë numër i plotë pozitiv.')
    fillimi = time.perf_counter()
    n = len(sekuenca)
    me_e_mira = zinxhiri(n)
    e_mire = energjia(sekuenca, me_e_mira, pesha)
    r = Rezultati('Beam Search', sekuenca, me_e_mira, e_mire, rezerve=n>2, historia=[(0,e_mire)])
    if n > 2:
        beam = [[(0,0,0),(1,0,0)]]
        perfundoi = True
        for thellesia in range(2, n):
            kandidatet = []
            for prefiksi in beam:
                zena = set(prefiksi)
                x,y,z = prefiksi[-1]
                for dx,dy,dz in DREJTIMET:
                    if r.gjeneruar >= kufiri or time.perf_counter()-fillimi >= sekonda:
                        perfundoi = False
                        break
                    r.gjeneruar += 1
                    p = (x+dx,y+dy,z+dz)
                    if p in zena:
                        r.invalide += 1
                        continue
                    r.valide += 1
                    i_ri = prefiksi + [p]
                    e = energjia(sekuenca[:len(i_ri)], i_ri, pesha)
                    kandidatet.append((e, tuple(i_ri)))
                    if len(i_ri) == n and (r.rezerve or e < e_mire):
                        if e <= e_mire:
                            me_e_mira, e_mire = i_ri, e
                            r.tentativa_me_e_mire = r.gjeneruar
                            r.koha_me_e_mire = time.perf_counter()-fillimi
                            r.historia.append((r.gjeneruar, e_mire))
                            r.rezerve = False
                if not perfundoi:
                    break
            if not perfundoi:
                break
            kandidatet.sort()
            r.hequr += max(0, len(kandidatet)-gjeresia)
            beam = [list(p) for _,p in kandidatet[:gjeresia]]
            if not beam:
                break
        r.arsyeja = 'Kërkimi përfundoi.' if perfundoi else 'U arrit koha ose buxheti.'
    else:
        r.arsyeja = 'Zinxhir i shkurtër.'
    r.pikat, r.energjia = me_e_mira, e_mire
    r.koha = time.perf_counter()-fillimi
    r.historia.append((r.gjeneruar, e_mire))
    return r
