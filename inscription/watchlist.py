# inscription/watchlist.py

import os
import pandas as pd
from django.conf import settings

# Chemin vers le fichier de la liste externe
WATCHLIST_PATH = os.path.join(settings.BASE_DIR, "sensitive_ids.xlsx")

# Charger une seule fois au démarrage
if os.path.exists(WATCHLIST_PATH):
    _df_watch = pd.read_excel(WATCHLIST_PATH)
    # On uniformise tout en string
    _df_watch["id_type"] = _df_watch["id_type"].astype(str).str.lower()
    _df_watch["id_number"] = _df_watch["id_number"].astype(str)
    WATCHLIST = set(zip(_df_watch["id_type"], _df_watch["id_number"]))
else:
    WATCHLIST = set()


def is_on_watchlist(id_type: str, id_number: str) -> bool:
    """
    Retourne True si (id_type, id_number) est dans la liste externe.
    """
    if not id_type or not id_number:
        return False
    key = (str(id_type).lower(), str(id_number))
    return key in WATCHLIST