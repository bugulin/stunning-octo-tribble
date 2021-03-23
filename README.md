# Docházka

Program na evidenci docházky zaměstnanců.


## Specifikace

### Technické detaily

- Python 3, grafická knihovna GTK+ 3
- data v SQLite databázi

### Co by to mělo umět

- zobrazení a editace příchodů a odchodů v jednotlivých dnech daného měsíce
- pohyb v čase (změna měsíce a roku)
- export docházky do souboru
- správa jednotlivých zaměstnanců


## Spuštění

**Požadavky:** Program ke svému běhu potřebuje Python 3, PyGObject (balíček `python-gobject`) a SQLite verze alespoň 3.6.19.

Program se spouští souborem `main.py`.

### Omezení

Podporované roky jsou jen 1 až 9998 kvůli omezení pythonního modulu `datetime` a datového typu v `sqlite3`.

Bohužel některá grafická prostředí ignorují ikonu okna nastavenou samotným programem, takže po spuštění se může aplikace zobrazovat s výchozí ikonou (např. ozubené kolečko). Podobně jsou na tom i ilustrační ikony, které v některých ikonových tématech nejsou dostupné, takže se místo nich zobrazuje např. `<!>`.

## Struktura

Program se skládá ze dvou částí: komunikace s databází a grafické rozhraní.

Rozhraní pro komunikaci s databází umožňuje soubor `database.py`. V souboru `managers.py` je zavedena abstrakce nad databází a umožňuje dotazy na záznamy jako na objekty (ne v pravém slova smyslu).

O grafické rozhraní se starají ostatní soubory, hlavními jsou `application.py` a `window.py`, kde je samotná aplikace a její hlavní okno. Okno aplikace je rozděleno na několik větších widgetů z adresáře `widgets`. Pro přehlednější organizaci se využívají GTK šablony ze speciálních XML souborů, které se nacházejí v adresáři `ui`.

Adresář `data` obsahuje dodatečná data k aplikaci, jako jsou CSS styly nebo ikona.

V adresáři `modules` je místo pro rozšíření aplikace. Budou se tam nacházet skripty rozšiřující funkčnost aplikace, které ale přímo nesouvisí se samotnými úpravami docházky a komunikací s databází. Zatím tam je např. modul pro export dat.

## Zásluhy

Pro logo programu bylo použito:
- ikona kalendáře od <a href="https://www.freepik.com" title="Freepik">Freepik</a> z <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
- <a href='https://www.freepik.com/vectors/logo'>Vektorové logo od freepik - www.freepik.com</a>
