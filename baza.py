import sqlite3

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

def ustvari_mesto(conn):
    """
    Ustvari tabelo mesto.
    """
    conn.execute("""
        CREATE TABLE mesto(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ime TEXT NOT NULL,
            drzava INTEGER NOT NULL
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

def ustvari_atrakcije(conn):
    """
    Ustvari tabelo atrakcije.
    """
    conn.execute("""
        CREATE TABLE atrakcije(
            id INTEGER PRIMARY KEY,
            ime TEXT NOT NULL,
            vrsta TEXT CHECK (vrsta IN ("zanimivost", "aktivnost", "dogodek")),
            datum TEXT NOT NULL,
            za_otroke TEXT CHECK (za_otroke IN ("DA", "NE")),
            vstopnina TEXT CHECK (vstopnina IN ("DA", "NE")),
            ocena DECIMAL DEFAULT NULL CHECK (ocena BETWEEN 1 AND 5),
            letni_cas INTEGER 
        );
    """)

if __name__ == "__main__":
    conn = sqlite3.connect("baza.sqlite")
    ustvari_mesto(conn)
    ustvari_drzava(conn)
    ustvari_letnicas(conn)
    ustvari_atrakcije(conn)
    
    
