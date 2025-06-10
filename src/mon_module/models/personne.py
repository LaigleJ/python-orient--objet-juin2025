
class Personne:
    def __init__(
        self,
        nom: str,
        age: int,
        revenu_annuel: float,
        loyer: float,
        depenses_mensuelles: float,
        objectif: float,
        duree_epargne: int,
        versement_mensuel_utilisateur: float = None
    ):
        self.nom = nom
        self.age = age
        self.revenu_annuel = revenu_annuel
        self.loyer = loyer
        self.depenses_mensuelles = depenses_mensuelles
        self.objectif = objectif
        self.duree_epargne = duree_epargne
        self.versement_mensuel_utilisateur = versement_mensuel_utilisateur

        self._capacite_epargne_mensuelle = self._calcul_capacite_epargne()

    def _calcul_capacite_epargne(self) -> float:
        """
        Capacité d'épargne mensuelle = (revenu annuel / 12) - loyer - dépenses
        """
        capacite = (self.revenu_annuel / 12) - self.loyer - self.depenses_mensuelles
        return max(0.0, capacite)

    @property
    def capacite_epargne(self) -> float:
        """Expose la capacité d’épargne calculée (accès en lecture seule)"""
        return self._capacite_epargne_mensuelle

    def __str__(self) -> str:
        return (f"{self.nom}, {self.age} ans | Objectif: {self.objectif}€ sur {self.duree_epargne} mois | "
                f"Capacité d’épargne : {self.capacite_epargne:.2f} €/mois")
