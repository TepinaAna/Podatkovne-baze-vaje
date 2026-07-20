import sqlite3

def ustvari_drzava(conn):
    """
    Ustvari tabelo drzava.
    """
    conn.execute("""
        CREATE TABLE drzava(
            id TEXT PRIMARY KEY,
            ime TEXT NOT NULL,
            eu TEXT
        );
    """)

def ustvari_mesto(conn):
    """
    Ustvari tabelo mesto.
    """
    conn.execute("""
        CREATE TABLE mesto(
            id INTEGER PRIMARY KEY,
            ime TEXT NOT NULL,
            priljubljenost REAL,
            priporoceni_dnevi INTEGER,
            drzava_id TEXT NOT NULL,
            FOREIGN KEY (drzava_id) REFERENCES drzava(id)
        );
    """)
    
def ustvari_mesto_koordinate(conn):
    conn.execute("""
        CREATE TABLE mesto_koordinate(
            mesto_id INTEGER PRIMARY KEY,
            latitude REAL NOT NULL CHECK (latitude BETWEEN -90 AND 90),
            longitude REAL NOT NULL CHECK (longitude BETWEEN -180 AND 180),
            vir TEXT,
            FOREIGN KEY (mesto_id) REFERENCES mesto(id)
        );
    """)
    
def ustvari_bliznje_mesto(conn):
    conn.execute("""
        CREATE TABLE bliznje_mesto(
            mesto_id INTEGER NOT NULL,
            bliznje_mesto_id INTEGER NOT NULL,
            razdalja_km REAL NOT NULL CHECK (razdalja_km >= 0),
            PRIMARY KEY (mesto_id, bliznje_mesto_id),
            CHECK (mesto_id <> bliznje_mesto_id),
            FOREIGN KEY (mesto_id) REFERENCES mesto(id),
            FOREIGN KEY (bliznje_mesto_id) REFERENCES mesto(id)
        );
    """)
    
def ustvari_letnicas(conn):
    """
    Ustvari tabelo letnicas.
    """
    conn.execute("""
        CREATE TABLE letni_cas(
            id INTEGER PRIMARY KEY,
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
    ustvari_drzava(conn)
    ustvari_mesto(conn)
    ustvari_mesto_koordinate(conn)
    ustvari_bliznje_mesto(conn)
    ustvari_letnicas(conn)
    ustvari_atrakcije(conn)
    
    
