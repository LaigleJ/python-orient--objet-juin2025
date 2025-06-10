# src/mon_module/models/personne.py

import numpy as np # <-- NOUVELLE IMPORTATION

class Personne:
    def __init__(self, nom: str, age: int, revenu_annuel: float, loyer: float,
                 depenses_mensuelles: float, objectif: float = 0.0, duree_epargne: int = 0, # <-- Ajout de valeurs par défaut pour objectif et duree_epargne
                 versement_mensuel_utilisateur: float = np.nan): # <-- Changement du type par défaut à np.nan
        """
        Initialise une nouvelle instance de la classe Personne.

        Args:
            nom (str): Nom de la personne.
            age (int): Âge de la personne.
            revenu_annuel (float): Revenu annuel de la personne.
            loyer (float): Loyer mensuel de la personne.
            depenses_mensuelles (float): Dépenses mensuelles (hors loyer).
            objectif (float, optional): Objectif financier à atteindre. Défaut à 0.0.
            duree_epargne (int, optional): Durée d'épargne souhaitée en mois. Défaut à 0.
            versement_mensuel_utilisateur (float, optional): Versement mensuel défini par l'utilisateur.
                                                              Utilise np.nan si non spécifié ou vide.
        """
        self.nom = nom
        self.age = age
        self.revenu_annuel = revenu_annuel
        self.loyer = loyer
        self.depenses_mensuelles = depenses_mensuelles
        self.objectif = objectif
        self.duree_epargne = duree_epargne
        self.versement_mensuel_utilisateur = versement_mensuel_utilisateur
        self.capacite_epargne_mensuelle = self._calcul_capacite_epargne()

    def _calcul_capacite_epargne(self) -> float:
        """
        Calcule la capacité d'épargne mensuelle de la personne.
        (Revenu annuel / 12) - loyer - dépenses mensuelles.
        Gère les cas où versement_mensuel_utilisateur est np.nan.
        """
        if not np.isnan(self.versement_mensuel_utilisateur): # Si versement utilisateur N'EST PAS nan
            return self.versement_mensuel_utilisateur
        else:
            # Assurez-vous que les revenus/dépenses sont des nombres avant le calcul
            # On considère 0 si une des valeurs est NaN pour le calcul de la capacité naturelle
            revenu_mensuel = (self.revenu_annuel if not np.isnan(self.revenu_annuel) else 0.0) / 12
            loyer = self.loyer if not np.isnan(self.loyer) else 0.0
            depenses_mensuelles = self.depenses_mensuelles if not np.isnan(self.depenses_mensuelles) else 0.0
            return revenu_mensuel - loyer - depenses_mensuelles

    def __str__(self):
        """
        Fournit une représentation textuelle conviviale de l'objet Personne.
        """
        capacite_str = f"{self.capacite_epargne_mensuelle:.2f} €/mois"
        if not np.isnan(self.versement_mensuel_utilisateur):
            capacite_str = f"{self.versement_mensuel_utilisateur:.2f} €/mois (défini par l'utilisateur)"
        return (f"Personne: {self.nom} (âge: {self.age} ans)\n"
                f"  Revenu annuel: {self.revenu_annuel:.2f} €, Loyer: {self.loyer:.2f} €, Dépenses: {self.depenses_mensuelles:.2f} €\n"
                f"  Capacité d'épargne mensuelle estimée: {capacite_str}\n"
                f"  Objectif financier: {self.objectif:.2f} € sur {self.duree_epargne} mois")