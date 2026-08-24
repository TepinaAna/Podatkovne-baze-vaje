import sqlite3


def connect():
    conn = sqlite3.connect("baza.sqlite")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


class Drzava:
    def __init__(self, id, ime, eu):
        self.id = id
        self.ime = ime
        self.eu = eu

    @staticmethod
    def poisci_vse():
        conn = connect()

        vrstice = conn.execute("""
            SELECT id, ime, eu
            FROM drzava
            ORDER BY ime
        """).fetchall()

        conn.close()

        return [
            Drzava(
                vrstica["id"],
                vrstica["ime"],
                vrstica["eu"]
            )
            for vrstica in vrstice
        ]

    @staticmethod
    def poisci_po_id(id):
        conn = connect()

        vrstica = conn.execute("""
            SELECT id, ime, eu
            FROM drzava
            WHERE id = ?
        """, (id,)).fetchone()

        conn.close()

        if vrstica is None:
            return None

        return Drzava(
            vrstica["id"],
            vrstica["ime"],
            vrstica["eu"]
        )


class Mesto:
    def __init__(
        self,
        id,
        ime,
        priljubljenost,
        priporoceni_dnevi,
        drzava_id,
        drzava=None,
        casovni_pas=None
    ):
        self.id = id
        self.ime = ime
        self.priljubljenost = priljubljenost
        self.priporoceni_dnevi = priporoceni_dnevi
        self.drzava_id = drzava_id
        self.drzava = drzava
        self.casovni_pas = casovni_pas

    @staticmethod
    def poisci_vse():
        conn = connect()

        vrstice = conn.execute("""
            SELECT id,
                   ime,
                   priljubljenost,
                   priporoceni_dnevi,
                   drzava_id
            FROM mesto
            ORDER BY ime
        """).fetchall()

        conn.close()

        return [
            Mesto(
                vrstica["id"],
                vrstica["ime"],
                vrstica["priljubljenost"],
                vrstica["priporoceni_dnevi"],
                vrstica["drzava_id"]
            )
            for vrstica in vrstice
        ]

    @staticmethod
    def poisci_po_id(id):
        conn = connect()

        vrstica = conn.execute("""
            SELECT id,
                   ime,
                   priljubljenost,
                   priporoceni_dnevi,
                   drzava_id
            FROM mesto
            WHERE id = ?
        """, (id,)).fetchone()

        conn.close()

        if vrstica is None:
            return None

        return Mesto(
            vrstica["id"],
            vrstica["ime"],
            vrstica["priljubljenost"],
            vrstica["priporoceni_dnevi"],
            vrstica["drzava_id"]
        )

    @staticmethod
    def poisci_po_imenu(iskanje):
        conn = connect()

        vrstice = conn.execute("""
            SELECT id,
                   ime,
                   priljubljenost,
                   priporoceni_dnevi,
                   drzava_id
            FROM mesto
            WHERE LOWER(ime) LIKE LOWER(?)
            ORDER BY priljubljenost DESC, ime
        """, (f"%{iskanje}%",)).fetchall()

        conn.close()

        return [
            Mesto(
                vrstica["id"],
                vrstica["ime"],
                vrstica["priljubljenost"],
                vrstica["priporoceni_dnevi"],
                vrstica["drzava_id"]
            )
            for vrstica in vrstice
        ]

    @staticmethod
    def top_mesta(stevilo=10):
        conn = connect()
    
        vrstice = conn.execute("""
            SELECT m.id,
                   m.ime,
                   m.priljubljenost,
                   m.priporoceni_dnevi,
                   m.drzava_id,
                   d.ime AS drzava,
                   d.eu AS casovni_pas
            FROM mesto m
            JOIN drzava d
                 ON d.id = m.drzava_id
            ORDER BY m.priljubljenost DESC,
                     m.ime
            LIMIT ?
        """, (stevilo,)).fetchall()
    
        conn.close()
    
        return [
            Mesto(
                vrstica["id"],
                vrstica["ime"],
                vrstica["priljubljenost"],
                vrstica["priporoceni_dnevi"],
                vrstica["drzava_id"],
                vrstica["drzava"],
                vrstica["casovni_pas"]
            )
            for vrstica in vrstice
        ]

    def drzava(self):
        return Drzava.poisci_po_id(self.drzava_id)


class MestoKoordinate:
    def __init__(
        self,
        mesto_id,
        latitude,
        longitude,
        vir
    ):
        self.mesto_id = mesto_id
        self.latitude = latitude
        self.longitude = longitude
        self.vir = vir

    @staticmethod
    def poisci_po_mestu(mesto_id):
        conn = connect()

        vrstica = conn.execute("""
            SELECT mesto_id,
                   latitude,
                   longitude,
                   vir
            FROM mesto_koordinate
            WHERE mesto_id = ?
        """, (mesto_id,)).fetchone()

        conn.close()

        if vrstica is None:
            return None

        return MestoKoordinate(
            vrstica["mesto_id"],
            vrstica["latitude"],
            vrstica["longitude"],
            vrstica["vir"]
        )


class BliznjeMesto:
    def __init__(
        self,
        mesto_id,
        bliznje_mesto_id,
        razdalja_km
    ):
        self.mesto_id = mesto_id
        self.bliznje_mesto_id = bliznje_mesto_id
        self.razdalja_km = razdalja_km

    @staticmethod
    def poisci_za_mesto(mesto_id, omejitev=5):
        conn = connect()

        vrstice = conn.execute("""
            SELECT mesto_id,
                   bliznje_mesto_id,
                   razdalja_km
            FROM bliznje_mesto
            WHERE mesto_id = ?
            ORDER BY razdalja_km
            LIMIT ?
        """, (mesto_id, omejitev)).fetchall()

        conn.close()

        return [
            BliznjeMesto(
                vrstica["mesto_id"],
                vrstica["bliznje_mesto_id"],
                vrstica["razdalja_km"]
            )
            for vrstica in vrstice
        ]


class Aktivnost:
    def __init__(
        self,
        id,
        ime,
        ocena,
        vstopnina,
        za_otroke,
        mesto_id
    ):
        self.id = id
        self.ime = ime
        self.ocena = ocena
        self.vstopnina = vstopnina
        self.za_otroke = za_otroke
        self.mesto_id = mesto_id

    @staticmethod
    def poisci_po_id(id):
        conn = connect()

        vrstica = conn.execute("""
            SELECT id,
                   ime,
                   ocena,
                   vstopnina,
                   za_otroke,
                   mesto_id
            FROM aktivnost
            WHERE id = ?
        """, (id,)).fetchone()

        conn.close()

        if vrstica is None:
            return None

        return Aktivnost(
            vrstica["id"],
            vrstica["ime"],
            vrstica["ocena"],
            vrstica["vstopnina"],
            vrstica["za_otroke"],
            vrstica["mesto_id"]
        )

    @staticmethod
    def poisci_po_mestu(mesto_id):
        conn = connect()

        vrstice = conn.execute("""
            SELECT id,
                   ime,
                   ocena,
                   vstopnina,
                   za_otroke,
                   mesto_id
            FROM aktivnost
            WHERE mesto_id = ?
            ORDER BY ocena DESC, ime
        """, (mesto_id,)).fetchall()

        conn.close()

        return [
            Aktivnost(
                vrstica["id"],
                vrstica["ime"],
                vrstica["ocena"],
                vrstica["vstopnina"],
                vrstica["za_otroke"],
                vrstica["mesto_id"]
            )
            for vrstica in vrstice
        ]


class LetniCas:
    def __init__(self, id, ime):
        self.id = id
        self.ime = ime

    @staticmethod
    def poisci_vse():
        conn = connect()

        vrstice = conn.execute("""
            SELECT id, ime
            FROM letni_cas
            ORDER BY id
        """).fetchall()

        conn.close()

        return [
            LetniCas(
                vrstica["id"],
                vrstica["ime"]
            )
            for vrstica in vrstice
        ]


class AktivnostLetniCas:
    def __init__(
        self,
        aktivnost_id,
        letni_cas_id
    ):
        self.aktivnost_id = aktivnost_id
        self.letni_cas_id = letni_cas_id

    @staticmethod
    def poisci_za_aktivnost(aktivnost_id):
        conn = connect()

        vrstice = conn.execute("""
            SELECT aktivnost_id,
                   letni_cas_id
            FROM aktivnost_letni_cas
            WHERE aktivnost_id = ?
            ORDER BY letni_cas_id
        """, (aktivnost_id,)).fetchall()

        conn.close()

        return [
            AktivnostLetniCas(
                vrstica["aktivnost_id"],
                vrstica["letni_cas_id"]
            )
            for vrstica in vrstice
        ]


class Znamenitost:
    def __init__(
        self,
        id,
        ime,
        ocena,
        vstopnina,
        za_otroke,
        mesto_id
    ):
        self.id = id
        self.ime = ime
        self.ocena = ocena
        self.vstopnina = vstopnina
        self.za_otroke = za_otroke
        self.mesto_id = mesto_id

    @staticmethod
    def poisci_po_id(id):
        conn = connect()

        vrstica = conn.execute("""
            SELECT id,
                   ime,
                   ocena,
                   vstopnina,
                   za_otroke,
                   mesto_id
            FROM znamenitost
            WHERE id = ?
        """, (id,)).fetchone()

        conn.close()

        if vrstica is None:
            return None

        return Znamenitost(
            vrstica["id"],
            vrstica["ime"],
            vrstica["ocena"],
            vrstica["vstopnina"],
            vrstica["za_otroke"],
            vrstica["mesto_id"]
        )

    @staticmethod
    def poisci_po_mestu(mesto_id):
        conn = connect()

        vrstice = conn.execute("""
            SELECT id,
                   ime,
                   ocena,
                   vstopnina,
                   za_otroke,
                   mesto_id
            FROM znamenitost
            WHERE mesto_id = ?
            ORDER BY ocena DESC, ime
        """, (mesto_id,)).fetchall()

        conn.close()

        return [
            Znamenitost(
                vrstica["id"],
                vrstica["ime"],
                vrstica["ocena"],
                vrstica["vstopnina"],
                vrstica["za_otroke"],
                vrstica["mesto_id"]
            )
            for vrstica in vrstice
        ]


class Dogodek:
    def __init__(
        self,
        id,
        ime,
        datum,
        stanje,
        vstopnina,
        za_otroke,
        mesto_id
    ):
        self.id = id
        self.ime = ime
        self.datum = datum
        self.stanje = stanje
        self.vstopnina = vstopnina
        self.za_otroke = za_otroke
        self.mesto_id = mesto_id

    @staticmethod
    def poisci_po_id(id):
        conn = connect()

        vrstica = conn.execute("""
            SELECT id,
                   ime,
                   datum,
                   stanje,
                   vstopnina,
                   za_otroke,
                   mesto_id
            FROM dogodek
            WHERE id = ?
        """, (id,)).fetchone()

        conn.close()

        if vrstica is None:
            return None

        return Dogodek(
            vrstica["id"],
            vrstica["ime"],
            vrstica["datum"],
            vrstica["stanje"],
            vrstica["vstopnina"],
            vrstica["za_otroke"],
            vrstica["mesto_id"]
        )

    @staticmethod
    def poisci_po_mestu(mesto_id):
        conn = connect()

        vrstice = conn.execute("""
            SELECT id,
                   ime,
                   datum,
                   stanje,
                   vstopnina,
                   za_otroke,
                   mesto_id
            FROM dogodek
            WHERE mesto_id = ?
            ORDER BY datum, ime
        """, (mesto_id,)).fetchall()

        conn.close()

        return [
            Dogodek(
                vrstica["id"],
                vrstica["ime"],
                vrstica["datum"],
                vrstica["stanje"],
                vrstica["vstopnina"],
                vrstica["za_otroke"],
                vrstica["mesto_id"]
            )
            for vrstica in vrstice
        ]


class Razdalja:
    def __init__(
        self,
        id,
        znamenitost1_id,
        znamenitost2_id,
        razdalja_km
    ):
        self.id = id
        self.znamenitost1_id = znamenitost1_id
        self.znamenitost2_id = znamenitost2_id
        self.razdalja_km = razdalja_km

    @staticmethod
    def poisci_za_znamenitost(znamenitost_id):
        conn = connect()

        vrstice = conn.execute("""
            SELECT id,
                   znamenitost1_id,
                   znamenitost2_id,
                   razdalja_km
            FROM razdalja
            WHERE znamenitost1_id = ?
               OR znamenitost2_id = ?
            ORDER BY razdalja_km
        """, (
            znamenitost_id,
            znamenitost_id
        )).fetchall()

        conn.close()

        return [
            Razdalja(
                vrstica["id"],
                vrstica["znamenitost1_id"],
                vrstica["znamenitost2_id"],
                vrstica["razdalja_km"]
            )
            for vrstica in vrstice
        ]


class Ocena:
    def __init__(
        self,
        id,
        mesto_id,
        vrednost
    ):
        self.id = id
        self.mesto_id = mesto_id
        self.vrednost = vrednost

    @staticmethod
    def vstavi(mesto_id, vrednost):
        if vrednost < 1 or vrednost > 5:
            raise ValueError(
                "Ocena mora biti med 1 in 5."
            )

        conn = connect()

        conn.execute("""
            INSERT INTO ocena (
                mesto_id,
                vrednost
            )
            VALUES (?, ?)
        """, (
            mesto_id,
            vrednost
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def statistika_za_mesto(mesto_id):
        conn = connect()

        vrstica = conn.execute("""
            SELECT COUNT(*) AS stevilo_ocen,
                   ROUND(
                       AVG(vrednost),
                       2
                   ) AS povprecje
            FROM ocena
            WHERE mesto_id = ?
        """, (mesto_id,)).fetchone()

        conn.close()

        return vrstica
