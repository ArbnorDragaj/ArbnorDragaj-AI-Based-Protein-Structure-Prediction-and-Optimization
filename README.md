# AI-Based Protein Structure Prediction and Optimization

Projekt universitar për lëndën **Dizajnimi i Algoritmeve**. Programi merr një sekuencë aminoacidesh, kërkon struktura të vlefshme në hapësirë 3D dhe krahason dy algoritme: **Simulated Annealing** dhe **Beam Search**.

Struktura shfaqet në një dritare interaktive ku mund të rrotullohet me maus. Projekti përfshin edhe eksperimente, grafikë dhe teste.

> **Kufizim:** ky është model edukativ i thjeshtuar HP në rrjetë kubike. Ai ilustron kërkimin dhe optimizimin; nuk është parashikim biologjik i saktë i strukturës reale të një proteine.

## Përmbajtja

- [Qëllimi dhe funksionet](#qëllimi-dhe-funksionet)
- [Instalimi dhe nisja](#instalimi-dhe-nisja)
- [Përdorimi i aplikacionit](#përdorimi-i-aplikacionit)
- [Modeli dhe energjia](#modeli-dhe-energjia)
- [Algoritmet](#algoritmet)
- [Matjet dhe rezultatet](#matjet-dhe-rezultatet)
- [Eksperimentet dhe grafikët](#eksperimentet-dhe-grafikët)
- [Testet](#testet)
- [Struktura e projektit](#struktura-e-projektit)
- [Kufizimet](#kufizimet)

## Qëllimi dhe funksionet

Numri i mënyrave në të cilat një proteinë mund të paloset rritet shumë shpejt me gjatësinë e sekuencës. Projekti demonstron si mund të kërkohet një strukturë me energji të ulët pa u shqyrtuar të gjitha mundësitë.

Aplikacioni:

- pranon sekuenca me 20 aminoacidet standarde;
- kontrollon mbivendosjet dhe lidhjet ndërmjet aminoacideve;
- ekzekuton dy algoritmet njëri pas tjetrit dhe krahason rezultatet;
- shfaq strukturat në 3D dhe raporton energjinë, kandidatët, kohën dhe memorien e gjurmuar;
- gjeneron tabela dhe grafikë nga eksperimente me gjatësi dhe përbërje të ndryshme.

## Instalimi dhe nisja

### Kërkesat

- Python **3.11 ose më i ri**, me Tkinter të instaluar.
- Matplotlib, i specifikuar në `requirements.txt`.
- Një ekran grafik për dritaren 3D.

Matplotlib është varësia e vetme e drejtpërdrejtë; ai instalon edhe varësitë e veta, përfshirë NumPy. Algoritmet, testet dhe eksportimi përdorin bibliotekën standarde të Python-it. Nuk përdoren biblioteka protein-folding, modele të trajnuara ose API të jashtme.

### Windows dhe VS Code

Hape dosjen e projektit në VS Code, zgjidh **Terminal → New Terminal** dhe ekzekuto:

```powershell
py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Tri komandat e para nevojiten gjatë përgatitjes. Herëve të tjera, nga terminali në dosjen e projektit, mjafton:

```powershell
.\.venv\Scripts\python.exe main.py
```

Nëse je duke e marrë projektin për herë të parë me Git:

```powershell
git clone https://github.com/ArbnorDragaj/ArbnorDragaj-AI-Based-Protein-Structure-Prediction-and-Optimization.git
cd ArbnorDragaj-AI-Based-Protein-Structure-Prediction-and-Optimization
```

Pastaj ndiq komandat e përgatitjes më sipër.

### Linux

Me Python 3.11+, Tkinter dhe mbështetjen `venv` të instaluara:

```bash
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

Nëse mungon Tkinter, instalojeni nga paketat e sistemit për shpërndarjen tuaj Linux. Kontrollo instalimin me `python3 -m tkinter`. Ekzekutimi është provuar në Windows; udhëzimet për Linux nuk janë provuar në këtë mjedis.

## Përdorimi i aplikacionit

1. Shkruaj sekuencën, për shembull `ACDEFGHIKLMNPQRSTVWY`. Shkronjat e vogla pranohen dhe kthehen në të mëdha.
2. Gjatësia përditësohet automatikisht. Mund të ndryshosh peshën e kontakteve H–H, kufirin kohor, tentativat dhe gjerësinë Beam; këto vlera duhet të jenë pozitive.
3. Shtyp **Ekzekuto dhe krahaso**. Programi ekzekuton të dy algoritmet njëri pas tjetrit dhe shfaq përmbledhjen poshtë figurës.
4. Te **Shfaq strukturën**, zgjidh Simulated Annealing ose Beam Search për të parë rezultatin përkatës.
5. Tërhiq figurën me butonin e majtë të mausit për ta rrotulluar. Përdor **Zmadho +**, **Zvogëlo −** ose rrotën e mausit mbi figurë për të ndryshuar zmadhimin. **Rivendos pamjen** kthen këndin dhe zmadhimin fillestar.

Zmadhimi ndryshon vetëm kamerën; koordinatat, lidhjet dhe energjia e proteinës mbeten të njëjta. Boshtet X, Y, Z dhe rrjeta koordinative janë të dukshme. Butonat dhe rrota e mausit lejojnë zmadhim nga 0.6 deri në 1.8 herë kundrejt pamjes fillestare.

Butoni **Grafikët e eksperimenteve** hap një dritare ku mund të zgjedhësh energjinë, kohën, memorien Python, kandidatët ose konvergjencën. Grafikët lexohen nga skedarët PNG në `rezultate/`; janë rezultate të eksperimenteve të ruajtura, jo të simulimit aktual. Për t'i përditësuar, ekzekuto `eksperimente.py` dhe hape përsëri dritaren e grafikëve. Nëse mungojnë të gjithë grafikët, aplikacioni shfaq udhëzimin për krijimin e tyre.

Zgjedhësi ndryshon strukturën e shfaqur; nuk e nis algoritmin veçmas. Grafiku paraqet rezultatin përfundimtar, jo çdo lëvizje gjatë kërkimit.

| Fusha | Vlera fillestare | Kuptimi |
|---|---:|---|
| Sekuenca | `AVILMFWYACDE` | Renditja e aminoacideve; gjatësia fillestare është 12 |
| Pesha H–H | 1 | Sa peshon secili kontakt H–H në energji |
| Koha për algoritëm | 2 s | Kufiri praktik kohor për secilin algoritëm |
| Tentativat maksimale | 3000 | Numri maksimal i kandidatëve të gjeneruar |
| Gjerësia Beam | 30 | Numri maksimal i prefikseve të mbajtura në çdo nivel |

Pikat portokalli paraqesin kategorinë **H**, ndërsa pikat blu kategorinë **P**. Katrori shënon fillimin dhe rombi fundin e zinxhirit. Numrat paraqesin renditjen kur sekuenca ka deri në 25 aminoacide.

Për një provë tjetër, përdor sekuencën `ACDEFGHIKLMNPQRSTVWY`, kohën `3`, tentativat `5000` dhe gjerësinë Beam `25`. Në një ekzekutim të mëparshëm u morën energjitë **−6** për SA dhe **−7** për Beam. Koha dhe, kur kufiri kohor ndërpret kërkimin, rezultati mund të ndryshojnë.

## Modeli dhe energjia

Proteina paraqitet si një listë e renditur koordinatash të plota `(x, y, z)` në rrjetë kubike. Çdo aminoacid ka një pozicion, asnjë çift nuk mbivendoset dhe dy aminoacide radhazi kanë distancë Manhattan 1. Koordinatat negative lejohen.

Sekuenca origjinale ruhet dhe përdoret një ndarje e thjeshtuar:

- **H – hidrofobike:** A, V, I, L, M, F, W, Y, C.
- **P – polare:** aminoacidet e tjera të lejuara.

Shkronja **H** në sekuencën origjinale është histidinë dhe në këtë ndarje i përket kategorisë P; ajo nuk duhet ngatërruar me etiketën hidrofobike H.

Energjia e një strukture është:

```text
E = − pesha × numri i kontakteve H–H
```

Një kontakt numërohet kur dy aminoacide H janë fqinjë në rrjetë, por **nuk janë radhazi në sekuencë**. Çdo çift numërohet vetëm një herë. Për shembull, katër aminoacide H të vendosura në një katror kanë një kontakt shtesë dhe energji **−1** kur pesha është 1. Objektivi është të minimizohet energjia.

## Algoritmet

### Simulated Annealing

Nis nga një zinxhir i drejtë dhe krijon kandidatë duke rrotulluar bishtin rreth një pike të zinxhirit. Kandidatët e pavlefshëm refuzohen. Përmirësimet pranohen; një përkeqësim mund të pranohet me probabilitet që varet nga temperatura. Temperatura ulet gradualisht dhe ruhet veçmas struktura më e mirë e gjetur.

Kjo qasje bën **përmirësim lokal** dhe pranimi i disa përkeqësimeve mund ta ndihmojë kërkimin të largohet nga një minimum lokal. Në aplikacion përdoret seed 42; gjatë eksperimenteve përdoren seed-e të ndryshme.

### Beam Search

Ndërton zinxhirin hap pas hapi. Aminoacidi i parë vendoset në origjinë dhe lidhja e parë fiksohet në drejtimin +x për të shmangur disa variante simetrike. Në çdo nivel shqyrtohen deri në gjashtë drejtimet e rrjetës, refuzohen pozitat e zëna dhe ruhen maksimumi **B** prefikset më të mira.

Nëse buxheti mbaron para se të gjendet një strukturë e plotë, programi kthen zinxhirin e drejtë të vlefshëm si **rezervë** dhe e shënon këtë në rezultat. Energjia e prefiksit nuk garanton cilësinë e strukturës përfundimtare.

### Krahasimi

SA propozon struktura të plota dhe përdor rastësi; Beam zgjeron prefikse dhe është determinist për të njëjtat hyrje e buxhet të përfunduar. Kandidatët e tyre nuk përfaqësojnë domosdoshmërisht të njëjtën sasi pune. Asnjëri algoritëm nuk garanton optimumin global. Një energji më e ulët, kohë më e shkurtër ose përdorim më i vogël i memories nuk mjafton i vetëm për të shpallur një fitues të përgjithshëm.

## Matjet dhe rezultatet

Për secilin algoritëm, dritarja shfaq energjinë, kohën, memorien e gjurmuar, numrin e kandidatëve të gjeneruar, validë dhe invalidë, vlefshmërinë, kohën dhe tentativën kur u gjet rezultati më i mirë, arsyen e ndalimit dhe përdorimin e rezervës. Nëse struktura fillestare mbetet më e mira, koha dhe tentativa janë zero.

Për Beam shfaqet edhe numri i kandidatëve validë të hequr nga gjerësia Beam:

```text
Pruning (%) = 100 × kandidatët e hequr nga Beam / kandidatët validë
```

Nëse nuk ka kandidatë validë, shfaqet 0%. Kjo përqindje lidhet me kandidatët **e gjeneruar**, jo me të gjithë hapësirën teorike të strukturave, e cila nuk është numëruar.

Koha kryesore matet me `time.perf_counter()` pa vizatimin dhe pa `tracemalloc`. Memoria matet në një **proces të veçantë**, duke riekzekutuar algoritmin me `tracemalloc`. Ajo është kulmi i alokimeve Python të gjurmuara, jo RSS ose memoria totale e procesit. Meqë matja është ekzekutim tjetër dhe kufiri kohor ende zbatohet, numri i kandidatëve mund të ndryshojë; ai shfaqet veçmas.

## Eksperimentet dhe grafikët

Nga dosja e projektit në Windows:

```powershell
.\.venv\Scripts\python.exe eksperimente.py
```

Në Linux:

```bash
.venv/bin/python eksperimente.py
```

Skripti përdor gjatësi **6, 10, 14 dhe 18** dhe tri familje sekuencash: hidrofobike, të përziera dhe polare. Për çdo rast ekzekuton SA me seed-et 1, 2 dhe 3, si dhe një herë Beam Search: gjithsej **48 ekzekutime**. Parametrat janë pesha 1, maksimumi 3000 kandidatë, kufiri 2 sekonda dhe gjerësia Beam 20. Matja e veçantë e memories për SA përdor seed 42.

Rezultatet e ruajtura janë:

- [Tabela CSV](rezultate/rezultatet.csv) — sekuencat, seed-et dhe matjet individuale.
- [Energjia](rezultate/energjia.png), [koha](rezultate/koha_s.png), [memoria](rezultate/memoria_kib.png) dhe [kandidatët](rezultate/kandidate.png) kundrejt gjatësisë.
- [Konvergjenca](rezultate/konvergjenca.png) — energjia më e mirë kundrejt numrit të kandidatëve për një rast të përzier me gjatësi 18.

**Riekzekutimi i eksperimenteve i zëvendëson skedarët e gjeneruar në `rezultate/`.** Koha e matur ndikohet nga pajisja dhe ngarkesa e saj. Përmbledhja e serisë së ruajtur dhe interpretimi i saj gjenden te [RAPORTI.md](RAPORTI.md).

## Testet

Në Windows:

```powershell
.\.venv\Scripts\python.exe -m unittest -v
```

Në Linux:

```bash
.venv/bin/python -m unittest -v
```

Testet kontrollojnë inputin, vlefshmërinë, përplasjet, lidhjet e prishura, energjinë e katrorit me katër H, rrotullimet, rastet e shkurtra, rezervën, statistikat dhe riprodhueshmërinë e SA me të njëjtin seed.

## Struktura e projektit

```text
├── main.py             # Ndërfaqja dhe pamja interaktive 3D
├── grafiket.py         # Shfaqja e grafikëve të ruajtur brenda aplikacionit
├── proteina.py         # Modeli HP, energjia dhe dy algoritmet
├── matja.py            # Matja e memories në proces të veçantë
├── eksperimente.py     # Eksperimentet dhe grafikët
├── test_proteina.py    # Testet me unittest
├── requirements.txt    # Varësia Matplotlib
├── RAPORTI.md          # Analiza dhe interpretimi
└── rezultate/          # Tabela CSV dhe grafikët e ruajtur
```

Për të kuptuar kodin, fillo me `proteina.py`, vazhdo me `main.py`, pastaj lexo `matja.py` dhe `eksperimente.py`. Analiza e kompleksitetit kohor dhe hapësinor është te [raporti](RAPORTI.md).

## Kufizimet

- Modeli HP nuk llogarit atomet, tretësin ose forcat reale fizike të proteinës.
- Cilësia varet nga sekuenca, buxheti, temperatura dhe gjerësia Beam; optimumi global nuk garantohet.
- Një kufi kohor mund të tejkalohet pak nga një hap që është duke u kryer.
- Matja me `tracemalloc` nuk përfshin çdo alokim native dhe nuk duhet interpretuar si memorie totale e procesit.
- Ndërfaqja shfaq rezultatet e përfunduara; për të parë konvergjencën përdor grafikun e eksperimenteve.
