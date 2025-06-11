import pytest
from src.mon_module.models.resultat import ResultatEpargne as Resultat

def test_resultat_initialisation():
    """
    Teste l'initialisation d'un objet Resultat.
    """
    resultat = Resultat(
        personne_nom="Alice",
        produit_nom="Livret A",
        taux_interet=0.03,
        fiscalite=0.0,
        versement_mensuel=150.75,
        duree_mois=67,
        capital_brut=10005.20,
        capital_net=10000.0,
        atteint_objectif=True,
        message="Simulation réussie, objectif atteint."
    )
    assert resultat.personne_nom == "Alice"
    assert resultat.produit_nom == "Livret A"
    assert resultat.taux_interet == 0.03
    assert resultat.fiscalite == 0.0
    assert resultat.versement_mensuel == pytest.approx(150.75)
    assert resultat.duree_mois == 67
    assert resultat.capital_brut == pytest.approx(10005.20)
    assert resultat.capital_net == pytest.approx(10000.0)
    assert resultat.atteint_objectif is True
    assert resultat.message == "Simulation réussie, objectif atteint."


def test_resultat_affichage(capsys):
    """
    Teste la méthode d'affichage du Resultat.
    Vérifie un scénario de simulation.
    """
    resultat = Resultat(
        personne_nom="Bob",
        produit_nom="PEL",
        taux_interet=0.01,
        fiscalite=0.172,
        versement_mensuel=100.0,
        duree_mois=50,
        capital_brut=5020.50,
        capital_net=4156.95,
        atteint_objectif=False,
        message="Simulation terminée, objectif non atteint."
    )
    resultat.afficher()
    captured = capsys.readouterr()

    assert "Simulation pour Bob" in captured.out
    assert "Produit d'épargne: PEL" in captured.out
    assert "Taux: 1.00%" in captured.out
    assert "Fiscalité: 17.20%" in captured.out
    assert "Versement mensuel: 100.00 €/mois" in captured.out
    assert "Montant atteint après 50 mois: 5020.50 €" in captured.out
    assert "Montant net après fiscalité: 4156.95 €" in captured.out
    assert "Statut de l'objectif: Non atteint" in captured.out
    assert "Message de la simulation: Simulation terminée, objectif non atteint." in captured.out


def test_resultat_affichage_capacite_suffisante(capsys):
    """
    Teste l'affichage lorsque l'objectif est atteint.
    """
    resultat = Resultat(
        personne_nom="Charlie",
        produit_nom="Assurance Vie",
        taux_interet=0.04,
        fiscalite=0.30,
        versement_mensuel=120.0,
        duree_mois=60,
        capital_brut=7050.0,
        capital_net=4935.0,
        atteint_objectif=True,
        message="Objectif atteint avec succès."
    )
    resultat.afficher()
    captured = capsys.readouterr()

    assert "Simulation pour Charlie" in captured.out
    assert "Produit d'épargne: Assurance Vie" in captured.out
    assert "Taux: 4.00%" in captured.out
    assert "Fiscalité: 30.00%" in captured.out
    assert "Versement mensuel: 120.00 €/mois" in captured.out
    assert "Montant atteint après 60 mois: 7050.00 €" in captured.out
    assert "Montant net après fiscalité: 4935.00 €" in captured.out
    assert "Statut de l'objectif: Atteint" in captured.out
    assert "Message de la simulation: Objectif atteint avec succès." in captured.out