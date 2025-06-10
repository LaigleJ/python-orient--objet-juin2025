class Personne:
    def __init__(self, nom: str, age: int, revenu_annuel: float, loyer: float,
                 depenses_mensuelles: float, objectif: float, duree_epargne: int,
                 versement_mensuel_utilisateur: float = None):
        """
        Initialise une nouvelle instance de la classe Personne.

        Args:
            nom (str): Nom de la personne.
            age (int): Âge de la personne.
            revenu_annuel (float): Revenu annuel de la personne.
            loyer (float): Loyer mensuel de la personne.
            depenses_mensuelles (float): Dépenses mensuelles (hors loyer).
            objectif (float): Objectif financier à atteindre.
            duree_epargne (int): Durée d'épargne souhaitée en mois.
            versement_mensuel_utilisateur (float, optional): Versement mensuel défini par l'utilisateur.
                                                              Si None, la capacité d'épargne est calculée.
        """
        self.nom = nom
        self.age = age
        self.revenu_annuel = revenu_annuel
        self.loyer = loyer
        self.depenses_mensuelles = depenses_mensuelles
        self.objectif = objectif
        self.duree_epargne = duree_epargne
        self.versement_mensuel_utilisateur = versement_mensuel_utilisateur
        # La capacité d'épargne est calculée et stockée dès l'initialisation
        self.capacite_epargne_mensuelle = self._calcul_capacite_epargne()

    def _calcul_capacite_epargne(self) -> float:
        """
        Calcule la capacité d'épargne mensuelle de la personne.
        (Revenu annuel / 12) - loyer - dépenses mensuelles.
        """
        if self.versement_mensuel_utilisateur is not None:
            # Si un versement utilisateur est spécifié, on l'utilise pour la capacité
            return self.versement_mensuel_utilisateur
        else:
            # Sinon, on calcule la capacité basée sur revenu - dépenses
            revenu_mensuel = self.revenu_annuel / 12
            return revenu_mensuel - self.loyer - self.depenses_mensuelles

    def __str__(self):
        """
        Fournit une représentation textuelle conviviale de l'objet Personne.
        """
        capacite_str = f"{self.capacite_epargne_mensuelle:.2f} €/mois"
        if self.versement_mensuel_utilisateur is not None:
            capacite_str = f"{self.versement_mensuel_utilisateur:.2f} €/mois (défini par l'utilisateur)"
        return (f"Personne: {self.nom} (âge: {self.age} ans)\n"
                f"  Revenu annuel: {self.revenu_annuel:.2f} €, Loyer: {self.loyer:.2f} €, Dépenses: {self.depenses_mensuelles:.2f} €\n"
                f"  Capacité d'épargne mensuelle estimée: {capacite_str}\n"
                f"  Objectif financier: {self.objectif:.2f} € sur {self.duree_epargne} mois")