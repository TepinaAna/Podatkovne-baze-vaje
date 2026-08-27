# Obisk mest

Namen projekta je razviti spletno aplikacijo za pregledno raziskovanje mest, njihovih aktivnosti, znamenitosti in dogodkov.

## Funkcionalnosti

Mesta je mogoče:
- iskati po imenu ali delu imena,
- filtrirati po časovnem pasu,
- filtrirati po priporočenem številu dni,
- razvrščati po priljubljenosti.

Za posamezno mesto aplikacija prikazuje:
- osnovne podatke o mestu in državi,
- časovni pas,
- uporabniške ocene mesta,
- aktivnosti in njihove letne čase,
- znamenitosti,
- dogodke,
- razdalje med znamenitostmi,
- do pet bližnjih mest v isti državi.

Bližnja mesta niso določena s fiksno kilometrsko mejo. Iz shranjenih povezav se za posamezno mesto prikaže do pet najbližjih mest v isti državi, razvrščenih po razdalji.

Uporabniki lahko mesto ocenijo z oceno od 1 do 5. Uporabniške ocene mesta so ločene od ocen aktivnosti in znamenitosti ter od podatka o priljubljenosti mesta.

## Arhitektura

Projekt je organiziran po namembnosti:
- app.py vsebuje Flask poti in spletno logiko,
- model.py vsebuje dostop do podatkovne baze in podatkovne modele,
- cli.py vsebuje tekstovni uporabniški vmesnik,
- baza.py ustvari strukturo podatkovne baze,
- import_data.py uvozi podatke iz CSV datotek,
- templates vsebuje HTML predloge,
- static vsebuje CSS.

Spletni in tekstovni vmesnik do baze ne dostopata neposredno, ampak uporabljata model.py.

## Zagon

1. Namestite odvisnosti:
    pip install -r requirements.txt

2. Ustvarite podatkovno bazo:
    python baza.py

3. Uvozite podatke:
    python import_data.py

4. Zaženite spletno aplikacijo:
    python app.py

Aplikacija je nato dostopna na naslovu http://127.0.0.1:5000/.

## Tekstovni vmesnik

Za zagon CLI uporabite:
    python cli.py

CLI omogoča najmanj štiri funkcionalnosti: izpis mest, iskanje mesta po imenu, prikaz aktivnosti v izbranem mestu in prikaz znamenitosti v izbranem mestu.

## Opomba o lokalni bazi

Datoteka baza.sqlite ni vključena v repozitorij, ker je *.sqlite v .gitignore. Baza se ustvari lokalno iz baza.py in podatkov v mapi data.

Če imate staro lokalno baza.sqlite iz prejšnje različice sheme, jo izbrišite in ponovno zaženite baza.py ter import_data.py.

<img width="644" height="603" alt="image" src="https://github.com/user-attachments/assets/fa9559bc-4ea4-4d7e-9e66-cac2771b64f1" />

