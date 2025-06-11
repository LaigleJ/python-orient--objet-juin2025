import math

class Epargne:
    def __init__(self, nom: str, taux_interet_annuel: float, frais_gestion_annuels: float, inflation_annuelle: float,
                 fiscalite: float, duree_min: int, versement_max: float = None):
        self.nom = nom
        self.taux_interet_annuel = taux_interet_annuel
        self.frais_gestion_annuels = frais_gestion_annuels
        self.inflation_annuelle = inflation_annuelle
        self.fiscalite = fiscalite
        self.duree_min = duree_min
        self.versement_max = versement_max

    def calcul_interets_composes(self, montant_initial: float, versement_mensuel: float, duree_mois: int) -> float:
        """
        Calcule le montant final d'une épargne avec intérêts composés,
        en tenant compte des frais et de l'inflation.

        Args:
            montant_initial (float): Le capital de départ.
            versement_mensuel (float): Le montant versé chaque mois.
            duree_mois (int): La durée de l'épargne en mois.

        Returns:
            float: Le montant final après intérêts et frais (avant fiscalité).
        """
        taux_mensuel_net = (self.taux_interet_annuel - self.frais_gestion_annuels) / 12
        montant_courant = montant_initial

        for _ in range(duree_mois):
            montant_courant *= (1 + taux_mensuel_net)
            montant_courant += versement_mensuel

        return montant_courant

    def appliquer_fiscalite(self, montant_brut: float, montant_verse: float) -> float:
        """Applique la fiscalité sur les gains (montant_brut - montant_verse)."""
        gains = montant_brut - montant_verse
        if gains > 0:
            return montant_brut - (gains * self.fiscalite)
        return montant_brut

    def ajuster_inflation(self, montant_nominal: float, duree_mois: int) -> float:
        """Ajuste un montant pour l'inflation sur une durée donnée."""
        taux_inflation_mensuel = self.inflation_annuelle / 12
        return montant_nominal / ((1 + taux_inflation_mensuel) ** duree_mois)