import sqlite3

def connect():
    return sqlite3.connect("baza.sqlite")

def izpisi_mesta():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT mesto.ime, drzava.ime
        FROM mesto
        JOIN drzava ON mesto.drzava_id = drzava.id
    """)

    for m in cur.fetchall():
        print(f"{m[0]} ({m[1]})")

    conn.close()

def izpisi_aktivnosti_v_mestu():
    mesto = input("Vnesi ime mesta: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT aktivnost.ime
        FROM aktivnost
        JOIN mesto ON aktivnost.mesto_id = mesto.id
        WHERE mesto.ime = ?
    """, (mesto,))

    rezultati = cur.fetchall()

    if rezultati:
        for r in rezultati:
            print("-", r[0])
    else:
        print("Ni rezultatov.")

    conn.close()

def meni():
    while True:
        print("\n1 - PrikaÅ¾i mesta")
        print("2 - Aktivnosti v mestu")
        print("0 - Izhod")

        izbira = input("Izbira: ")

        if izbira == "1":
            izpisi_mesta()
        elif izbira == "2":
            izpisi_aktivnosti_v_mestu()
        elif izbira == "0":
            break

if __name__ == "__main__":
    meni()