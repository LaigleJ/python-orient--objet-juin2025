# main.py

from src.mon_module.models.personne import Personne
from src.mon_module.models.epargne import Epargne
from src.mon_module.utils import calcul_interets_composes
from src.mon_module.data_manager import importer_donnees, creer_objets_personne_depuis_df, creer_objets_epargne_depuis_df

# --- Tests des classes Personne et Epargne (vos tests précédents) ---
# ... (laissez le code de test des classes Personne et Epargne ici)
print("\n" + "="*50 + "\n")

# --- Tests de la fonction calcul_interets_composes (vos tests précédents) ---
# ... (laissez le code de test de calcul_interets_composes ici)
print("\n" + "="*50 + "\n")

# --- Tests des fonctions d'importation et de création d'objets ---
print("--- Tests d'importation et création d'objets ---")

# Assurez-vous que ces fichiers existent dans votre dossier 'mon_projet/' (ou adaptez le chemin)
CHEMIN_PERSONNES_CSV = "personnes.csv"
CHEMIN_EPARGNE_CSV = "epargnes.csv"

# Créer des fichiers CSV temporaires pour le test si vous n'en avez pas encore
# REMARQUE : retirez ou commentez ce bloc une fois que vous avez vos vrais fichiers
try:
    with open(CHEMIN_PERSONNES_CSV, 'w') as f:
        f.write("nom,age,revenu_annuel,loyer,depenses_mensuelles,versement_mensuel_utilisateur\n")
        f.write("Jean,30,35000,700,400,\n")
        f.write("Marie,45,50000,900,600,1000\n")
        f.write("Pierre,25,25000,500,300,None\n") # Test avec "None" pour l'optionnel
except FileExistsError:
    pass # Le fichier existe déjà, on ne le recrée pas

try:
    with open(CHEMIN_EPARGNE_CSV, 'w') as f:
        f.write("nom,taux_interet,fiscalite,duree_min,versement_max\n")
        f.write("Livret A,0.03,0,0,22950\n")
        f.write("LDDS,0.03,0,0,12000\n")
        f.write("PEL,0.025,0.30,48,61200\n")
        f.write("Assurance Vie,0.045,0.172,96,\n") # Test avec absence de plafond
        f.write("Produit Fisc,0.02,30%,12,None\n") # Test avec pourcentage et "None"
except FileExistsError:
    pass # Le fichier existe déjà, on ne le recrée pas
# FIN DU BLOC TEMPORAIRE

try:
    print(f"\nImportation des données de {CHEMIN_PERSONNES_CSV} :")
    df_personnes = importer_donnees(CHEMIN_PERSONNES_CSV)
    personnes_objets = creer_objets_personne_depuis_df(df_personnes)
    for p in personnes_objets:
        print(p)
    print(f"Nombre de personnes importées : {len(personnes_objets)}")

    print(f"\nImportation des données de {CHEMIN_EPARGNE_CSV} :")
    df_epargnes = importer_donnees(CHEMIN_EPARGNE_CSV)
    epargnes_objets = creer_objets_epargne_depuis_df(df_epargnes)
    for e in epargnes_objets:
        print(e)
    print(f"Nombre de produits d'épargne importés : {len(epargnes_objets)}")

except (FileNotFoundError, ValueError) as e:
    print(f"Une erreur est survenue lors de l'importation : {e}")