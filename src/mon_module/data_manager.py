
import pandas as pd
import os
import logging 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from src.mon_module.models.personne import Personne
from src.mon_module.models.epargne import Epargne
from src.mon_module.data_cleaning import nettoyer_dataframe, nettoyer_nombre, nettoyer_taux


def importer_donnees_dataframe(chemin_fichier: str) -> pd.DataFrame:
    """
    Importe les données depuis un fichier CSV, TXT ou XLSX et les retourne sous forme de DataFrame Pandas.
    Cette fonction est générique pour la lecture de fichier brut avant nettoyage spécifique.

    Args:
        chemin_fichier (str): Chemin complet vers le fichier de données (CSV, TXT, XLSX).

    Returns:
        pd.DataFrame: Un DataFrame Pandas contenant les données brutes lues.

    Raises:
        FileNotFoundError: Si le fichier n'est pas trouvé.
        ValueError: Si le format de fichier n'est pas supporté.
    """
    extension = os.path.splitext(chemin_fichier)[1].lower()
    df = None

    try:
        if extension == '.csv':
            df = pd.read_csv(chemin_fichier)
        elif extension == '.txt':
            df = pd.read_csv(chemin_fichier, sep='\t')
        elif extension == '.xlsx':
            df = pd.read_excel(chemin_fichier)
        else:
            raise ValueError(f"Format de fichier non supporté : {extension}. Les formats supportés sont .csv, .txt, .xlsx.")
        logging.info(f"Fichier '{chemin_fichier}' importé avec succès dans un DataFrame.")
        return df

    except FileNotFoundError:
        logging.error(f"Erreur: Le fichier '{chemin_fichier}' n'a pas été trouvé.")
        raise
    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier '{chemin_fichier}' : {e}")
        raise ValueError(f"Impossible de lire le fichier '{chemin_fichier}' : {e}")


def import_personnes(fichier: str) -> list[Personne]:
    """
    Importe les données de personnes depuis un fichier, les nettoie et les convertit en objets Personne.

    Args:
        fichier (str): Chemin du fichier CSV, TXT ou XLSX contenant les données des personnes.

    Returns:
        list[Personne]: Liste d'objets Personne.

    Raises:
        ValueError: Si une erreur survient lors de l'importation ou de la création des objets.
    """
    logging.info(f"Début de l'importation des personnes depuis '{fichier}'.")
    try:
        df = importer_donnees_dataframe(fichier)
        df_nettoye = nettoyer_dataframe(df.copy()) # Applique le nettoyage
        personnes = []
        for index, row in df_nettoye.iterrows():
            try:
                personne = Personne(
                    nom=row['nom'],
                    age=row['age'],
                    revenu_annuel=row['revenu_annuel'],
                    loyer=row['loyer'],
                    depenses_mensuelles=row['depenses_mensuelles'],
                    
                    versement_mensuel_utilisateur=row.get('versement_mensuel_utilisateur') # .get() pour np.nan
                )
                personnes.append(personne)
            except KeyError as e:
                logging.error(f"Colonne manquante pour la création d'objet Personne à la ligne {index+2} : {e}. Vérifiez le fichier.")
                raise ValueError(f"Données Personne invalides : colonne '{e}' manquante.")
            except Exception as e:
                logging.error(f"Erreur inattendue lors de la création d'un objet Personne à la ligne {index+2} : {e}")
                raise ValueError(f"Erreur de création d'objet Personne : {e}")
        logging.info(f"{len(personnes)} personnes importées avec succès depuis '{fichier}'.")
        return personnes
    except Exception as e:
        logging.error(f"Échec de l'importation des personnes depuis '{fichier}' : {e}")
        raise

def import_epargnes(fichier: str) -> list[Epargne]:
    """
    Importe les données des produits d'épargne depuis un fichier, les nettoie et les convertit en objets Epargne.

    Args:
        fichier (str): Chemin du fichier CSV, TXT ou XLSX contenant les données d'épargne.

    Returns:
        list[Epargne]: Liste d'objets Epargne.

    Raises:
        ValueError: Si une erreur survient lors de l'importation ou de la création des objets.
    """
    logging.info(f"Début de l'importation des produits d'épargne depuis '{fichier}'.")
    try:
        df = importer_donnees_dataframe(fichier)
        df_nettoye = nettoyer_dataframe(df.copy()) # Applique le nettoyage
        epargnes = []
        for index, row in df_nettoye.iterrows():
            try:
                epargne = Epargne(
                    nom=row['nom'],
                    taux_interet=row['taux_interet'],
                    fiscalite=row['fiscalite'],
                    duree_min=row['duree_min'],
                    versement_max=row.get('versement_max') # .get() pour np.nan
                )
                epargnes.append(epargne)
            except KeyError as e:
                logging.error(f"Colonne manquante pour la création d'objet Epargne à la ligne {index+2} : {e}. Vérifiez le fichier.")
                raise ValueError(f"Données Epargne invalides : colonne '{e}' manquante.")
            except Exception as e:
                logging.error(f"Erreur inattendue lors de la création d'un objet Epargne à la ligne {index+2} : {e}")
                raise ValueError(f"Erreur de création d'objet Epargne : {e}")
        logging.info(f"{len(epargnes)} produits d'épargne importés avec succès depuis '{fichier}'.")
        return epargnes
    except Exception as e:
        logging.error(f"Échec de l'importation des produits d'épargne depuis '{fichier}' : {e}")
        raise

def save_personnes(personnes: list[Personne], fichier: str):
    """
    Exporte une liste d'objets Personne vers un fichier CSV, TXT ou XLSX.

    Args:
        personnes (list[Personne]): Liste d'objets Personne à exporter.
        fichier (str): Chemin du fichier de destination.
    """
    logging.info(f"Début de l'exportation des personnes vers '{fichier}'.")
    try:
        # Convertir la liste d'objets en un dictionnaire de listes pour créer le DataFrame
        data = {
            'nom': [p.nom for p in personnes],
            'age': [p.age for p in personnes],
            'revenu_annuel': [p.revenu_annuel for p in personnes],
            'loyer': [p.loyer for p in personnes],
            'depenses_mensuelles': [p.depenses_mensuelles for p in personnes],
            'objectif': [p.objectif for p in personnes],
            'duree_epargne': [p.duree_epargne for p in personnes],
            'versement_mensuel_utilisateur': [p.versement_mensuel_utilisateur for p in personnes]
        }
        df = pd.DataFrame(data)

        extension = os.path.splitext(fichier)[1].lower()
        if extension == '.csv':
            df.to_csv(fichier, index=False)
        elif extension == '.txt':
            df.to_csv(fichier, sep='\t', index=False)
        elif extension == '.xlsx':
            df.to_excel(fichier, index=False)
        else:
            raise ValueError(f"Format de fichier non supporté pour l'export : {extension}. Formats supportés : .csv, .txt, .xlsx.")
        logging.info(f"{len(personnes)} personnes exportées avec succès vers '{fichier}'.")
    except Exception as e:
        logging.error(f"Échec de l'exportation des personnes vers '{fichier}' : {e}")
        raise

def save_epargnes(epargnes: list[Epargne], fichier: str):
    """
    Exporte une liste d'objets Epargne vers un fichier CSV, TXT ou XLSX.

    Args:
        epargnes (list[Epargne]): Liste d'objets Epargne à exporter.
        fichier (str): Chemin du fichier de destination.
    """
    logging.info(f"Début de l'exportation des produits d'épargne vers '{fichier}'.")
    try:
        data = {
            'nom': [e.nom for e in epargnes],
            'taux_interet': [e.taux_interet for e in epargnes],
            'fiscalite': [e.fiscalite for e in epargnes],
            'duree_min': [e.duree_min for e in epargnes],
            'versement_max': [e.versement_max for e in epargnes]
        }
        df = pd.DataFrame(data)

        extension = os.path.splitext(fichier)[1].lower()
        if extension == '.csv':
            df.to_csv(fichier, index=False)
        elif extension == '.txt':
            df.to_csv(fichier, sep='\t', index=False)
        elif extension == '.xlsx':
            df.to_excel(fichier, index=False)
        else:
            raise ValueError(f"Format de fichier non supporté pour l'export : {extension}. Formats supportés : .csv, .txt, .xlsx.")
        logging.info(f"{len(epargnes)} produits d'épargne exportés avec succès vers '{fichier}'.")
    except Exception as e:
        logging.error(f"Échec de l'exportation des produits d'épargne vers '{fichier}' : {e}")
        raise