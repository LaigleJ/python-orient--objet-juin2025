
import pandas as pd
import numpy as np # Pour gérer np.nan si besoin, bien que moins probable ici

class ResultatEpargne:
    """
    Modélise un résultat de simulation d'épargne pour un scénario donné.
    """
    def __init__(self,
                 personne_nom: str,
                 produit_nom: str,
                 taux_interet: float,
                 fiscalite: float,
                 versement_mensuel: float,
                 duree_mois: int,
                 capital_brut: float,
                 capital_net: float,
                 atteint_objectif: bool = False,
                 message: str = ""):
        self.personne_nom = personne_nom
        self.produit_nom = produit_nom
        self.taux_interet = taux_interet
        self.fiscalite = fiscalite
        self.versement_mensuel = versement_mensuel
        self.duree_mois = duree_mois
        self.capital_brut = capital_brut
        self.capital_net = capital_net
        self.atteint_objectif = atteint_objectif
        self.message = message

    def __str__(self):
        """Fournit une représentation textuelle conviviale du résultat."""
        return (f"--- Résultat de Simulation ---\n"
                f"  Personne: {self.personne_nom}\n"
                f"  Produit: {self.produit_nom}\n"
                f"  Versement mensuel: {self.versement_mensuel:.2f} €\n"
                f"  Durée: {self.duree_mois} mois\n"
                f"  Capital brut: {self.capital_brut:.2f} €\n"
                f"  Capital net (après fiscalité): {self.capital_net:.2f} €\n"
                f"  Objectif atteint: {'Oui' if self.atteint_objectif else 'Non'}\n"
                f"  Message: {self.message}")

    def __repr__(self):
        """Fournit une représentation officielle de l'objet pour le débogage."""
        return (f"ResultatEpargne(personne_nom={repr(self.personne_nom)}, "
                f"produit_nom={repr(self.produit_nom)}, "
                f"taux_interet={self.taux_interet}, fiscalite={self.fiscalite}, "
                f"versement_mensuel={self.versement_mensuel}, duree_mois={self.duree_mois}, "
                f"capital_brut={self.capital_brut}, capital_net={self.capital_net}, "
                f"atteint_objectif={self.atteint_objectif}, message={repr(self.message)})")

    def to_dataframe(self) -> pd.DataFrame:
        """Convertit le résultat en un DataFrame Pandas."""
        data = {
            'Personne': [self.personne_nom],
            'Produit': [self.produit_nom],
            'Taux Interet': [self.taux_interet],
            'Fiscalite': [self.fiscalite],
            'Versement Mensuel': [self.versement_mensuel],
            'Duree Mois': [self.duree_mois],
            'Capital Brut': [self.capital_brut],
            'Capital Net': [self.capital_net],
            'Objectif Atteint': [self.atteint_objectif],
            'Message': [self.message]
        }
        return pd.DataFrame(data)