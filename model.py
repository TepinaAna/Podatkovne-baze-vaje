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

    @staticmethod
    def casovni_pasovi():
        conn = connect()

        vrstice = conn.execute("""
            SELECT DISTINCT eu
            FROM drzava
            WHERE eu IS NOT NULL
              AND eu <> ''
            ORDER BY eu
        """).fetchall()

        conn.close()

        return vrstice


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
    
    @staticmethod
    def poisci_podrobnosti(id):
        conn = connect()

        vrstica = conn.execute("""
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
            WHERE m.id = ?
        """, (id,)).fetchone()

        conn.close()

        if vrstica is None:
            return None

        return Mesto(
            vrstica["id"],
            vrstica["ime"],
            vrstica["priljubljenost"],
            vrstica["priporoceni_dnevi"],
            vrstica["drzava_id"],
            vrstica["drzava"],
            vrstica["casovni_pas"]
        )
        
    @staticmethod
    def aktivnosti(
        mesto_id,
        samo_za_otroke=False,
        samo_celo_leto=False
    ):
        conn = connect()

        query = """
            SELECT a.id,
                   a.ime,
                   a.ocena,
                   a.vstopnina,
                   a.za_otroke,
                   COUNT(
                       DISTINCT alc.letni_cas_id
                   ) AS stevilo_letnih_casov,
                   GROUP_CONCAT(
                       DISTINCT lc.ime
                   ) AS letni_casi
            FROM aktivnost a
            LEFT JOIN aktivnost_letni_cas alc
                   ON alc.aktivnost_id = a.id
            LEFT JOIN letni_cas lc
                   ON lc.id = alc.letni_cas_id
            WHERE a.mesto_id = ?
        """

        parametri = [mesto_id]

        if samo_za_otroke:
            query += """
                AND a.za_otroke = 'DA'
            """

        query += """
            GROUP BY a.id
        """

        if samo_celo_leto:
            query += """
                HAVING COUNT(
                    DISTINCT alc.letni_cas_id
                ) = 4
            """

        query += """
            ORDER BY a.ocena DESC,
                     a.ime
        """

        vrstice = conn.execute(
            query,
            parametri
        ).fetchall()

        conn.close()

        return vrstice

    @staticmethod
    def znamenitosti(mesto_id):
        return Znamenitost.poisci_po_mestu(
            mesto_id
        )
        
    @staticmethod
    def dogodki(mesto_id):
        return Dogodek.poisci_po_mestu(
            mesto_id
        )

    @staticmethod
    def razdalje(mesto_id):
        conn = connect()

        vrstice = conn.execute("""
            SELECT r.id,
                   z1.id AS znamenitost1_id,
                   z1.ime AS znamenitost1,
                   z2.id AS znamenitost2_id,
                   z2.ime AS znamenitost2,
                   r.razdalja_km
            FROM razdalja r
            JOIN znamenitost z1
                 ON z1.id = r.znamenitost1_id
            JOIN znamenitost z2
                 ON z2.id = r.znamenitost2_id
            WHERE z1.mesto_id = ?
              AND z2.mesto_id = ?
            ORDER BY r.razdalja_km,
                     z1.ime,
                     z2.ime
        """, (
            mesto_id,
            mesto_id
        )).fetchall()

        conn.close()

        return vrstice

    @staticmethod
    def bliznja_mesta(mesto_id):
        conn = connect()

        vrstice = conn.execute("""
            SELECT bm.bliznje_mesto_id AS id,
                   m.ime,
                   m.priljubljenost,
                   m.priporoceni_dnevi,
                   bm.razdalja_km,
                   (
                       SELECT z.ime
                       FROM znamenitost z
                       WHERE z.mesto_id = m.id
                       ORDER BY z.ocena DESC,
                                z.ime
                       LIMIT 1
                   ) AS top_znamenitost
            FROM bliznje_mesto bm
            JOIN mesto m
                 ON m.id = bm.bliznje_mesto_id
            WHERE bm.mesto_id = ?
              AND m.drzava_id = (
                  SELECT drzava_id
                  FROM mesto
                  WHERE id = ?
              )
            ORDER BY bm.razdalja_km,
                     m.priljubljenost DESC,
                     m.ime
            LIMIT 5
        """, (
            mesto_id,
            mesto_id
        )).fetchall()

        conn.close()

        return vrstice
        
    @staticmethod
    def moznosti_nocitev():
        conn = connect()

        vrstice = conn.execute("""
            SELECT priporoceni_dnevi AS stevilo,
                   COUNT(*) AS st_mest
            FROM mesto
            GROUP BY priporoceni_dnevi
            ORDER BY priporoceni_dnevi
        """).fetchall()

        conn.close()

        return vrstice

    @staticmethod
    def poisci_po_stevilu_dni(stevilo):
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
            WHERE m.priporoceni_dnevi = ?
            ORDER BY m.priljubljenost DESC,
                     m.ime
            LIMIT 200
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
        
    @staticmethod
    def poisci_po_casovnem_pasu(pas):
        conn = connect()

        vrstice = conn.execute("""
            SELECT m.id,
                   m.ime,
                   m.priljubljenost,
                   m.priporoceni_dnevi,
                   d.ime AS drzava
            FROM mesto m
            JOIN drzava d
                 ON m.drzava_id = d.id
            WHERE d.eu = ?
            ORDER BY m.priljubljenost DESC,
                     m.ime
        """, (pas,)).fetchall()

        conn.close()

        return vrstice

    @staticmethod
    def predlogi_po_casovnih_pasovih():
        conn = connect()

        vrstice = conn.execute("""
            SELECT casovni_pas,
                   id,
                   ime,
                   priljubljenost,
                   priporoceni_dnevi,
                   drzava
            FROM (
                SELECT d.eu AS casovni_pas,
                       m.id,
                       m.ime,
                       m.priljubljenost,
                       m.priporoceni_dnevi,
                       d.ime AS drzava,
                       ROW_NUMBER() OVER (
                           PARTITION BY d.eu
                           ORDER BY
                               m.priljubljenost DESC,
                               m.ime
                       ) AS vrstni_red
                FROM mesto m
                JOIN drzava d
                     ON d.id = m.drzava_id
                WHERE d.eu IS NOT NULL
                  AND d.eu <> ''
            )
            WHERE vrstni_red = 1
            ORDER BY casovni_pas
        """).fetchall()

        conn.close()

        return vrstice

    @staticmethod
    def poisci_za_ocenjevanje(mesto_id):
        conn = connect()

        vrstica = conn.execute("""
            SELECT m.id,
                   m.ime,
                   d.ime AS drzava
            FROM mesto m
            JOIN drzava d
                 ON d.id = m.drzava_id
            WHERE m.id = ?
        """, (mesto_id,)).fetchone()

        conn.close()

        return vrstica
    
    def poisci_drzavo(self):
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
        mesto_id,
        mesto=None,
        drzava=None
    ):
        self.id = id
        self.ime = ime
        self.ocena = ocena
        self.vstopnina = vstopnina
        self.za_otroke = za_otroke
        self.mesto_id = mesto_id
        self.mesto = mesto
        self.drzava = drzava

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
    def poisci_podrobnosti(id):
        conn = connect()
    
        vrstica = conn.execute("""
            SELECT a.id,
                   a.ime,
                   a.ocena,
                   a.vstopnina,
                   a.za_otroke,
                   a.mesto_id,
                   m.ime AS mesto,
                   d.ime AS drzava
            FROM aktivnost a
            JOIN mesto m
                 ON m.id = a.mesto_id
            JOIN drzava d
                 ON d.id = m.drzava_id
            WHERE a.id = ?
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
            vrstica["mesto_id"],
            vrstica["mesto"],
            vrstica["drzava"]
        )

    @staticmethod
    def isci(
        ime="",
        letni_cas="",
        za_otroke=False,
        celo_leto=False
    ):
        conn = connect()

        query = """
            SELECT a.id,
                   a.ime,
                   a.ocena,
                   a.za_otroke,
                   a.vstopnina,
                   m.id AS mesto_id,
                   m.ime AS mesto,
                   d.ime AS drzava,
                   COUNT(
                       DISTINCT alc.letni_cas_id
                   ) AS stevilo_letnih_casov,
                   GROUP_CONCAT(
                       DISTINCT lc.ime
                   ) AS letni_casi
            FROM aktivnost a
            JOIN mesto m
                 ON m.id = a.mesto_id
            JOIN drzava d
                 ON d.id = m.drzava_id
            LEFT JOIN aktivnost_letni_cas alc
                 ON alc.aktivnost_id = a.id
            LEFT JOIN letni_cas lc
                 ON lc.id = alc.letni_cas_id
            WHERE 1 = 1
        """

        parametri = []

        if ime:
            query += """
                AND LOWER(a.ime) LIKE LOWER(?)
            """
            parametri.append(
                f"%{ime}%"
            )

        if letni_cas:
            query += """
                AND EXISTS (
                    SELECT 1
                    FROM aktivnost_letni_cas alc2
                    WHERE alc2.aktivnost_id = a.id
                      AND alc2.letni_cas_id = ?
                )
            """
            parametri.append(letni_cas)

        if za_otroke:
            query += """
                AND a.za_otroke = 'DA'
            """

        query += """
            GROUP BY a.id
        """

        if celo_leto:
            query += """
                HAVING COUNT(
                    DISTINCT alc.letni_cas_id
                ) = 4
            """

        query += """
            ORDER BY a.ocena DESC,
                     a.ime
            LIMIT 200
        """

        vrstice = conn.execute(
            query,
            parametri
        ).fetchall()

        conn.close()

        return vrstice

    @staticmethod
    def vrste_aktivnosti():
        conn = connect()

        vrstice = conn.execute("""
            SELECT DISTINCT
                CASE
                    WHEN instr(ime, ' – ') > 0
                    THEN substr(
                        ime,
                        1,
                        instr(ime, ' – ') - 1
                    )
                    ELSE ime
                END AS ime
            FROM aktivnost
            ORDER BY ime
        """).fetchall()

        conn.close()

        return vrstice
        

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
        
    def letni_casi(self):
        conn = connect()
    
        vrstice = conn.execute("""
            SELECT lc.id,
                   lc.ime
            FROM letni_cas lc
            JOIN aktivnost_letni_cas alc
                 ON alc.letni_cas_id = lc.id
            WHERE alc.aktivnost_id = ?
            ORDER BY lc.id
        """, (self.id,)).fetchall()
    
        conn.close()
    
        return [
            LetniCas(
                vrstica["id"],
                vrstica["ime"]
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

    @staticmethod
    def poisci_vse_za_filter():
        conn = connect()

        vrstice = conn.execute("""
            SELECT id, ime
            FROM letni_cas
            ORDER BY id
        """).fetchall()

        conn.close()

        return vrstice


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
        mesto_id,
        mesto=None,
        drzava=None
    ):
        self.id = id
        self.ime = ime
        self.ocena = ocena
        self.vstopnina = vstopnina
        self.za_otroke = za_otroke
        self.mesto_id = mesto_id
        self.mesto = mesto
        self.drzava = drzava

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
        
    @staticmethod
    def poisci_podrobnosti(id):
        conn = connect()
        
        vrstica = conn.execute("""
            SELECT z.id,
                   z.ime,
                   z.ocena,
                   z.vstopnina,
                   z.za_otroke,
                   z.mesto_id,
                   m.ime AS mesto,
                   d.ime AS drzava
            FROM znamenitost z
            JOIN mesto m
                 ON m.id = z.mesto_id
            JOIN drzava d
                 ON d.id = m.drzava_id
            WHERE z.id = ?
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
            vrstica["mesto_id"],
            vrstica["mesto"],
            vrstica["drzava"]
        )
        
    def poisci_bliznje(self):
        conn = connect()
    
        vrstice = conn.execute("""
            SELECT
                CASE
                    WHEN r.znamenitost1_id = ?
                    THEN z2.id
                    ELSE z1.id
                END AS id,
                CASE
                    WHEN r.znamenitost1_id = ?
                    THEN z2.ime
                    ELSE z1.ime
                END AS ime,
                r.razdalja_km
            FROM razdalja r
            JOIN znamenitost z1
                 ON z1.id = r.znamenitost1_id
            JOIN znamenitost z2
                 ON z2.id = r.znamenitost2_id
            WHERE r.znamenitost1_id = ?
               OR r.znamenitost2_id = ?
            ORDER BY r.razdalja_km
        """, (
            self.id,
            self.id,
            self.id,
            self.id
        )).fetchall()
    
        conn.close()
    
        return vrstice


class Dogodek:
    def __init__(
        self,
        id,
        ime,
        datum,
        stanje,
        vstopnina,
        za_otroke,
        mesto_id,
        mesto=None,
        drzava=None
    ):
        self.id = id
        self.ime = ime
        self.datum = datum
        self.stanje = stanje
        self.vstopnina = vstopnina
        self.za_otroke = za_otroke
        self.mesto_id = mesto_id
        self.mesto = mesto
        self.drzava = drzava

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
    def poisci_podrobnosti(id):
        conn = connect()
    
        vrstica = conn.execute("""
            SELECT e.id,
                   e.ime,
                   e.datum,
                   e.stanje,
                   e.vstopnina,
                   e.za_otroke,
                   e.mesto_id,
                   m.ime AS mesto,
                   d.ime AS drzava
            FROM dogodek e
            JOIN mesto m
                 ON m.id = e.mesto_id
            JOIN drzava d
                 ON d.id = m.drzava_id
            WHERE e.id = ?
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
            vrstica["mesto_id"],
            vrstica["mesto"],
            vrstica["drzava"]
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
