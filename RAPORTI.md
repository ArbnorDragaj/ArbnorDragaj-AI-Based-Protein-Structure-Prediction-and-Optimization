# Raporti: optimizimi i strukturës së proteinës

## Modeli dhe objektivi

Proteina është listë e renditur koordinatash të plota (x,y,z) në rrjetë kubike. Çdo pozicion duhet unik dhe dy aminoacide radhazi duhet të kenë distancë Manhattan 1. Struktura invalide refuzohet. Modeli HP është edukativ: A,V,I,L,M,F,W,Y,C klasifikohen H; të tjerat P. Histidina, shkronja H në sekuencë, këtu është P. Nuk modelohen atome, tretës ose forca reale fizike.

E = −pesha × numri i kontakteve H–H jo radhazi. Çdo çift numërohet një herë. Për katër H në katror E=−1 me peshë 1; për një zinxhir të drejtë E=0. Pesha duhet pozitive dhe e fundme. Edhe rezultati i shumëzimit kontrollohet: overflow refuzohet me ValueError, pa kthyer inf/NaN. Energjia dhe algoritmet pranojnë të njëjtin normalizim të sekuencës.

## Simulated Annealing

Nis nga zinxhir i drejtë. Rrotullon bishtin me ±90° rreth njërit bosht në një pivot të brendshëm. Kontrollon vlefshmërinë para energjisë. Pranon përmirësime dhe barazime; përkeqësimet pranohen me exp(−delta/T). T nis 2 dhe ulet me faktor 0.995 deri në dyshemenë 1e−9. Struktura aktuale dhe më e mira ruhen veçmas. Rrotullimet janë mekanizmi i përmirësimit lokal. SA nuk garanton optimum global dhe nuk pretendon se ka vizituar çdo strukturë. Pranimi varet edhe nga shkalla e peshës kundrejt temperaturës.

## Beam Search dhe plotësimi

Origjina fiksohet dhe lidhja e parë vendoset në +x, duke hequr një pjesë të simetrive globale. Prefikset zgjerohen në gjashtë drejtime. Përplasjet refuzohen; kandidatët renditen sipas energjisë së prefiksit dhe koordinatave, pastaj mbahen maksimumi B. Barazimet kanë bias gjeometrik nga koordinatat; kjo është heuristikë dhe jo provë optimaliteti.

Pas një niveli të përfunduar, çdo prefiks i mbajtur provohet për plotësim duke kontrolluar drejtimet me radhë deri te bishti i parë i drejtë valid. Plotësimi pranohet vetëm pa mbivendosje dhe vetëm nëse përmirëson energjinë e zgjidhjes së plotë të ruajtur. Nëse nuk gjendet bisht i drejtë, prefiksi mbetet në kërkim: nuk pretendojmë se ai është i pazgjidhshëm. Kur ka strukturë të plotë të gjeneruar në nivelin final, edhe ajo krahasohet me zgjidhjen më të mirë.

Kështu kufiri kohor ose buxheti nuk e detyron algoritmin ta hedhë një zgjidhje të mirë të plotë të gjetur përmes plotësimit. Zinxhiri fillestar mbetet rezervë valide. Flamuri `rezerve` tregon prejardhjen nga inicializimi/plotësimi, jo strukturë të paplotë. Arsyeja e ndalimit dallon buxhetin, kohën dhe përfundimin e kërkimit.

Numëruesi `gjeneruar` mbulon propozimet SA ose zgjerimet Beam dhe respekton buxhetin. Vlerësimet shtesë të plotësimit Beam ruhen veçmas te `plotesime_te_vleresuara`; shuma e tyre paraqitet në GUI/CSV. Buxheti kufizon propozimet, ndërsa koha përfshin edhe plotësimet. Kandidatët mund të përsëriten; këta janë numërues tentativash, jo numër strukturash unike.

## Reduktimi dhe pruning-u

Pruning lokal = 100 × prefikse të hequra nga gjerësia Beam / kandidatë validë të gjeneruar. Nuk është përqindje e gjithë hapësirës teorike. SA nuk përdor këtë lloj pruning-u.

Për n=4,6,8, referenca numëron të gjitha strukturat valide me origjinën dhe lidhjen e parë +x: 25, 589 dhe 13565. Këto vlera përfshijnë ende simetri të tjera dhe ky univers thuhet shprehimisht. Prefikset e hequra para nivelit final përfaqësojnë nënbashkësi të shkëputura të strukturave përfundimtare. Numërojmë ekzakt sa struktura bien nën këto prefikse. Heqjet në nivelin final përjashtohen nga kjo metrikë, sepse ato struktura tashmë janë zgjeruar dhe vlerësuar.

Kontrollojmë identitetin: struktura totale = struktura nën prefikset e hequra + struktura të plota të gjeneruara nga zgjerimi Beam, kur kërkimi përfundon. Kjo mat heqjen nga zgjerimi, jo domosdoshmërisht mosvlerësimin e energjisë: disa struktura mund të jenë provuar si plotësime. Për gjatësi më të mëdha nuk shpikim përqindje globale. Kufiri 8 vlen vetëm për enumerimin diagnostik, jo për algoritmet kryesore.

## Referenca e pavarur dhe cilësia

`referenca.py` përdor enumerim të plotë dhe llogarit energjinë duke kontrolluar drejtpërdrejt të gjitha çiftet jo radhazi, pa funksionin e energjisë/kontakteve të algoritmeve. Për rastet e vogla raportohet hendeku E − optimumi; zero do të thotë optimum i gjetur për modelin. Asnjë rezultat nuk lejohet të ketë energji më të ulët se optimumi ekzakt.

Testet kontrollojnë edhe Beam me gjerësi mjaft të madhe që të mos heqë kandidatë: në raste të vogla ai duhet të përputhet me optimumin. Për gjatësi të mëdha krahasimi mbetet relativ mes heuristikave; nuk pretendohet cilësi biologjike ose optimum i provuar.

## Kompleksiteti

Me n aminoacide, I propozime dhe gjerësi B: kopjimi, rrotullimi, vlefshmëria dhe energjia kushtojnë O(n) mesatarisht, duke supozuar hash O(1) mesatarisht. Numrat e koordinatave trajtohen sipas modelit të zakonshëm të kostos së operacioneve.

SA: O(I·n) kohë, O(n+I) memorie për strukturat dhe historinë. Beam: deri 6B kandidatë për nivel, O(n) për kandidat dhe O(n) krahasim koordinatash në barazime gjatë renditjes; kufi i sipërm O(B·n²·log(B+1)) kohë. Plotësimet me deri gjashtë bishta kanë O(n) kosto për prefiks dhe mbeten brenda këtij kufiri. Memoria bazë O(B·n+I), përfshirë historinë. Me gjurmimin diagnostik të prefikseve të hequra mund të shtohet O(I·n) memorie; ai është i çaktivizuar në matjet kryesore. Enumerimi i plotë mbetet eksponencial.

Buxheti dhe koha kontrollohen mes hapave, jo gjatë çdo operacioni; inicializimi, renditja, një vlerësim apo plotësim mund ta tejkalojë afatin. Kjo nuk është garanci real-time. Matjet empirike nuk provojnë kompleksitetin asimptotik.

## Protokolli eksperimental

Gjatësitë: 6,10,18,30,60,100. Familjet: hidrofobike, të përziera dhe polare. Pesë seed-e SA (1–5) dhe pesë përsëritje Beam për rast: 180 matje. Parametrat: pesha 1, buxheti 3000 propozime, koha 1 s për algoritëm, B=20. Rendi i algoritmeve alternohet. Beam është determinist kur ndërpritet nga i njëjti buxhet; koha dhe ndërprerja kohore mund të ndryshojnë mes përsëritjeve.

Koha matet pa vizatim dhe pa tracemalloc. Për çdo matje, memoria riekzekutohet në proces të veçantë me të njëjtin seed dhe parametra. Është peak i alokimeve Python të gjurmuara, jo RSS ose RAM i plotë. Ngadalësimi i tracemalloc dhe kufiri kohor mund të ndryshojnë numrin e kandidatëve dhe energjinë; të dyja ruhen veçmas. Përsëritjet Beam nuk janë raste të pavarura rastësore të zgjidhjes: shërbejnë për ndryshueshmërinë e performancës.

`permbledhja.csv` dhe vijat e gabimit japin mesatare ±1 devijim standard të mostrës, jo interval besueshmërie. Konvergjenca jep energjinë më të mirë sipas kandidatëve, për çdo familje/gjatësi; pas ndalimit mbahet rezultati final. Për kohën e përmirësimit ruhet veçmas `koha_me_e_mire_s`. Një kandidat SA dhe një zgjerim Beam nuk janë e njëjta sasi pune.

Eksperimenti i gjerësisë ka B=5,20,60, gjatësi 30,60 dhe tri përsëritje: 18 prova. B më i madh nuk garanton energji më të mirë brenda një buxheti të caktuar, sepse ndryshon shpërndarjen e punës mes gjerësisë dhe thellësisë. Familja polare me E=0 kontrollon funksionin e modelit; nuk dëshmon epërsi optimizimi.

## Rezultatet e serisë aktuale, n=100

Tabela gjenerohet nga të dhënat reale. Për interpretim përdoren bashkë energjia, koha, memoria dhe përdorimi i rezervës; nuk shpallet fitues universal.

| Familja | Algoritmi | E më e mirë | E mesatare | Koha mesatare (s) | Peak Python mesatar (KiB) | Plotësime rezervë / 5 |
|---|---|---:|---:|---:|---:|---:|
| hidrofobike | SA | -66 | -60.00 | 0.6946 | 61.3 | 0 |
| hidrofobike | Beam | -30 | -30.00 | 0.1784 | 294.7 | 5 |
| përzier | SA | -27 | -23.40 | 0.5709 | 61.9 | 0 |
| përzier | Beam | -14 | -14.00 | 0.1686 | 313.2 | 5 |
| polare | SA | 0 | 0.00 | 0.7839 | 53.7 | 0 |
| polare | Beam | 0 | 0.00 | 0.1368 | 319.6 | 5 |

## Verifikimi dhe kufizimet

`python -m unittest -v` ekzekuton kontrollet e modelit dhe algoritmeve. `python verifiko_rezultatet.py` kontrollon koordinatat dhe energjinë e 180 rezultateve me llogaritje të pavarur, numëruesit, historitë monotone, përmbledhjet statistikore, 18 referencat dhe praninë e grafikëve. Të dhënat e plota ruhen, jo vetëm imazhet.

Këto kontrolle rrisin besueshmërinë, por nuk garantojnë mungesë absolute gabimesh. HP mbetet thjeshtim; SA/Beam nuk garantojnë optimum për rastet e përgjithshme. Kufizimet strukturore shtesë dhe hibridi janë opsionale në detyrë dhe nuk janë shtuar. Python dhe Matplotlib nuk zëvendësojnë algoritmet: kërkimi dhe modeli janë implementuar në projekt; Matplotlib vizaton.
