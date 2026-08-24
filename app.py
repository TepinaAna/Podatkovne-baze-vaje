from flask import Flask, abort, flash, redirect, render_template, request, url_for
from model import Aktivnost, Dogodek, Drzava, LetniCas, Mesto, Ocena, Znamenitost


app = Flask(__name__)
app.secret_key = "obisk-mest-projekt"


@app.route("/")
def index():
    iskanje = request.args.get(
        "mesto",
        ""
    ).strip()

    if iskanje:
        mesta = Mesto.poisci_po_imenu(
            iskanje
        )
    else:
        mesta = Mesto.top_mesta(10)

    return render_template(
        "index.html",
        mesta=mesta,
        iskanje=iskanje
    )

@app.route("/mesto/<int:id>")
def mesto(id):
    samo_za_otroke = (
        request.args.get("za_otroke") == "DA"
    )
    samo_celo_leto = (
        request.args.get("celo_leto") == "DA"
    )

    mesto_podatki = Mesto.poisci_podrobnosti(id)

    if mesto_podatki is None:
        abort(404)

    aktivnosti = Mesto.aktivnosti(
        id,
        samo_za_otroke,
        samo_celo_leto
    )

    znamenitosti = Mesto.znamenitosti(id)
    dogodki = Mesto.dogodki(id)
    razdalje = Mesto.razdalje(id)
    bliznja_mesta = Mesto.bliznja_mesta(id)
    ocena_podatki = Ocena.statistika_za_mesto(id)

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
    podatek = Aktivnost.poisci_podrobnosti(id)

    if podatek is None:
        abort(404)

    letni_casi = podatek.letni_casi()

    return render_template(
        "aktivnost.html",
        aktivnost=podatek,
        letni_casi=letni_casi,
        celo_leto=len(letni_casi) == 4
    )

@app.route("/znamenitost/<int:id>")
def znamenitost(id):
    podatek = Znamenitost.poisci_podrobnosti(id)

    if podatek is None:
        abort(404)

    bliznje = podatek.poisci_bliznje()

    return render_template(
        "znamenitost.html",
        znamenitost=podatek,
        bliznje=bliznje
    )
    
@app.route("/dogodek/<int:id>")
def dogodek(id):
    podatek = Dogodek.poisci_podrobnosti(id)

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

    moznosti = Mesto.moznosti_nocitev()

    mesta = []

    if izbrano_stevilo is not None:
        mesta = Mesto.poisci_po_stevilu_dni(
            izbrano_stevilo
        )

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
                aktivnost=request.form.get(
                    "aktivnost",
                    ""
                ),
                letni_cas=request.form.get(
                    "letni_cas",
                    ""
                ),
                za_otroke=request.form.get(
                    "za_otroke",
                    ""
                ),
                celo_leto=request.form.get(
                    "celo_leto",
                    ""
                )
            )
        )

    izbrana_aktivnost = request.args.get(
        "aktivnost",
        ""
    ).strip()

    izbran_letni_cas = request.args.get(
        "letni_cas",
        ""
    )

    za_otroke = (
        request.args.get("za_otroke") == "DA"
    )

    celo_leto = (
        request.args.get("celo_leto") == "DA"
    )

    rezultati = Aktivnost.isci(
        izbrana_aktivnost,
        izbran_letni_cas,
        za_otroke,
        celo_leto
    )

    letni_casi = LetniCas.poisci_vse_za_filter()

    vrste_aktivnosti = (
        Aktivnost.vrste_aktivnosti()
    )

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

@app.route(
    "/kontinent",
    methods=["GET", "POST"]
)
def kontinent():
    if request.method == "POST":
        return redirect(
            url_for(
                "kontinent",
                kontinent=request.form.get(
                    "kontinent",
                    ""
                )
            )
        )

    izbran = request.args.get(
        "kontinent",
        ""
    )

    kontinenti = Drzava.kontinenti()

    mesta = []

    if izbran:
        mesta = Mesto.poisci_po_kontinentu(
            izbran
        )

    return render_template(
        "kontinent.html",
        kontinenti=kontinenti,
        mesta=mesta,
        izbran=izbran
    )


@app.route("/top")
def top():
    return redirect(
        url_for("index")
    )


@app.route(
    "/oceni/<int:mesto_id>",
    methods=["GET", "POST"]
)
def oceni(mesto_id):
    mesto_podatki = (
        Mesto.poisci_za_ocenjevanje(mesto_id)
    )

    if mesto_podatki is None:
        abort(404)

    if request.method == "POST":
        vrednost = request.form.get(
            "vrednost",
            ""
        )

        try:
            vrednost = int(vrednost)
        except ValueError:
            vrednost = 0

        try:
            Ocena.vstavi(
                mesto_id,
                vrednost
            )
        except ValueError:
            flash(
                "Izberi oceno od 1 do 5.",
                "napaka"
            )

            return redirect(
                url_for(
                    "oceni",
                    mesto_id=mesto_id
                )
            )

        flash(
            "Ocena je bila uspešno shranjena.",
            "uspeh"
        )

        return redirect(
            url_for(
                "mesto",
                id=mesto_id
            )
        )

    ocene = Ocena.statistika_za_mesto(
        mesto_id
    )

    return render_template(
        "oceni.html",
        mesto=mesto_podatki,
        ocene=ocene
    )

@app.errorhandler(404)
def ni_najdeno(_error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)

