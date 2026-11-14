# AI-Based Protein Structure Prediction and Optimization

Projekt universitar në Python: dy algoritme të shkruara në projekt kërkojnë një strukturë proteinike në një rrjetë kubike 3D. Paraqitja është model edukativ HP dhe **nuk është parashikim biologjik i saktë**.

## Nisja në Windows

Hape këtë dosje në VS Code dhe në terminal shkruaj:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Në Linux (me Python 3.11+, Tkinter dhe venv të instaluara):

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

1. Shkruaj sekuencën dhe, nëse dëshiron, ndrysho peshën, kohën, numrin e tentativave dhe gjerësinë Beam. Gjatësia përditësohet automatikisht.
2. Shtyp **Ekzekuto dhe krahaso**. Të dy algoritmet ekzekutohen njëri pas tjetrit; rezultatet shfaqen poshtë figurës.
3. Te **Shfaq strukturën** zgjidh algoritmin. Tërhiq figurën me butonin e majtë të mausit për rrotullim dhe përdor rrotën për zmadhim. **Rivendos pamjen** kthen këndin fillestar.

Portokalli është H, blu është P. Numrat janë renditja e aminoacideve, kur zinxhiri ka deri në 25 elemente. Katrori shënon fillimin dhe rombi fundin.

## Testet dhe eksperimentet

```powershell
.\.venv\Scripts\python.exe -m unittest -v
.\.venv\Scripts\python.exe eksperimente.py
```

Eksperimentet shkruajnë `rezultate/rezultatet.csv` dhe pesë grafikë PNG në `rezultate/`. Riekzekutimi i eksperimenteve zëvendëson këto skedarë të gjeneruar. Tabela përmban përbërjen, sekuencën, seed-in SA, energjinë, kohën, numëruesit, memorien dhe përdorimin e rezervës.

## Skedarët

- `proteina.py`: modeli, energjia, rrotullimi, Simulated Annealing dhe Beam Search.
- `main.py`: ndërfaqja e thjeshtë dhe pamja interaktive 3D.
- `matja.py`: matja e veçantë e memories me `tracemalloc`.
- `eksperimente.py`: krahasimi në gjatësi e përbërje të ndryshme dhe grafikët.
- `test_proteina.py`: testet e modelit dhe algoritmeve.
- `RAPORTI.md`: shpjegimi, kompleksiteti dhe interpretimi i rezultateve.

Matplotlib është varësia e vetme e drejtpërdrejtë. Ai instalon edhe varësitë e veta, si NumPy; algoritmet përdorin vetëm bibliotekën standarde. Nuk përdoren biblioteka protein-folding, modele të trajnuara apo API.
