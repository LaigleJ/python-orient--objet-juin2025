import pytest
from src.mon_module.models.personne import Personne

def test_personne_initialisation():
    """
    Teste l'initialisation d'un objet Personne avec des valeurs valides.
    """
    personne = Personne(
        nom="Jean",
        age=30,
        revenu_annuel=35000,
        loyer=700,
        depenses_mensuelles=400,
        objectif=15000,
        duree_epargne=60,
        versement_mensuel_utilisateur=None
    )
    assert personne.nom == "Jean"
    assert personne.age == 30
    assert personne.revenu_annuel == 35000
    assert personne.loyer == 700
    assert personne.depenses_mensuelles == 400
    assert personne.objectif == 15000
    assert personne.duree_epargne == 60
    assert personne.versement_mensuel_utilisateur is None

def test_personne_capacite_epargne_mensuelle_sans_versement_utilisateur():
    """
    Teste le calcul de la capacité d'épargne mensuelle sans versement utilisateur.
    """
    personne = Personne(
        nom="Jean",
        age=30,
        revenu_annuel=35000,
        loyer=700,
        depenses_mensuelles=400,
        objectif=15000,
        duree_epargne=60,
        versement_mensuel_utilisateur=None
    )
    
    assert personne.capacite_epargne_mensuelle == pytest.approx((35000 / 12) - (700 + 400))

def test_personne_capacite_epargne_mensuelle_avec_versement_utilisateur():
    """
    Teste le calcul de la capacité d'épargne mensuelle avec versement utilisateur.
    Le versement utilisateur devrait prévaloir.
    """
    personne = Personne(
        nom="Marie",
        age=45,
        revenu_annuel=50000,
        loyer=900,
        depenses_mensuelles=600,
        objectif=25000,
        duree_epargne=120,
        versement_mensuel_utilisateur=1000
    )

    assert personne.capacite_epargne_mensuelle == 1000

def test_personne_capacite_epargne_mensuelle_revenu_nul():
    """
    Teste la capacité d'épargne lorsque le revenu annuel est nul.
    """
    personne = Personne(
        nom="Sans Revenu",
        age=20,
        revenu_annuel=0,
        loyer=0,
        depenses_mensuelles=0,
        objectif=1000,
        duree_epargne=12,
        versement_mensuel_utilisateur=None
    )
    assert personne.capacite_epargne_mensuelle == 0

def test_personne_capacite_epargne_mensuelle_negatif():
    """
    Teste la capacité d'épargne lorsque les dépenses sont supérieures au revenu.
    Doit retourner 0 car la capacité ne peut pas être négative.
    """
    personne = Personne(
        nom="Dépenses Excessives",
        age=40,
        revenu_annuel=12000, # 1000 par mois
        loyer=600,
        depenses_mensuelles=500,
        objectif=10000,
        duree_epargne=60,
        versement_mensuel_utilisateur=None
    )
    
    assert personne.capacite_epargne_mensuelle == 0

def test_personne_afficher_output(capsys):
    """
    Teste la méthode afficher() pour s'assurer qu'elle imprime correctement.
    Utilise capsys de pytest pour capturer la sortie standard.
    """
    personne = Personne(
        nom="Test Affichage",
        age=30,
        revenu_annuel=36000,
        loyer=800,
        depenses_mensuelles=400,
        objectif=10000,
        duree_epargne=24,
        versement_mensuel_utilisateur=None
    )
    personne.afficher()
    captured = capsys.readouterr()
    
    assert "Personne: Test Affichage (âge: 30 ans)" in captured.out
    assert "Revenu annuel: 36000.00 €" in captured.out
    assert "Capacité d'épargne mensuelle estimée: 1800.00 €/mois" in captured.out
    assert "Objectif financier: 10000.00 € sur 24 mois" in captured.out