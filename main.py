
import logging # Pour configurer le logging global
from src.mon_module.models.personne import Personne
from src.mon_module.models.epargne import Epargne
from src.mon_module.utils import calcul_interets_composes
from src.mon_module.data_manager import import_personnes, import_epargnes, save_personnes, save_epargnes

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print("\n" + "="*50 + "\n")

print("\n" + "="*50 + "\n")

# --- Tests des fonctions d'importation et de création d'objets ---
print("--- Tests d'importation et création d'objets ---")

CHEMIN_PERSONNES_CSV = "personnes.csv"
CHEMIN_EPARGNE_CSV = "epargnes.csv"
CHEMIN_PERSONNES_TXT_EXPORT = "personnes_export.txt" # Nouveau fichier d'export
CHEMIN_EPARGNE_XLSX_EXPORT = "epargnes_export.xlsx" # Nouveau fichier d'export

# Bloc temporaire pour créer des fichiers de test
try:
    with open(CHEMIN_PERSONNES_CSV, 'w') as f:
        f.write("nom,age,revenu_annuel,loyer,depenses_mensuelles,versement_mensuel_utilisateur\n")
        f.write("Jean,30,35000,700,400,\n")
        f.write("Marie,45,50000,900,600,1000\n")
        f.write("Pierre,25,25000,500,300,None\n")
except FileExistsError:
    pass

try:
    with open(CHEMIN_EPARGNE_CSV, 'w') as f:
        f.write("nom,taux_interet,fiscalite,duree_min,versement_max\n")
        f.write("Livret A,0.03,0,0,22950\n")
        f.write("LDDS,0.03,0,0,12000\n")
        f.write("PEL,0.025,0.30,48,61200\n")
        f.write("Assurance Vie,0.045,0.172,96,\n")
        f.write("Produit Fisc,0.02,30%,12,None\n")
except FileExistsError:
    pass
# FIN DU BLOC TEMPORAIRE

try:
    print(f"\nTentative d'importation de {CHEMIN_PERSONNES_CSV}...")
    personnes_chargees = import_personnes(CHEMIN_PERSONNES_CSV)
    for p in personnes_chargees:
        print(p)
    print(f"Total personnes importées : {len(personnes_chargees)}")

    print(f"\nTentative d'importation de {CHEMIN_EPARGNE_CSV}...")
    epargnes_chargees = import_epargnes(CHEMIN_EPARGNE_CSV)
    for e in epargnes_chargees:
        print(e)
    print(f"Total produits d'épargne importés : {len(epargnes_chargees)}")

    # --- Test des fonctions d'exportation ---
    print(f"\n--- Tests d'exportation d'objets ---")

    # Export des personnes vers un fichier TXT
    print(f"\nTentative d'exportation des personnes vers {CHEMIN_PERSONNES_TXT_EXPORT}...")
    save_personnes(personnes_chargees, CHEMIN_PERSONNES_TXT_EXPORT)
    # Vérifier l'export en réimportant (facultatif, mais bonne pratique)
    print(f"Vérification de l'export TXT :")
    personnes_rechargees_txt = import_personnes(CHEMIN_PERSONNES_TXT_EXPORT)
    print(f"  {len(personnes_rechargees_txt)} personnes rechargées depuis le TXT exporté.")


    # Export des épargnes vers un fichier XLSX
    print(f"\nTentative d'exportation des épargnes vers {CHEMIN_EPARGNE_XLSX_EXPORT}...")
    save_epargnes(epargnes_chargees, CHEMIN_EPARGNE_XLSX_EXPORT)
    # Vérifier l'export en réimportant
    print(f"Vérification de l'export XLSX :")
    epargnes_rechargees_xlsx = import_epargnes(CHEMIN_EPARGNE_XLSX_EXPORT)
    print(f"  {len(epargnes_rechargees_xlsx)} produits d'épargne rechargés depuis le XLSX exporté.")

except (FileNotFoundError, ValueError) as e:
    logging.error(f"Une erreur générale est survenue dans main.py : {e}")