
import logging
import numpy as np

from src.mon_module.models.personne import Personne
from src.mon_module.models.epargne import Epargne
from src.mon_module.models.resultat import ResultatEpargne # NOUVELLE IMPORTATION
from src.mon_module.utils import calcul_interets_composes # Votre fonction de calcul

def suggestion_epargne(personne: Personne, epargnes: list[Epargne]) -> list[ResultatEpargne]:
    """
    Génère des scénarios de simulation d'épargne pour une personne donnée avec divers produits.

    Args:
        personne (Personne): L'instance de la personne pour la simulation.
        epargnes (list[Epargne]): La liste des produits d'épargne disponibles.

    Returns:
        list[ResultatEpargne]: Une liste des résultats de simulation pour les scénarios valides.
    """
    logging.info(f"Début de la simulation d'épargne pour {personne.nom}.")
    resultats_simulations = []

    # Vérifier que la capacité d'épargne est valide
    if np.isnan(personne.capacite_epargne_mensuelle) or personne.capacite_epargne_mensuelle <= 0:
        logging.warning(f"La capacité d'épargne de {personne.nom} est invalide ou nulle ({personne.capacite_epargne_mensuelle:.2f} €). Pas de simulation possible.")
        return []

    capacite_epargne_mensuelle = personne.capacite_epargne_mensuelle

    # Définir les scénarios d'effort en pourcentage
    # Inclure le versement_mensuel_utilisateur si valide
    efforts_pourcentage = [0.25, 0.50, 0.75, 1.00]
    scenarios_versement_mensuel = []

    # Ajouter le versement_mensuel_utilisateur si applicable et valide
    if not np.isnan(personne.versement_mensuel_utilisateur) and personne.versement_mensuel_utilisateur > 0:
        scenarios_versement_mensuel.append(personne.versement_mensuel_utilisateur)

    # Calculer les versements pour les pourcentages de capacité
    for effort in efforts_pourcentage:
        scenarios_versement_mensuel.append(capacite_epargne_mensuelle * effort)

    # Supprimer les doublons et s'assurer que les versements sont positifs
    scenarios_versement_mensuel = sorted(list(set([v for v in scenarios_versement_mensuel if v > 0])))

    # Durée de l'épargne en années pour la fonction de calcul des intérêts composés
    duree_epargne_annees = max(1, round(personne.duree_epargne / 12)) # Au moins 1 an si durée en mois est 0 ou faible

    for epargne_produit in epargnes:
        logging.info(f"  Analyse du produit '{epargne_produit.nom}'.")

        # Ignorer les produits inaccessibles selon la durée d'investissement
        if personne.duree_epargne < epargne_produit.duree_min:
            logging.info(f"    Produit '{epargne_produit.nom}' ignoré : durée minimale ({epargne_produit.duree_min} mois) non atteinte par la durée d'épargne de {personne.duree_epargne} mois.")
            continue

        for versement_mensuel in scenarios_versement_mensuel:
            # Calculer le versement annuel
            versement_annuel_total = versement_mensuel * 12

            message_scenario = ""
            # Gérer le plafond de versement
            if not np.isnan(epargne_produit.versement_max) and versement_annuel_total > epargne_produit.versement_max:
                # Si le versement annuel dépasse le plafond, on le ramène au plafond
                versement_annuel_effectif = epargne_produit.versement_max
                # Et donc le versement mensuel effectif est le plafond annuel / 12
                versement_mensuel_effectif = versement_annuel_effectif / 12
                message_scenario = f"Versement ajusté au plafond ({epargne_produit.versement_max:.2f} €/an)."
                logging.info(f"    Scénario: {versement_mensuel:.2f} €/mois. Versement annuel {versement_annuel_total:.2f} € dépasse le plafond de '{epargne_produit.nom}'. Ajusté à {versement_mensuel_effectif:.2f} €/mois.")
            else:
                versement_annuel_effectif = versement_annuel_total
                versement_mensuel_effectif = versement_mensuel
                logging.info(f"    Scénario: {versement_mensuel:.2f} €/mois. Versement annuel effectif: {versement_annuel_effectif:.2f} €.")

            # S'assurer que le versement effectif est positif
            if versement_annuel_effectif <= 0:
                logging.info(f"    Versement effectif de {versement_annuel_effectif:.2f} €/an est nul ou négatif. Scénario ignoré.")
                continue

            # Calcul du capital brut avec intérêts
            try:
                capital_brut = calcul_interets_composes(
                    versement_annuel=versement_annuel_effectif,
                    taux_annuel=epargne_produit.taux_interet,
                    duree_annees=duree_epargne_annees
                )
            except ValueError as e:
                logging.error(f"Erreur de calcul des intérêts pour {epargne_produit.nom} avec {versement_annuel_effectif}€/an sur {duree_epargne_annees} ans: {e}")
                continue # Passe au scénario suivant

            # Application de la fiscalité (si le capital brut est positif)
            gains_bruts = capital_brut - (versement_annuel_effectif * duree_epargne_annees)
            if gains_bruts > 0:
                imposition = gains_bruts * epargne_produit.fiscalite
                capital_net = capital_brut - imposition
            else:
                capital_net = capital_brut # Pas d'imposition si pas de gains

            # Vérifier si l'objectif est atteint
            atteint_objectif = capital_net >= personne.objectif

            # Ajouter le résultat à la liste
            resultats_simulations.append(
                ResultatEpargne(
                    personne_nom=personne.nom,
                    produit_nom=epargne_produit.nom,
                    taux_interet=epargne_produit.taux_interet,
                    fiscalite=epargne_produit.fiscalite,
                    versement_mensuel=versement_mensuel_effectif,
                    duree_mois=personne.duree_epargne, # On garde la durée en mois de la personne
                    capital_brut=capital_brut,
                    capital_net=capital_net,
                    atteint_objectif=atteint_objectif,
                    message=message_scenario
                )
            )
    logging.info(f"Simulation d'épargne terminée pour {personne.nom}. Total de {len(resultats_simulations)} scénarios générés.")
    return resultats_simulations