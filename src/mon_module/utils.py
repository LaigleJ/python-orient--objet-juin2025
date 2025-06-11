import datetime
from functools import wraps # Important pour préserver les métadonnées de la fonction décorée

def calcul_interets_composes(versement_annuel: float, taux_annuel: float, duree_annees: int) -> float:
    """
    Calcule le montant final d'un placement avec intérêts composés.

    Args:
        versement_annuel (float): Le montant total versé par an.
        taux_annuel (float): Le taux d'intérêt annuel (ex: 0.03 pour 3%).
        duree_annees (int): La durée du placement en années.

    Returns:
        float: Le montant total accumulé après la durée spécifiée.
    """
    if duree_annees < 0:
        raise ValueError("La durée en années ne peut pas être négative.")
    if taux_annuel < 0:
        raise ValueError("Le taux d'intérêt annuel ne peut pas être négatif.")
    if versement_annuel < 0:
        raise ValueError("Le versement annuel ne peut pas être négatif.")

    montant_final = 0.0
    for annee in range(duree_annees):
        # Le montant_final est le capital de l'année précédente + le versement de cette année
        montant_final += versement_annuel
        # On applique les intérêts sur le nouveau capital
        montant_final *= (1 + taux_annuel)
    return montant_final

def log_suggestion_process(func):
    """
    Décorateur qui affiche un message clair avant l'exécution
    de la fonction de suggestion d'épargne.
    """
    @wraps(func) # Permet de préserver le nom, le module, et le docstring de 'func'
    def wrapper(nombre_placements: int, nom_personne: str, *args, **kwargs):
        """
        La fonction wrapper qui ajoute la logique d'affichage.
        """
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time} - Nous allons faire une comparaison de {nombre_placements} placements selon la situation de {nom_personne}.")
        return func(nombre_placements, nom_personne, *args, **kwargs) # Exécute la fonction originale

    return wrapper