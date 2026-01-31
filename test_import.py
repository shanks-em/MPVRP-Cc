"""
Script de test pour vérifier les imports
"""

import sys
import os

print("Test d'imports...\n")
print(f"Répertoire courant: {os.getcwd()}")
print(f"Python path: {sys.path[:3]}\n")

try:
    from src.api_client import MPVRPAPIClient
    print("✅ Import api_client réussi")
    
    from src.instance_reader import Instance
    print("✅ Import instance_reader réussi")
    
    from src.solver import GreedySolver
    print("✅ Import solver réussi")
    
    from src.solution_model import Solution
    print("✅ Import solution_model réussi")
    
    print("\n✅ Tous les imports fonctionnent !")
    
    # Test création client
    print("\nTest création client API...")
    client = MPVRPAPIClient()
    print("✅ Client API créé")
    
    print("\nTest health check...")
    if client.health_check():
        print("✅ API disponible")
    else:
        print("⚠️  API non disponible (mais imports OK)")
    
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)
