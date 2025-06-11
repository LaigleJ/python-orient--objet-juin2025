import pandas as pd
import numpy as np # <-- NOUVELLE IMPORTATION POUR np.nan

def nettoyer_taux(taux):
    """Convertit un taux en float, gère les pourcentages et les erreurs."""
    # Utilise np.nan pour les valeurs non trouvées ou non convertibles, pour cohérence avec pandas
    if pd.isna(taux) or taux is None or str(taux).lower().strip() == 'none' or str(taux).strip() == '': # Ajout de gestion chaîne vide
        return np.nan # Retourne np.nan pour indiquer une valeur manquante/non définie
    try:
        taux_str = str(taux).replace(',', '.').strip() # Remplace virgule par point et supprime espaces
        if '%' in taux_str:
            return float(taux_str.strip('%')) / 100
        else:
            return float(taux_str)
    except ValueError:
        raise ValueError(f"Taux invalide : '{taux}'")

def nettoyer_nombre(nombre, type_cible=float): # <-- Changement du type_cible par défaut à float
    """Convertit une valeur en int ou float, gère les valeurs manquantes et les erreurs."""
    if pd.isna(nombre) or nombre is None or str(nombre).lower().strip() == 'none' or str(nombre).strip() == '': # Ajout de gestion chaîne vide
        return np.nan # Retourne np.nan
    try:
        # Convertir en float d'abord pour gérer les décimales, puis en int si demandé
        val = float(str(nombre).replace(',', '.').strip())
        return type_cible(val)
    except ValueError:
        raise ValueError(f"Nombre invalide : '{nombre}'")

def nettoyer_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie un DataFrame pandas pour l'import des données Personne ou Epargne."""
    # Crée une copie du DataFrame pour éviter les SettingWithCopyWarning
    df_cleaned = df.copy()

    # Définir les colonnes par type de nettoyage attendu
    cols_pour_taux = ['taux_interet', 'fiscalite']
    cols_pour_float = ['revenu_annuel', 'loyer', 'depenses_mensuelles', 'versement_max', 'versement_mensuel_utilisateur']
    cols_pour_int = ['age', 'duree_min', 'duree_epargne'] # Ajout de duree_epargne

    for col in df_cleaned.columns:
        if col in cols_pour_taux:
            df_cleaned[col] = df_cleaned[col].apply(nettoyer_taux)
        elif col in cols_pour_float:
            # S'assurer que le nettoyage de nombre est appelé avec float
            df_cleaned[col] = df_cleaned[col].apply(lambda x: nettoyer_nombre(x, float))
        elif col in cols_pour_int:
            # S'assurer que le nettoyage de nombre est appelé avec int
            df_cleaned[col] = df_cleaned[col].apply(lambda x: nettoyer_nombre(x, int))
    return df_cleaned