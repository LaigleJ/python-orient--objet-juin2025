
class Epargne:
    def __init__(
        self,
        nom: str,
        taux_interet: float,
        fiscalite: float,
        duree_min: int,
        versement_max: float = None
    ):
        self.nom = nom
        self.taux_interet = taux_interet  # ex : 0.03 pour 3 %
        self.fiscalite = fiscalite        # ex : 0.17 pour 17 %
        self.duree_min = duree_min        # en mois
        self.versement_max = versement_max  # en € ou None = illimité

    def __str__(self) -> str:
        taux_net = self.taux_interet * (1 - self.fiscalite)
        return (f"{self.nom} | Taux net: {taux_net*100:.2f}% | "
                f"Durée min: {self.duree_min} mois | "
                f"Plafond: {self.versement_max if self.versement_max else 'Aucun'} €")

    def __repr__(self) -> str:
        return f"Epargne({self.nom}, {self.taux_interet}, {self.fiscalite}, {self.duree_min}, {self.versement_max})"
