# Raporti: optimizimi i strukturës së proteinës

## Problemi dhe modeli

Një sekuencë aminoacidesh mund të ketë shumë konfigurime. Këtu çdo aminoacid është një pikë me koordinata të plota `(x,y,z)`. Pozitat duhet të jenë të ndryshme dhe pikat radhazi duhet të kenë distancë Manhattan 1. Koordinatat negative lejohen; renditja ruhet. Një listë mban renditjen dhe një `set` ose `dict` kontrollon pozitat.

Përdorim modelin edukativ HP: A, V, I, L, M, F, W, Y, C janë H; të tjerat janë P. Shkronja **H** në sekuencën origjinale është histidinë dhe klasifikohet P në këtë ndarje të thjeshtuar. H/P nuk përfaqëson të gjitha vetitë reale kimike.

## Funksioni i energjisë

`E = -pesha × numri i kontakteve H–H`.

Kontakt është një çift H–H me distancë Manhattan 1 që nuk janë radhazi në zinxhir. Çdo çift numërohet një herë. Për shembull katër H në katror kanë një kontakt shtesë dhe, me peshë 1, energjinë -1. Zinxhiri i drejtë ka energji 0. Synimi është energji sa më e ulët. Strukturat me përplasje ose lidhje të prishura refuzohen, pa penalitet numerik.

## Simulated Annealing

Fillohet nga zinxhir i drejtë. Në çdo tentativë zgjidhet një pivot dhe bishti rrotullohet me 90° rreth njërit bosht. Kandidati i pavlefshëm refuzohet. Për një kandidat valid llogaritet ndryshimi i energjisë: nëse është më i mirë ose i barabartë pranohet; nëse është më i keq mund të pranohet me probabilitet `exp(-delta/T)`. Temperatura ulet gradualisht. Mbajmë veçmas strukturën aktuale dhe më të mirën. Kjo lëvizje është përmirësimi lokal; pranimi i përkohshëm i përkeqësimeve ndihmon largimin nga disa minimume lokale.

## Beam Search

Fillojmë në origjinë dhe e fiksojmë lidhjen e parë në drejtimin +x: kjo shmang variante të njëjta me rrotullim global. Në secilin hap zgjerojmë prefikset në gjashtë drejtime, refuzojmë përplasjet, rendisim sipas energjisë dhe koordinatave, pastaj ruajmë maksimumi B prefikse. Energjia e prefiksit është heuristikë, jo garanci për rezultat të mirë final. Nëse koha ose buxheti mbaron para një strukture të plotë, kthehet zinxhiri i drejtë valid si rezervë; ai shënohet qartë.

Simulated Annealing ndryshon një strukturë të plotë; Beam Search ndërton shumë alternativa pjesore. I zgjedhim sepse tregojnë dy mënyra të ndryshme kërkimi dhe përmbushin kërkesën për teknikë të avancuar. Asnjëri nuk garanton optimum global.

## Reduktimi dhe kompleksiteti

Refuzimi i përplasjeve heq kandidatë invalidë. Beam ruan vetëm B alternativa në çdo nivel, ndërsa lidhja e parë fiksohet për simetri. Përqindja e shfaqur është `100 × hequr nga Beam / validë të gjeneruar`, ose 0 kur nuk ka validë; **nuk është përqindje e gjithë hapësirës teorike**, e cila nuk është numëruar. SA nuk përdor të njëjtin pruning si Beam.

Për n aminoacide, I tentativa dhe gjerësi B: kontrolli i vlefshmërisë, kopjimi dhe rrotullimi kushtojnë O(n). Energjia kontrollon gjashtë fqinjë për pikë me `dict`: O(n) mesatarisht, duke supozuar operacione hash mesatarisht O(1). SA kushton O(I·n) kohë dhe O(n+I) memorie në rastin më të keq, përfshirë historinë e përmirësimeve. Beam gjeneron deri në 6B zgjerime për nivel dhe i rendit: duke llogaritur se krahasimi i koordinatave në barazime mund të kushtojë O(n), një kufi i sipërm është O(B·n²·log(B+1)) kohë dhe O(B·n+I) memorie me historinë. Koha mund të jetë më e vogël kur mbaron buxheti. Kërkimi i plotë rritet në mënyrë eksponenciale; B më i madh rrit numrin e alternativave, por edhe kohën dhe memorien.

## Matjet dhe eksperimentet

Koha e algoritmit matet me `perf_counter` pa vizatim ose `tracemalloc`. Memoria matet me `tracemalloc` në proces të veçantë, duke riekzekutuar algoritmin; është kulmi i alokimeve Python të gjurmuara, jo RSS apo gjithë memoria e procesit. Kufiri kohor dhe ngadalësimi i matjes mund të ndryshojnë numrin e kandidatëve: edhe ai numër ruhet në tabelë.

Eksperimenti përdor gjatësitë 6, 10, 14, 18 dhe tre familje: hidrofobike, të përziera dhe polare. Për çdo rast SA ekzekutohet me seed 1, 2 dhe 3; Beam është determinist dhe ekzekutohet një herë. Parametrat janë pesha 1, maksimumi 3000 kandidatë, 2 sekonda dhe B=20. Matja e veçantë e memories për SA përdor seed 42 dhe i njëjti rezultat memorieje shfaqet në tre rreshtat SA të atij rasti. Buxhet i barabartë kandidatësh nuk do të thotë punë e barabartë: SA gjeneron struktura të plota, Beam zgjerime prefiksesh.

Të dhënat reale janë në [rezultatet.csv](rezultate/rezultatet.csv), ndërsa grafikët tregojnë energjinë, kohën, memorien, kandidatët dhe konvergjencën. Për familjen vetëm P, E=0 është kontroll i modelit. Koha e matur ndikohet nga kompjuteri dhe ngarkesa e tij; ajo nuk provon kompleksitetin asimptotik ose një fitues të përgjithshëm.

Përmbledhje e matur për n=18, Python 3.14.4 në Windows 11; koha SA është mesatare e tri seed-eve, ndërsa Beam është një ekzekutim. Gjatë serisë në kompjuter kishte edhe procese të tjera aktive.

| Familja | Algoritmi | E më e mirë | E mesatare | Koha mesatare (s) | Peak Python (KiB) |
|---|---|---:|---:|---:|---:|
| Hidrofobike | SA | -13 | -11.67 | 0.3699 | 10.5 |
| Hidrofobike | Beam | -16 | -16 | 0.0567 | 185.5 |
| Përzier | SA | -5 | -5 | 0.4358 | 10.5 |
| Përzier | Beam | -6 | -6 | 0.0454 | 203.5 |
| Polare | SA | 0 | 0 | 0.3691 | 9.0 |
| Polare | Beam | 0 | 0 | 0.0162 | 215.5 |

Në këto raste Beam gjeti energji më të ulët për familjet hidrofobike dhe të përziera, por përdori më shumë memorie të gjurmuar. Kjo nuk provon se Beam është gjithmonë më i mirë. Të 48 strukturat u kontrolluan si valide gjatë eksperimentit.

## Kufizimet

Modeli nuk përmban atome, tretës ose forca reale fizike. Rrjeta është e thjeshtuar. Energjia e prefiksit nuk garanton se Beam gjen strukturën më të mirë. Rezultati rezervë mund të ketë energji 0 nëse buxheti është tepër i vogël. Matja e memories është ekzekutim i veçantë dhe nuk përfshin çdo alokim native. Kufiri kohor kontrollohet mes hapave dhe mund të tejkalohet pak. Hibridi mbetet opsional dhe nuk është implementuar.
