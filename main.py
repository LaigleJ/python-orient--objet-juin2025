# main.py

import logging
import pandas as pd

from src.mon_module.models.personne import Personne
from src.mon_module.models.epargne import Epargne
from src.mon_module.models.resultat import ResultatEpargne
from src.mon_module.utils import calcul_interets_composes
from src.mon_module.data_manager import import_personnes, import_epargnes, save_personnes, save_epargnes, save_resultats_simulation
from src.mon_module.core import suggestion_epargne

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Tests des classes Personne et Epargne (vos tests précédents, peuvent être commentés/supprimés si vous voulez un output plus court) ---
# Si vous avez des tests spécifiques pour ces classes, vous pouvez les laisser ici.
# print("\n" + "="*50 + "\n")

# --- Tests de la fonction calcul_interets_composes (vos tests précédents) ---
# Si vous avez des tests spécifiques pour cette fonction, vous pouvez les laisser ici.
# print("\n" + "="*50 + "\n")

# --- Tests des fonctions d'importation et d'exportation d'objets ---
print("--- Tests d'importation et d'exportation d'objets ---")

CHEMIN_PERSONNES_CSV = "personnes.csv"
CHEMIN_EPARGNE_CSV = "epargnes.csv"
CHEMIN_PERSONNES_TXT_EXPORT = "personnes_export.txt"
CHEMIN_EPARGNE_XLSX_EXPORT = "epargnes_export.xlsx"
CHEMIN_RESULTATS_SIMULATION_CSV = "resultats_simulations.csv" # Nouveau chemin pour les résultats

# ====================================================================================
# ATTENTION : BLOC DE CRÉATION DE FICHIERS TEMPORAIRES
# COMMENTEZ OU SUPPRIMEZ CE BLOC SI VOUS GÉREZ VOS PROPRES FICHIERS CSV MANUELLEMENT
# ====================================================================================
# try:
#     with open(CHEMIN_PERSONNES_CSV, 'w') as f:
#         f.write("nom,age,revenu_annuel,loyer,depenses_mensuelles,objectif,duree_epargne,versement_mensuel_utilisateur\n")
#         f.write("Jean,30,35000,700,400,15000,60,\n") # Jean: obj 15k, 5 ans (60 mois)
#         f.write("Marie,45,50000,900,600,25000,120,1000\n") # Marie: obj 25k, 10 ans (120 mois), versement utilisateur
#         f.write("Pierre,25,25000,500,300,5000,36,None\n") # Pierre: obj 5k, 3 ans (36 mois)
#         f.write("Sophie,35,40000,800,500,0,0,\n") # Sophie: pas d'objectif, pas de durée, pas de versement utilisateur
# except FileExistsError:
#     pass

# try:
#     with open(CHEMIN_EPARGNE_CSV, 'w') as f:
#         f.write("nom,taux_interet,fiscalite,duree_min,versement_max\n")
#         f.write("Livret A,0.03,0,0,22950\n")
#         f.write("LDDS,0.03,0,0,12000\n")
#         f.write("PEL,0.025,0.30,48,61200\n")
#         f.write("Assurance Vie,0.045,0.172,96,\n")
#         f.write("Crypto Risquee,0.15,0.30,12,None\n")
# except FileExistsError:
#     pass
# ====================================================================================
# FIN DU BLOC TEMPORAIRE DE CRÉATION DE FICHIERS
# ====================================================================================

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

    print(f"\n--- Tests d'exportation d'objets ---")

    print(f"\nTentative d'exportation des personnes vers {CHEMIN_PERSONNES_TXT_EXPORT}...")
    save_personnes(personnes_chargees, CHEMIN_PERSONNES_TXT_EXPORT)
    print(f"Vérification de l'export TXT :")
    personnes_rechargees_txt = import_personnes(CHEMIN_PERSONNES_TXT_EXPORT)
    print(f"  {len(personnes_rechargees_txt)} personnes rechargées depuis le TXT exporté.")

    print(f"\nTentative d'exportation des épargnes vers {CHEMIN_EPARGNE_XLSX_EXPORT}...")
    save_epargnes(epargnes_chargees, CHEMIN_EPARGNE_XLSX_EXPORT)
    print(f"Vérification de l'export XLSX :")
    epargnes_rechargees_xlsx = import_epargnes(CHEMIN_EPARGNE_XLSX_EXPORT)
    print(f"  {len(epargnes_rechargees_xlsx)} produits d'épargne rechargés depuis le XLSX exporté.")

except (FileNotFoundError, ValueError) as e:
    logging.error(f"Une erreur générale est survenue lors de l'import/export : {e}")

print("\n" + "="*50 + "\n")

# --- Tests de la fonction de simulation (suggestion_epargne) ---
print("--- Tests de la fonction de simulation (suggestion_epargne) ---")

try:
    # Charger les personnes et les produits d'épargne pour la simulation
    personnes_pour_simu = import_personnes(CHEMIN_PERSONNES_CSV)
    epargnes_pour_simu = import_epargnes(CHEMIN_EPARGNE_CSV)

    all_simulation_results = [] # Pour stocker tous les résultats pour un éventuel export global
    for p in personnes_pour_simu:
        print(f"\n===== Simulation pour {p.nom} =====")
        scenarios_personne = suggestion_epargne(p, epargnes_pour_simu)

        if not scenarios_personne:
            print(f"Aucun scénario valide trouvé pour {p.nom}.")
            continue

        # Afficher les résultats de simulation pour la personne
        for s in scenarios_personne:
            print(s)
            print("-" * 20) # Séparateur de scénario

        # Ajouter les résultats de cette personne à la liste globale
        all_simulation_results.extend(scenarios_personne)

    # Affichage de tous les résultats dans un DataFrame Pandas (optionnel)
    if all_simulation_results:
        # Concaténer tous les DataFrames individuels des résultats
        df_all_results = pd.concat([s.to_dataframe() for s in all_simulation_results], ignore_index=True)
        print("\n===== Résumé de TOUS les résultats de simulation (DataFrame) =====")
        print(df_all_results.to_string()) # to_string() pour éviter la troncature en console

        # Exportation des résultats de simulation vers un fichier CSV
        save_resultats_simulation(all_simulation_results, CHEMIN_RESULTATS_SIMULATION_CSV)
        print(f"\nRésultats de simulation exportés vers '{CHEMIN_RESULTATS_SIMULATION_CSV}'.")

    else:
        print("\nAucun résultat de simulation à afficher.")


except Exception as e:
    logging.error(f"Erreur critique lors de la simulation : {e}", exc_info=True)