import pytest
from src.mon_module.models.epargne import Epargne

def test_epargne_initialisation():
    """
    Teste l'initialisation d'un objet Epargne avec des valeurs valides.
    """
    epargne = Epargne(
        nom="Livret A",
        fiscalite=0.0,
        duree_min=0,
        taux_interet_annuel=0.03,
        frais_gestion_annuels=0.005,
        inflation_annuelle=0.02
    )
    assert epargne.taux_interet_annuel == 0.03
    assert epargne.frais_gestion_annuels == 0.005
    assert epargne.inflation_annuelle == 0.02

def test_epargne_calcul_interets_composes():
    """
    Teste la méthode de calcul des intérêts composés.
    """
    epargne = Epargne(
        nom="PEL",
        fiscalite=0.172,
        duree_min=12,
        taux_interet_annuel=0.05,
        frais_gestion_annuels=0.01,
        inflation_annuelle=0.02
    )

    montant_final_attendu = epargne.calcul_interets_composes(
        montant_initial=1000,
        versement_mensuel=100,
        duree_mois=12
    )

    assert montant_final_attendu > 1000 + (100 * 12) 
    assert montant_final_attendu < 1000 + (100 * 12) * 1.1
   
    assert epargne.calcul_interets_composes(0, 0, 12) == 0
    assert epargne.calcul_interets_composes(100, 0, 0) == 100 