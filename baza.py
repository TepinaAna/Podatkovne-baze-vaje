import sqlite3

def ustvari_mesto(conn):
    """
    Ustvari tabelo mesto.
    """
    conn.execute("""
        CREATE TABLE mesto(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ime TEXT NOT NULL,
            drzava INTERGER NOT NULL
        );
    """)

def ustvari_drzava(conn):
    """
    Ustvari tabelo drzava.
    """
    conn.execute("""
        CREATE TABLE drzava(
            id INTEGER PRIMARY KEY,
            ime TEXT NOT NULL
        );
    """)

def ustvari_dogodek(conn):
    """
    Ustvari tabelo dogodek.
    """
    conn.execute("""
        CREATE TABLE dogodek(
            id INTEGER PRIMARY KEY,
            ime TEXT NOT NULL,
            mesto INTEGER NOT NULL,
            datum TEXT NOT NULL,
            za_otroke TEXT CHECK (za_otroke IN ("DA", "NE")),
            vstopnina TEXT CHECK (vstopnina IN ("DA", "NE")),
            stanje TEXT CHECK (stanje IN ("prihajajoč", "se izvaja"))
        );
    """)

def ustvari_letnicas(conn):
    """
    Ustvari tabelo letnicas.
    """
    conn.execute("""
        CREATE TABLE letnicas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ime TEXT NOT NULL
        );
    """)

def ustvari_aktivnosti(conn):
    """
    Ustvari tabelo aktivnosti.
    """
    conn.execute("""
        CREATE TABLE aktivnosti(
            ime TEXT NOT NULL,
            mesto TEXT NOT NULL,
            za_otroke TEXT CHECK (za_otroke IN ("DA", "NE")),
            vstopnina TEXT CHECK (vstopnina IN ("DA", "NE")),
            ocena DECIMAL DEFAULT "null" CHECK (ocena BETWEEN 1 AND 5),
            letni_cas INTEGER             
        );
    """)

def ustvari_znamenitosti(conn):
    """
    Ustvari tabelo znamenitosti.
    """
    conn.execute("""
        CREATE TABLE znamenitosti(
            ime TEXT NOT NULL,
            mesto TEXT NOT NULL,
            za_otroke TEXT CHECK (za_otroke IN ("DA", "NE")),
            vstopnina TEXT CHECK (vstopnina IN ("DA", "NE")),
            ocena DECIMAL DEFAULT "null" CHECK (ocena BETWEEN 1 AND 5)          
        );
    """)

if __name__ == "__main__":
    conn = sqlite3.connect("baza.sqlite")
    ustvari_mesto(conn)
    ustvari_drzava(conn)
    ustvari_dogodek(conn)
    ustvari_letnicas(conn)
    ustvari_aktivnosti(conn)
    ustvari_znamenitosti(conn)