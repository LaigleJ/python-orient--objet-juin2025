
from src.mon_module.models.personne import Personne
from src.mon_module.models.epargne import Epargne
from src.mon_module.utils import calcul_interets_composes # <-- Nouvelle importation

# --- Tests des classes Personne et Epargne (vos tests précédents) ---
print("\n" + "="*50 + "\n") # Séparateur pour la lisibilité

# --- Tests de la fonction calcul_interets_composes ---

print("--- Tests de calcul_interets_composes ---")

# Exemple 1: Versement annuel de 1000€, taux 5%, durée 1 an
resultat1 = calcul_interets_composes(1000, 0.05, 1)
print(f"Exemple 1 (1000€/an, 5%, 1 an): {resultat1:.2f} €") 

# Exemple 2: Versement annuel de 100€, taux 10%, durée 2 ans
resultat2 = calcul_interets_composes(100, 0.10, 2)
print(f"Exemple 2 (100€/an, 10%, 2 ans): {resultat2:.2f} €") 

# Exemple 3: Versement annuel de 0€, taux 5%, durée 5 ans (pas d'épargne)
resultat3 = calcul_interets_composes(0, 0.05, 5)
print(f"Exemple 3 (0€/an, 5%, 5 ans): {resultat3:.2f} €") 

# Exemple 4: Tests de validation (vérifier les erreurs)
try:
    calcul_interets_composes(100, 0.05, -1)
except ValueError as e:
    print(f"Erreur attendue pour durée négative: {e}")

try:
    calcul_interets_composes(100, -0.05, 1)
except ValueError as e:
    print(f"Erreur attendue pour taux négatif: {e}")

try:
    calcul_interets_composes(-100, 0.05, 1)
except ValueError as e:
    print(f"Erreur attendue pour versement négatif: {e}")