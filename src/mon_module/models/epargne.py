# src/mon_module/models/epargne.py

import numpy as np # <-- NOUVELLE IMPORTATION

class Epargne:
    def __init__(self, nom: str, taux_interet: float, fiscalite: float,
                 duree_min: int, versement_max: float = np.nan): # <-- Changement du type par défaut à np.nan
        """
        Initialise une nouvelle instance de la classe Epargne.

        Args:
            nom (str): Nom du produit d'épargne (ex: "Livret A", "PEL").
            taux_interet (float): Taux d'intérêt annuel du produit (ex: 0.03 pour 3%).
            fiscalite (float): Taux de fiscalité applicable aux gains (ex: 0.30 pour 30%).
            duree_min (int): Durée minimale de détention en mois.
            versement_max (float, optional): Plafond de versement maximal du produit. Utilise np.nan si pas de plafond.
        """
        self.nom = nom
        self.taux_interet = taux_interet
        self.fiscalite = fiscalite
        self.duree_min = duree_min
        self.versement_max = versement_max

    def __str__(self):
        """
        Fournit une représentation textuelle conviviale de l'objet Epargne.
        """
        versement_max_str = f"{self.versement_max:.2f} €" if not np.isnan(self.versement_max) else "Aucun"
        return (f"Produit d'épargne: {self.nom}\n"
                f"  Taux d'intérêt: {self.taux_interet * 100:.2f} %\n"
                f"  Fiscalité: {self.fiscalite * 100:.2f} %\n"
                f"  Durée minimale: {self.duree_min} mois\n"
                f"  Plafond de versement: {versement_max_str}")

    def __repr__(self):
        """
        Fournit une représentation officielle de l'objet Epargne, utile pour le débogage.
        """
        return (f"Epargne(nom={repr(self.nom)}, taux_interet={self.taux_interet}, "
                f"fiscalite={self.fiscalite}, duree_min={self.duree_min}, "
                f"versement_max={self.versement_max})")