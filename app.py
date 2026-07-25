import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def connect():
    conn = sqlite3.connect("baza.sqlite")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mesta")
def mesta():
    conn = connect()
    seznam_mest = conn.execute("""
        SELECT id, ime, priljubljenost, priporoceni_dnevi
        FROM mesto
        ORDER BY ime
    """).fetchall()
    conn.close()

    return render_template("mesta.html", mesta=seznam_mest)

if __name__ == "__main__":
    app.run(debug=True)

