from model import Aktivnost, Mesto, Znamenitost


def izberi_mesto():
    iskanje = input(
        "Vnesi ime ali del imena mesta: "
    ).strip()

    if not iskanje:
        print("Ime mesta ne sme biti prazno.")
        return None

    mesta = Mesto.poisci_po_imenu(iskanje)

    if not mesta:
        print("Ni najdenih mest.")
        return None

    if len(mesta) == 1:
        return mesta[0]

    print("\nNajdena mesta:")

    prikazana_mesta = mesta[:20]

    for i, mesto in enumerate(
        prikazana_mesta,
        start=1
    ):
        print(
            f"{i} - {mesto.ime}"
        )

    if len(mesta) > 20:
        print(
            "Prikazanih je prvih 20 rezultatov."
        )

    izbira = input(
        "Izberi številko mesta: "
    ).strip()

    try:
        indeks = int(izbira)
    except ValueError:
        print("Vnesti moraš številko.")
        return None

    if indeks < 1 or indeks > len(prikazana_mesta):
        print("Neveljavna izbira.")
        return None

    return prikazana_mesta[indeks - 1]


def izpisi_mesta():
    mesta = Mesto.poisci_vse()

    print("\nMesta:")

    for mesto in mesta:
        print(
            f"- {mesto.ime}"
        )


def poisci_mesta_po_imenu():
    iskanje = input(
        "Vnesi ime ali del imena mesta: "
    ).strip()

    mesta = Mesto.poisci_po_imenu(
        iskanje
    )

    if not mesta:
        print("Ni rezultatov.")
        return

    print("\nNajdena mesta:")

    for mesto in mesta:
        print(
            f"- {mesto.ime} "
            f"(priljubljenost: "
            f"{mesto.priljubljenost}/5, "
            f"priporočeno dni: "
            f"{mesto.priporoceni_dnevi})"
        )


def izpisi_aktivnosti_v_mestu():
    mesto = izberi_mesto()

    if mesto is None:
        return

    aktivnosti = Aktivnost.poisci_po_mestu(
        mesto.id
    )

    print(
        f"\nAktivnosti v mestu "
        f"{mesto.ime}:"
    )

    if not aktivnosti:
        print("Ni najdenih aktivnosti.")
        return

    for aktivnost in aktivnosti:
        print(
            f"- {aktivnost.ime} "
            f"(ocena: {aktivnost.ocena}/5)"
        )


def izpisi_znamenitosti_v_mestu():
    mesto = izberi_mesto()

    if mesto is None:
        return

    znamenitosti = Znamenitost.poisci_po_mestu(
        mesto.id
    )

    print(
        f"\nZnamenitosti v mestu "
        f"{mesto.ime}:"
    )

    if not znamenitosti:
        print("Ni najdenih znamenitosti.")
        return

    for znamenitost in znamenitosti:
        print(
            f"- {znamenitost.ime} "
            f"(ocena: "
            f"{znamenitost.ocena}/5)"
        )


def izpisi_top_mesta():
    mesta = Mesto.top_mesta(10)

    print("\nTop 10 mest:")

    for i, mesto in enumerate(
        mesta,
        start=1
    ):
        print(
            f"{i}. {mesto.ime} "
            f"- {mesto.priljubljenost}/5"
        )


def meni():
    while True:
        print("\n--- OBISK MEST ---")
        print("1 - Prikaži vsa mesta")
        print("2 - Poišči mesto po imenu")
        print("3 - Aktivnosti v mestu")
        print("4 - Znamenitosti v mestu")
        print("5 - Top 10 mest")
        print("0 - Izhod")

        izbira = input(
            "Izbira: "
        ).strip()

        if izbira == "1":
            izpisi_mesta()

        elif izbira == "2":
            poisci_mesta_po_imenu()

        elif izbira == "3":
            izpisi_aktivnosti_v_mestu()

        elif izbira == "4":
            izpisi_znamenitosti_v_mestu()

        elif izbira == "5":
            izpisi_top_mesta()

        elif izbira == "0":
            print("Izhod.")
            break

        else:
            print("Neveljavna izbira.")


if __name__ == "__main__":
    meni()
