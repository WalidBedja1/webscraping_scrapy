import re
from itemloaders.processors import MapCompose


def clean(string):
    """Nettoie les chaînes de caractères des caractères indésirables"""
    if not isinstance(string, str):
        return string

    remplacements = {
        "&nbsp;": " ",
        "\n": " ",
        "\t": " ",
        "\r": " ",
        ",\xa0": ", ",
        "Pas de données reprises dans la BCE.": "",
        "'": "",
        '" ': "",
        ' "': "",
        '"': "",
        "  ": " "
    }

    for ancien, nouveau in remplacements.items():
        string = string.replace(ancien, nouveau)

    return string.strip()


def clean_address(address):
    """Nettoie spécifiquement les adresses"""
    if not isinstance(address, str):
        return address

    # Remplace tous les espaces spéciaux et normalise
    address = re.sub(r'[\s\xa0\u200b]+', ' ', address.strip())
    # Nettoie les virgules mal formatées
    address = re.sub(r'\s*,\s*', ', ', address)
    # Formatage des codes postaux (ex: "9070 Destelbergen")
    address = re.sub(r'(\d{4})\s+([A-Za-z-]+)', r'\1 \2', address)

    return address


def convert_date(date_str):
    """Convertit une date en français vers le format JJ/MM/AAAA"""
    if not date_str or not isinstance(date_str, str):
        return date_str

    mois_francais = {
        "janvier": "01", "février": "02", "mars": "03", "avril": "04",
        "mai": "05", "juin": "06", "juillet": "07", "août": "08",
        "septembre": "09", "octobre": "10", "novembre": "11", "décembre": "12"
    }

    try:
        parts = date_str.split()
        if len(parts) != 3:
            return date_str

        jour, mois, annee = parts

        # Validation du mois
        mois_lower = mois.lower()
        if mois_lower not in mois_francais:
            return date_str

        return f"{jour.zfill(2)}/{mois_francais[mois_lower]}/{annee}"

    except Exception:
        return date_str


# Processeurs pour ItemLoader
clean_processor = MapCompose(clean)
address_processor = MapCompose(clean, clean_address)
date_processor = MapCompose(clean, convert_date)