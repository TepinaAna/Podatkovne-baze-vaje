import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def connect():
    conn = sqlite3.connect("baza.sqlite")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = connect()

    mesta = conn.execute("""
        SELECT m.id,
               m.ime,
               m.priljubljenost,
               m.priporoceni_dnevi,
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

    conn.close()
    
    return render_template(
        "mesto.html",
        mesto=mesto_podatki,
        aktivnosti=aktivnosti,
        znamenitosti=znamenitosti,
        dogodki=dogodki,
        samo_za_otroke=samo_za_otroke,
        samo_celo_leto=samo_celo_leto
    )

if __name__ == "__main__":
    app.run(debug=True)

