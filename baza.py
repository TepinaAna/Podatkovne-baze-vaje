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
    
def ustvari_znamenitost(conn):
    conn.execute("""
        CREATE TABLE znamenitost(
            id INTEGER PRIMARY KEY,
            ime TEXT NOT NULL,
            ocena INTEGER CHECK (ocena BETWEEN 1 AND 5),
            vstopnina TEXT CHECK (vstopnina IN ('DA', 'NE')),
            za_otroke TEXT CHECK (za_otroke IN ('DA', 'NE')),
            mesto_id INTEGER NOT NULL,
            FOREIGN KEY (mesto_id) REFERENCES mesto(id)
        );
    """)

def ustvari_aktivnost(conn):
    conn.execute("""
        CREATE TABLE aktivnost(
            id INTEGER PRIMARY KEY,
            ime TEXT NOT NULL,
            ocena INTEGER CHECK (ocena BETWEEN 1 AND 5),
            vstopnina TEXT CHECK (vstopnina IN ('DA', 'NE')),
            za_otroke TEXT CHECK (za_otroke IN ('DA', 'NE')),
            mesto_id INTEGER NOT NULL,
            FOREIGN KEY (mesto_id) REFERENCES mesto(id)
        );
    """)
    
def ustvari_aktivnost_letni_cas(conn):
    conn.execute("""
        CREATE TABLE aktivnost_letni_cas(
            aktivnost_id INTEGER,
            letni_cas_id INTEGER,
            PRIMARY KEY (aktivnost_id, letni_cas_id),
            FOREIGN KEY (aktivnost_id) REFERENCES aktivnost(id),
            FOREIGN KEY (letni_cas_id) REFERENCES letni_cas(id)
        );
    """)


def ustvari_dogodek(conn):
    conn.execute("""
        CREATE TABLE dogodek(
            id INTEGER PRIMARY KEY,
            ime TEXT NOT NULL,
            datum TEXT NOT NULL,
            stanje TEXT,
            vstopnina TEXT CHECK (vstopnina IN ('DA', 'NE')),
            za_otroke TEXT CHECK (za_otroke IN ('DA', 'NE')),
            mesto_id INTEGER NOT NULL,
            FOREIGN KEY (mesto_id) REFERENCES mesto(id)
        );
    """)


def ustvari_razdalja(conn):
    conn.execute("""
        CREATE TABLE razdalja(
            id INTEGER PRIMARY KEY,
            znamenitost1_id INTEGER NOT NULL,
            znamenitost2_id INTEGER NOT NULL,
            razdalja_km REAL NOT NULL CHECK (razdalja_km >= 0),
            CHECK (znamenitost1_id <> znamenitost2_id),
            FOREIGN KEY (znamenitost1_id) REFERENCES znamenitost(id),
            FOREIGN KEY (znamenitost2_id) REFERENCES znamenitost(id)
        );
    """)


def ustvari_ocena(conn):
    conn.execute("""
        CREATE TABLE ocena(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mesto_id INTEGER,
            vrednost INTEGER CHECK (vrednost BETWEEN 1 AND 5),
            FOREIGN KEY (mesto_id) REFERENCES mesto(id)
        );
    """)


if __name__ == "__main__":
    conn = sqlite3.connect("baza.sqlite")
    conn.execute("PRAGMA foreign_keys = ON")

    # Omogoča ponovni zagon skripte brez ročnega brisanja datoteke baze.
    conn.executescript("""
        DROP TABLE IF EXISTS ocena;
        DROP TABLE IF EXISTS bliznje_mesto;
        DROP TABLE IF EXISTS mesto_koordinate;
        DROP TABLE IF EXISTS razdalja;
        DROP TABLE IF EXISTS dogodek;
        DROP TABLE IF EXISTS aktivnost_letni_cas;
        DROP TABLE IF EXISTS aktivnost;
        DROP TABLE IF EXISTS znamenitost;
        DROP TABLE IF EXISTS letni_cas;
        DROP TABLE IF EXISTS mesto;
        DROP TABLE IF EXISTS drzava;
    """)

    ustvari_drzava(conn)
    ustvari_mesto(conn)
    ustvari_mesto_koordinate(conn)
    ustvari_bliznje_mesto(conn)
    ustvari_letnicas(conn)
    ustvari_znamenitost(conn)
    ustvari_aktivnost(conn)
    ustvari_aktivnost_letni_cas(conn)
    ustvari_dogodek(conn)
    ustvari_razdalja(conn)
    ustvari_ocena(conn)

    conn.commit()
    conn.close()
    print("PODATKOVNA BAZA JE USTVARJENA")
    
    
