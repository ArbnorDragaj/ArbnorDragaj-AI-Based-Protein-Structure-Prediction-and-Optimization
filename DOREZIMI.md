# Projekti për dorëzim

Ky version përfshin kodin, GUI-në, ekzekutimin nga terminali, importin/eksportin, testet, të dhënat eksperimentale dhe raportin. Nuk kërkon qasje në Kaggle ose në shërbim protein-folding për të punuar. Shembujt dhe eksperimentet bazë janë sintetike dhe shënohen si të tilla.

## Përputhja me kërkesat

| Kërkesa | Implementimi / prova |
|---|---|
| Sekuenca dhe struktura 3D | `proteina.py`: listë koordinatash të plota dhe ndarja HP |
| Refuzimi i strukturave invalide | `valide`: pozicione unike dhe distanca Manhattan 1 për lidhjet |
| Energjia e shpjeguar | Kontakte H–H jo radhazi; formula dhe shembulli i katrorit në raport |
| Dy algoritme dhe teknikë e avancuar | Simulated Annealing dhe Beam Search të implementuara në projekt |
| Arsyetimi i zgjedhjes | SA ndryshon zgjidhje të plota; Beam ndërton alternativa pjesore; raporti shpjegon kompromiset |
| Reduktimi i hapësirës | Gjerësia Beam, refuzimi i përplasjeve dhe fiksimi i lidhjes së parë |
| Përmirësimi lokal | Rrotullime të bishtit në SA, me kontroll të vlefshmërisë |
| Kompleksiteti kohor/hapësinor | `RAPORTI.md`, përfshirë historitë, plotësimet dhe gjurmimin diagnostik |
| Inputet | Sekuenca, gjatësia automatike, pesha, koha, buxheti dhe B; CSV/FASTA opsionale |
| Outputet | Struktura 3D, energjia, kandidatët/plotësimet, validët/invalidët, koha, peak Python dhe krahasimi |
| Pruning-u | Lokal në ekzekutimet kryesore; global ekzakt për universin e deklaruar deri n=8 |
| Eksperimentet dhe shkallëzimi | 180 matje: gjatësi 6,10,18,30,60,100, tri përbërje dhe pesë përsëritje |
| Cilësia dhe konvergjenca | 18 krahasime ekzakte, historitë e ruajtura, nëntë grafikë dhe tabelat statistikore |
| Verifikimi | `kontrollo.py`: sintaksa, testet dhe kontrolli i rezultateve me energji të pavarur |

Hibridi dhe kufizimet strukturore shtesë janë opsionale në kërkesat origjinale dhe nuk janë implementuar. Faktorët e listuar për energjinë janë shembuj të mundshëm; këtu është zgjedhur modeli HP me përplasjet si kufizim i fortë.

## Provimi pas klonimit

1. Përgatit `.venv` dhe instalo `requirements.txt` sipas README-së.
2. Ekzekuto `python kontrollo.py` me Python-in e ambientit. Pa ekran përdor `--pa-gui`.
3. Nis `python main.py` dhe provo parametrat fillestarë.
4. Rrotullo proteinën dhe përdor rrotën e mausit për zoom. Zgjidh strukturën SA ose Beam.
5. Lexo rezultatet dhe hap konvergjencën e rezultatit. Grafikët e eksperimenteve janë seri më vete.
6. Importo njërin nga skedarët `shembuj/sekuenca.*` dhe eksporto rezultatin si JSON/CSV.
7. Provo **Ndalo** me buxhet të madh. Rezultati duhet të mbetet valid dhe të shënohet i pjesshëm.

Shembujt e terminalit dhe dataset-it janë në README. Eksperimentet rigjenerohen me `eksperimente.py`; kjo mbishkruan artefaktet eksperimentale, ndërsa kontrolli i dorëzimit vetëm i lexon.

## Çfarë tregojnë rezultatet

Të 180 strukturat e ruajtura janë verifikuar për vlefshmëri dhe energji me llogaritje të pavarur. Të 18 rastet e zgjedhura me n=4,6,8 arritën optimumin për të dy algoritmet; kjo nuk përgjithësohet për çdo proteinë. Tabelat dhe grafiku i gjerësisë tregojnë kompromiset e kohës, memories dhe energjisë; nuk shpallet një fitues universal.

Memoria është peak i alokimeve Python në proces të veçantë, jo RSS. Numëruesit janë tentativa, jo domosdoshmërisht struktura unike. Plotësimet Beam numërohen veçmas. Pruning-u global mat heqjen nga zgjerimi Beam në universin me origjinën/lidhjen e parë të fiksuar; disa struktura mund të jenë vlerësuar si plotësime. Kufiri n=8 vlen vetëm për enumerimin ekzakt.

## Kufizimet e deklaruara

- Modeli HP në rrjetë nuk është parashikim biologjik atomik dhe nuk provon strukturën reale.
- SA/Beam nuk garantojnë optimum global në rastin e përgjithshëm.
- Koha dhe ndalimi kontrollohen midis hapave; një operacion në vazhdim mund ta vonojë ndalimin.
- Matja e memories mund të ndryshojë numrin e kandidatëve për shkak të ngadalësimit dhe kufirit kohor.
- Dataset-et reale kërkojnë skedar lokal, burim të dokumentuar dhe përputhje të formatit; nuk janë shkarkuar automatikisht.
- Testet e kaluara nuk garantojnë mungesë absolute gabimesh ose një vlerësim të caktuar akademik.

Pas këtij versioni, puna e mëtejshme mund të fokusohet në përmirësime të heuristikave, dataset-e reale dhe optimizim performance pa ndryshuar pretendimet e këtij dorëzimi.
