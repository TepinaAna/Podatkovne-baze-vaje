import sqlite3
from flask import Flask, render_template

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
        
    aktivnosti = conn.execute("""
        SELECT id,
               ime,
               ocena,
               vstopnina,
               za_otroke
        FROM aktivnost
        WHERE mesto_id = ?
        ORDER BY ocena DESC, ime
    """, (id,)).fetchall()

    conn.close()
    
    return render_template(
        "mesto.html",
        mesto=mesto_podatki,
        aktivnosti=aktivnosti
    )


if __name__ == "__main__":
    app.run(debug=True)

