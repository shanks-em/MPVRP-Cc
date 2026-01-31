"""
Script pour valider une solution via l'API
"""

import sys
import os

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api_client import MPVRPAPIClient


def valider(instance_file, solution_file):
    """Valide une solution"""
    
    client = MPVRPAPIClient()
    
    print("="*70)
    print("VALIDATION DE SOLUTION")
    print("="*70)
    print(f"\nInstance : {instance_file}")
    print(f"Solution : {solution_file}\n")
    
    try:
        result = client.verify_solution(instance_file, solution_file)
        
        print("="*70)
        
        if result['feasible']:
            print("✅ SOLUTION VALIDE !")
            print("="*70)
            
            metrics = result.get('metrics', {})
            print("\n📊 MÉTRIQUES:\n")
            print(f"   Distance totale     : {metrics.get('total_distance', 'N/A'):.2f}")
            print(f"   Coût changeover     : {metrics.get('total_changeover_cost', 'N/A'):.2f}")
            print(f"   Véhicules utilisés  : {metrics.get('nb_vehicles_used', 'N/A')}")
            print(f"   Changements produit : {metrics.get('nb_product_changes', 'N/A')}")
            
            total_cost = metrics.get('total_distance', 0) + metrics.get('total_changeover_cost', 0)
            print(f"\n   COÛT TOTAL          : {total_cost:.2f}")
        else:
            print("❌ SOLUTION INVALIDE !")
            print("="*70)
            
            errors = result.get('errors', [])
            print(f"\n❌ ERREURS DÉTECTÉES ({len(errors)}):\n")
            
            for i, error in enumerate(errors[:10], 1):
                print(f"   {i}. {error}")
            
            if len(errors) > 10:
                print(f"\n   ... et {len(errors) - 10} autres erreurs")
        
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")


if name == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python valider_solution.py <instance.dat> <solution.dat>")
        sys.exit(1)
    
    valider(sys.argv[1], sys.argv[2])
