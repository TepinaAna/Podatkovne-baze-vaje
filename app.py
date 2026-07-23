import sqlite3
from flask import Flask

app = Flask(__name__)

def connect():
    conn = sqlite3.connect("baza.sqlite")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return "Obisk evropskih mest"

@app.route("/mesta")
def mesta():
    conn = connect()
    mesta = conn.execute("""
        SELECT id, ime, priljubljenost, priporoceni_dnevi
        FROM mesto
        ORDER BY ime
    """).fetchall()
    conn.close()

    return {
        "mesta": [dict(mesto) for mesto in mesta]
    }

if __name__ == "__main__":
    app.run(debug=True)

