import numpy as np 

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
        Gère les cas où versement_mensuel_utilisateur est None.
        """
        # --- MODIFICATION ICI ---
        if self.versement_mensuel_utilisateur is not None: # Vérifier si ce n'est PAS None
            return self.versement_mensuel_utilisateur

        revenu_mensuel = self.revenu_annuel / 12
        depenses_totales_mensuelles = self.loyer + self.depenses_mensuelles
        capacite = revenu_mensuel - depenses_totales_mensuelles
        return max(0.0, capacite) # Assurer que la capacité n'est pas négative

    def __str__(self):
        """
        Fournit une représentation textuelle conviviale de l'objet Personne.
        """
        capacite_str = f"{self.capacite_epargne_mensuelle:.2f} €/mois"
        if self.versement_mensuel_utilisateur is not None and not np.isnan(self.versement_mensuel_utilisateur):
            capacite_str = f"{self.versement_mensuel_utilisateur:.2f} €/mois (défini par l'utilisateur)"
        return (f"Personne: {self.nom} (âge: {self.age} ans)\n"
                f"  Revenu annuel: {self.revenu_annuel:.2f} €, Loyer: {self.loyer:.2f} €, Dépenses: {self.depenses_mensuelles:.2f} €\n"
                f"  Capacité d'épargne mensuelle estimée: {capacite_str}\n"
                f"  Objectif financier: {self.objectif:.2f} € sur {self.duree_epargne} mois")

    def afficher(self):
            """
            Affiche les informations détaillées de la personne sur la console.
            """
            print(self.__str__())