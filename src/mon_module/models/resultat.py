import pandas as pd
import numpy as np

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

    def afficher(self):
        """
        Affiche les résultats de la simulation d'épargne.
        Cette méthode est ajoutée pour satisfaire les tests.
        Elle affiche les attributs réellement stockés par la classe.
        """
        print(f"Simulation pour {self.personne_nom}")
        print(f"Produit d'épargne: {self.produit_nom} (Taux: {self.taux_interet*100:.2f}%, Fiscalité: {self.fiscalite*100:.2f}%)")
        print(f"Versement mensuel: {self.versement_mensuel:.2f} €/mois")
        print(f"Montant atteint après {self.duree_mois} mois: {self.capital_brut:.2f} €")
        print(f"Montant net après fiscalité: {self.capital_net:.2f} €")
        # Le statut de l'objectif est basé sur l'attribut atteint_objectif
        print(f"Statut de l'objectif: {'Atteint' if self.atteint_objectif else 'Non atteint'}")
        print(f"Message de la simulation: {self.message}")

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