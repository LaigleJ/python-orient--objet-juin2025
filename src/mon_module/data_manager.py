# src/mon_module/data_manager.py

import pandas as pd
import os # Pour gérer les chemins de fichiers et les extensions

from src.mon_module.models.personne import Personne
from src.mon_module.models.epargne import Epargne
from src.mon_module.data_cleaning import nettoyer_dataframe, nettoyer_nombre, nettoyer_taux


def importer_donnees(chemin_fichier: str) -> pd.DataFrame:
    """
    Importe les données depuis un fichier CSV, TXT ou XLSX et les retourne sous forme de DataFrame Pandas.
    Applique un nettoyage de base en fonction du type de données identifié par le nom de fichier.

    Args:
        chemin_fichier (str): Chemin complet vers le fichier de données (CSV, TXT, XLSX).

    Returns:
        pd.DataFrame: Un DataFrame Pandas contenant les données nettoyées.

    Raises:
        FileNotFoundError: Si le fichier n'est pas trouvé.
        ValueError: Si le format de fichier n'est pas supporté ou si une erreur de nettoyage survient.
    """
    # Déterminer l'extension du fichier pour choisir la méthode de lecture
    extension = os.path.splitext(chemin_fichier)[1].lower()
    df = None

    try:
        if extension == '.csv':
            df = pd.read_csv(chemin_fichier)
        elif extension == '.txt':
            # Supposons que les fichiers TXT utilisent une tabulation comme séparateur
            df = pd.read_csv(chemin_fichier, sep='\t')
        elif extension == '.xlsx':
            df = pd.read_excel(chemin_fichier)
        else:
            raise ValueError(f"Format de fichier non supporté : {extension}. Les formats supportés sont .csv, .txt, .xlsx.")

        # Appliquer le nettoyage des données
        df = nettoyer_dataframe(df.copy()) # Utiliser .copy() pour éviter SettingWithCopyWarning

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier '{chemin_fichier}' n'a pas été trouvé.")
    except Exception as e: # Capture d'autres erreurs potentielles lors de la lecture ou du nettoyage
        raise ValueError(f"Erreur lors de l'importation ou du nettoyage du fichier '{chemin_fichier}' : {e}")

def creer_objets_personne_depuis_df(df: pd.DataFrame) -> list[Personne]:
    """
    Crée une liste d'objets Personne à partir d'un DataFrame Pandas nettoyé.

    Args:
        df (pd.DataFrame): DataFrame contenant les données des personnes, nettoyées.

    Returns:
        list[Personne]: Une liste d'objets Personne.
    """
    personnes = []
    for index, row in df.iterrows():
        try:
            personne = Personne(
                nom=row['nom'],
                age=row['age'],
                revenu_annuel=row['revenu_annuel'],
                loyer=row['loyer'],
                depenses_mensuelles=row['depenses_mensuelles'],
                # objectif et duree_epargne ne sont pas dans le CSV Personne, à ajouter si nécessaire
                # Pour l'instant, on met des valeurs par défaut ou on gère leur absence
                objectif=0.0, # Valeur par défaut
                duree_epargne=0, # Valeur par défaut
                versement_mensuel_utilisateur=row.get('versement_mensuel_utilisateur') # .get() pour gérer l'absence
            )
            personnes.append(personne)
        except KeyError as e:
            raise ValueError(f"Colonne manquante pour la création d'objet Personne : {e}. Vérifiez le CSV.")
        except Exception as e:
            raise ValueError(f"Erreur lors de la création d'un objet Personne à la ligne {index+2} : {e}")
    return personnes

def creer_objets_epargne_depuis_df(df: pd.DataFrame) -> list[Epargne]:
    """
    Crée une liste d'objets Epargne à partir d'un DataFrame Pandas nettoyé.

    Args:
        df (pd.DataFrame): DataFrame contenant les données d'épargne, nettoyées.

    Returns:
        list[Epargne]: Une liste d'objets Epargne.
    """
    epargnes = []
    for index, row in df.iterrows():
        try:
            epargne = Epargne(
                nom=row['nom'],
                taux_interet=row['taux_interet'],
                fiscalite=row['fiscalite'],
                duree_min=row['duree_min'],
                versement_max=row.get('versement_max') # .get() pour gérer l'absence
            )
            epargnes.append(epargne)
        except KeyError as e:
            raise ValueError(f"Colonne manquante pour la création d'objet Epargne : {e}. Vérifiez le CSV.")
        except Exception as e:
            raise ValueError(f"Erreur lors de la création d'un objet Epargne à la ligne {index+2} : {e}")
    return epargnes