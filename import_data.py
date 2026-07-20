import csv
import os
import sqlite3


conn = sqlite3.connect("baza.sqlite")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()


def uvozi(datoteka, tabela):
    pot = os.path.join("data", datoteka)

    with open(pot, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)  # preskoči glavo

        for vrstica in reader:
            placeholder = ",".join(["?"] * len(vrstica))
            sql = f"INSERT INTO {tabela} VALUES ({placeholder})"
            cursor.execute(sql, vrstica)

    print(f"Uvoženo: {datoteka}")


try:
    # Vrstni red je pomemben zaradi tujih ključev.
    uvozi("drzava.csv", "drzava")
    uvozi("mesto.csv", "mesto")
    uvozi("mesto_koordinate.csv", "mesto_koordinate")
    uvozi("bliznje_mesto.csv", "bliznje_mesto")
    uvozi("letni_cas.csv", "letni_cas")
    uvozi("znamenitost.csv", "znamenitost")
    uvozi("aktivnost.csv", "aktivnost")
    uvozi("aktivnost_letni_cas.csv", "aktivnost_letni_cas")
    uvozi("dogodek.csv", "dogodek")
    uvozi("razdalja.csv", "razdalja")
    conn.commit()
except Exception:
    conn.rollback()
    raise
finally:
    conn.close()

print("VSI PODATKI UVOŽENI")

