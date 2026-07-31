import sqlite3
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "obisk-mest-projekt"

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

    ocena_podatki = conn.execute("""
        SELECT COUNT(*) AS stevilo_ocen,
            ROUND(AVG(vrednost), 2) AS povprecje
        FROM ocena
        WHERE mesto_id = ?
    """, (id,)).fetchone()

    
    conn.close()
    
    return render_template(
        "mesto.html",
        mesto=mesto_podatki,
        aktivnosti=aktivnosti,
        znamenitosti=znamenitosti,
        dogodki=dogodki,
        razdalje=razdalje,
        bliznja_mesta=bliznja_mesta,
        ocena_podatki=ocena_podatki,
        samo_za_otroke=samo_za_otroke,
        samo_celo_leto=samo_celo_leto
    )
    
@app.route("/aktivnost/<int:id>")
def aktivnost(id):
    conn = connect()

    podatek = conn.execute("""
        SELECT a.id,
               a.ime,
               a.ocena,
               a.vstopnina,
               a.za_otroke,
               m.id AS mesto_id,
               m.ime AS mesto,
               d.ime AS drzava
        FROM aktivnost a
        JOIN mesto m
             ON m.id = a.mesto_id
        JOIN drzava d
             ON d.id = m.drzava_id
        WHERE a.id = ?
    """, (id,)).fetchone()

    if podatek is None:
        conn.close()
        abort(404)

    letni_casi = conn.execute("""
        SELECT lc.id,
               lc.ime
        FROM letni_cas lc
        JOIN aktivnost_letni_cas alc
             ON alc.letni_cas_id = lc.id
        WHERE alc.aktivnost_id = ?
        ORDER BY lc.id
    """, (id,)).fetchall()

    conn.close()

    return render_template(
        "aktivnost.html",
        aktivnost=podatek,
        letni_casi=letni_casi,
        celo_leto=len(letni_casi) == 4
    )

@app.route("/znamenitost/<int:id>")
def znamenitost(id):
    conn = connect()
    podatek = conn.execute("""
        SELECT z.id,
               z.ime,
               z.ocena,
               z.vstopnina,
               z.za_otroke,
               m.id AS mesto_id,
               m.ime AS mesto,
               d.ime AS drzava
        FROM znamenitost z
        JOIN mesto m
             ON m.id = z.mesto_id
        JOIN drzava d
             ON d.id = m.drzava_id
        WHERE z.id = ?
    """, (id,)).fetchone()
    if podatek is None:
        conn.close()
        abort(404)
    bliznje = conn.execute("""
        SELECT
            CASE
                WHEN r.znamenitost1_id = ? THEN z2.id
                ELSE z1.id
            END AS id,
            CASE
                WHEN r.znamenitost1_id = ? THEN z2.ime
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
    """, (id, id, id, id)).fetchall()
    conn.close()
    return render_template(
        "znamenitost.html",
        znamenitost=podatek,
        bliznje=bliznje
    )

@app.route("/dogodek/<int:id>")
def dogodek(id):
    conn = connect()
    podatek = conn.execute("""
        SELECT e.id,
               e.ime,
               e.datum,
               e.stanje,
               e.vstopnina,
               e.za_otroke,
               m.id AS mesto_id,
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
    if podatek is None:
        abort(404)
    return render_template(
        "dogodek.html",
        dogodek=podatek
    )
    
@app.route("/nocitve", methods=["GET", "POST"])
def nocitve():
    if request.method == "POST":
        return redirect(
            url_for(
                "nocitve",
                stevilo=request.form.get("stevilo", "")
            )
        )
    stevilo = request.args.get("stevilo", "")
    izbrano_stevilo = None
    if stevilo:
        try:
            izbrano_stevilo = int(stevilo)
        except ValueError:
            izbrano_stevilo = None
    conn = connect()
    moznosti = conn.execute("""
        SELECT priporoceni_dnevi AS stevilo,
               COUNT(*) AS st_mest
        FROM mesto
        GROUP BY priporoceni_dnevi
        ORDER BY priporoceni_dnevi
    """).fetchall()
    mesta = []
    if izbrano_stevilo is not None:
        mesta = conn.execute("""
            SELECT m.id,
                   m.ime,
                   m.priljubljenost,
                   m.priporoceni_dnevi,
                   d.ime AS drzava,
                   d.eu AS casovni_pas
            FROM mesto m
            JOIN drzava d
                 ON d.id = m.drzava_id
            WHERE m.priporoceni_dnevi = ?
            ORDER BY m.priljubljenost DESC,
                     m.ime
            LIMIT 200
        """, (izbrano_stevilo,)).fetchall()
    conn.close()
    return render_template(
        "nocitve.html",
        moznosti=moznosti,
        mesta=mesta,
        izbrano_stevilo=izbrano_stevilo
    )

@app.route("/iskanje", methods=["GET", "POST"])
def iskanje():
    if request.method == "POST":
        return redirect(
            url_for(
                "iskanje",
                aktivnost=request.form.get("aktivnost", ""),
                letni_cas=request.form.get("letni_cas", ""),
                za_otroke=request.form.get("za_otroke", ""),
                celo_leto=request.form.get("celo_leto", "")
            )
        )
    izbrana_aktivnost = request.args.get(
        "aktivnost", ""
    ).strip()
    izbran_letni_cas = request.args.get(
        "letni_cas", ""
    )
    za_otroke = request.args.get("za_otroke") == "DA"
    celo_leto = request.args.get("celo_leto") == "DA"
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
    if izbrana_aktivnost:
        query += " AND a.ime LIKE ?"
        parametri.append(
            f"{izbrana_aktivnost}%"
        )
    if izbran_letni_cas:
        query += """
            AND EXISTS (
                SELECT 1
                FROM aktivnost_letni_cas alc2
                WHERE alc2.aktivnost_id = a.id
                  AND alc2.letni_cas_id = ?
            )
        """
        parametri.append(izbran_letni_cas)
    if za_otroke:
        query += " AND a.za_otroke = 'DA'"
    query += " GROUP BY a.id"
    if celo_leto:
        query += """
            HAVING COUNT(
                DISTINCT alc.letni_cas_id
            ) = 4
        """
    query += " ORDER BY a.ocena DESC, a.ime LIMIT 200"
    conn = connect()
    rezultati = conn.execute(
        query,
        parametri
    ).fetchall()
    letni_casi = conn.execute("""
        SELECT id, ime
        FROM letni_cas
        ORDER BY id
    """).fetchall()
    vrste_aktivnosti = conn.execute("""
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
    return render_template(
        "iskanje.html",
        rezultati=rezultati,
        letni_casi=letni_casi,
        vrste_aktivnosti=vrste_aktivnosti,
        izbrana_aktivnost=izbrana_aktivnost,
        izbran_letni_cas=izbran_letni_cas,
        za_otroke=za_otroke,
        celo_leto=celo_leto
    )

@app.route("/casovni_pas", methods=["GET", "POST"])
def casovni_pas():
    if request.method == "POST":
        return redirect(
            url_for(
                "casovni_pas",
                pas=request.form.get("pas", "")
            )
        )
    izbran = request.args.get("pas", "")
    conn = connect()
    pasi = conn.execute("""
        SELECT DISTINCT eu
        FROM drzava
        WHERE eu IS NOT NULL
          AND eu <> ''
        ORDER BY eu
    """).fetchall()
    mesta = []
    if izbran:
        mesta = conn.execute("""
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
        """, (izbran,)).fetchall()
    predlogi = conn.execute("""
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
    return render_template(
        "casovni_pas.html",
        pasi=pasi,
        mesta=mesta,
        izbran=izbran,
        predlogi=predlogi
    )

@app.route("/top")
def top():
    conn = connect()
    mesta = conn.execute("""
        SELECT m.id,
               m.ime,
               m.priljubljenost,
               m.priporoceni_dnevi,
               d.ime AS drzava
        FROM mesto m
        JOIN drzava d
             ON d.id = m.drzava_id
        ORDER BY m.priljubljenost DESC,
                 m.ime
        LIMIT 10
    """).fetchall()
    conn.close()
    return render_template(
        "top.html",
        mesta=mesta
    )

@app.route("/oceni/<int:mesto_id>", methods=["GET", "POST"])
def oceni(mesto_id):
    conn = connect()

    mesto_podatki = conn.execute("""
        SELECT m.id,
               m.ime,
               d.ime AS drzava
        FROM mesto m
        JOIN drzava d
             ON d.id = m.drzava_id
        WHERE m.id = ?
    """, (mesto_id,)).fetchone()

    if mesto_podatki is None:
        conn.close()
        abort(404)

    if request.method == "POST":
        vrednost = request.form.get("vrednost", "")

        try:
            vrednost = int(vrednost)
        except ValueError:
            vrednost = 0

        if vrednost < 1 or vrednost > 5:
            conn.close()

            flash(
                "Izberi oceno od 1 do 5.",
                "napaka"
            )

            return redirect(
                url_for("oceni", mesto_id=mesto_id)
            )

        conn.execute("""
            INSERT INTO ocena (mesto_id, vrednost)
            VALUES (?, ?)
        """, (mesto_id, vrednost))

        conn.commit()
        conn.close()

        flash(
            "Ocena je bila uspešno shranjena.",
            "uspeh"
        )

        return redirect(
            url_for("mesto", id=mesto_id)
        )

    ocene = conn.execute("""
        SELECT COUNT(*) AS stevilo_ocen,
               ROUND(AVG(vrednost), 2) AS povprecje
        FROM ocena
        WHERE mesto_id = ?
    """, (mesto_id,)).fetchone()

    conn.close()

    return render_template(
        "oceni.html",
        mesto=mesto_podatki,
        ocene=ocene
    )


if __name__ == "__main__":
    app.run(debug=True)

