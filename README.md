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


## Zásluhy

Pro logo programu bylo použito:
- ikona kalendáře od <a href="https://www.freepik.com" title="Freepik">Freepik</a> z <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
- <a href='https://www.freepik.com/vectors/logo'>Vektorové logo od freepik - www.freepik.com</a>
