import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def connect():
    conn = sqlite3.connect("baza.sqlite")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

@app.route("/")
def index():
    conn = connect()

    mesta = conn.execute("""
        SELECT m.id,
               m.ime,
               m.priljubljenost,
               m.priporoceni_dnevi,
               d.id AS drzava_id,
               d.ime AS drzava
        FROM mesto m
        JOIN drzava d ON d.id = m.drzava_id
        ORDER BY m.priljubljenost DESC, m.ime
        LIMIT 12
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        mesta=mesta
    )

@app.route("/mesto/<int:id>")
def mesto(id):
    samo_za_otroke = request.args.get("za_otroke") == "DA"
    samo_celo_leto = request.args.get("celo_leto") == "DA"
    conn = connect()
 
    mesto_podatki = conn.execute("""
        SELECT m.id,
               m.ime,
               m.priljubljenost,
               m.priporoceni_dnevi,
               d.id AS drzava_id,
               d.ime AS drzava,
               d.eu AS casovni_pas
        FROM mesto m
        JOIN drzava d ON d.id = m.drzava_id
        WHERE m.id = ?
    """, (id,)).fetchone()
 
 
    if mesto_podatki is None:
        conn.close()
        return "Mesto ne obstaja.", 404
        
    query_aktivnosti = """
        SELECT a.id,
               a.ime,
               a.ocena,
               a.vstopnina,
               a.za_otroke,
               COUNT(DISTINCT alc.letni_cas_id) AS stevilo_letnih_casov,
               GROUP_CONCAT(DISTINCT lc.ime) AS letni_casi
        FROM aktivnost a
        LEFT JOIN aktivnost_letni_cas alc
               ON alc.aktivnost_id = a.id
        LEFT JOIN letni_cas lc
               ON lc.id = alc.letni_cas_id
        WHERE a.mesto_id = ?
    """
    parametri = [id]
    
    if samo_za_otroke:
        query_aktivnosti += " AND a.za_otroke = 'DA'"
        
    query_aktivnosti += " GROUP BY a.id"
    
    if samo_celo_leto:
        query_aktivnosti += """
            HAVING COUNT(DISTINCT alc.letni_cas_id) = 4
        """
        
    query_aktivnosti += " ORDER BY a.ocena DESC, a.ime"
    
    aktivnosti = conn.execute(
        query_aktivnosti,
        parametri
    ).fetchall()

    znamenitosti = conn.execute("""
        SELECT id,
               ime,
               ocena,
               vstopnina,
               za_otroke
        FROM znamenitost
        WHERE mesto_id = ?
        ORDER BY ocena DESC, ime
    """, (id,)
    ).fetchall()

    dogodki = conn.execute("""
        SELECT id,
               ime,
               datum,
               stanje,
               vstopnina,
               za_otroke
        FROM dogodek
        WHERE mesto_id = ?
        ORDER BY datum, ime
    """, (id,)
    ).fetchall()

    razdalje = conn.execute("""
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
        ORDER BY r.razdalja_km, z1.ime, z2.ime
    """, (id, id)).fetchall()

    bliznja_mesta = conn.execute("""
        SELECT bm.bliznje_mesto_id AS id,
               m.ime,
               m.priljubljenost,
               m.priporoceni_dnevi,
               bm.razdalja_km,
               (
                   SELECT z.ime
                   FROM znamenitost z
                   WHERE z.mesto_id = m.id
                   ORDER BY z.ocena DESC, z.ime
                   LIMIT 1
               ) AS top_znamenitost
        FROM bliznje_mesto bm
        JOIN mesto m
             ON m.id = bm.bliznje_mesto_id
        WHERE bm.mesto_id = ?
          AND m.drzava_id = ?
        ORDER BY bm.razdalja_km,
                 m.priljubljenost DESC,
                 m.ime
        LIMIT 5
    """, (id, mesto_podatki["drzava_id"])).fetchall()
    
    conn.close()
    
    return render_template(
        "mesto.html",
        mesto=mesto_podatki,
        aktivnosti=aktivnosti,
        znamenitosti=znamenitosti,
        dogodki=dogodki,
        razdalje=razdalje,
        bliznja_mesta=bliznja_mesta,
        samo_za_otroke=samo_za_otroke,
        samo_celo_leto=samo_celo_leto
    )

if __name__ == "__main__":
    app.run(debug=True)

