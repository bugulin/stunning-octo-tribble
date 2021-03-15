# Docházka

Program na evidenci docházky zaměstnanců.

### Technické detaily

- Python, grafická knihovna GTK+ 3
- data v SQLite databázi

### Co by to mělo umět

- zobrazení a editace příchodů a odchodů v jednotlivých dnech daného měsíce
- pohyb v čase (změna měsíce a roku)
- export docházky do souboru
- správa jednotlivých zaměstnanců

## Požadavky

Program ke svému běhu potřebuje Python 3, PyGObject (balíček `python-gobject`) a SQLite verze alespoň 3.6.19.

### Omezení

Podporované roky jsou jen 1 až 9998 kvůli omezení pythonního modulu `datetime` a datového typu v `sqlite3`.
