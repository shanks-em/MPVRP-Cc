"""
Test rapide de l'API et du système
"""

import sys
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from api_client import MPVRPAPIClient


def test_api_connectivity():
    """Test de connectivité avec l'API"""
    
    print("\n" + "="*70)
    print("TEST DE CONNECTIVITÉ API MPVRP-CC")
    print("="*70 + "\n")
    
    # Créer le client
    client = MPVRPAPIClient()
    
    print(f"URL de l'API: {client.base_url}")
    print("\nTest de connexion...", end=" ")
    
    # Test health check
    if client.health_check():
        print("✅ API disponible!\n")
        
        print("Statut: ✅ Prêt pour la génération et la validation")
        print("\nPour commencer:")
        print("  1. Générer des instances:")
        print("     python scripts/generate_instances.py --suite")
        print("\n  2. Résoudre une instance:")
        print("     python main.py instances/small/MPVRP_S_001.dat --verify")
        
        return True
    else:
        print("❌ API indisponible\n")
        print("Causes possibles:")
        print("  - Pas de connexion internet")
        print("  - L'API est en cours de démarrage (attendre 30s)")
        print("  - URL incorrecte")
        print("\nRéessayez dans quelques instants...")
        
        return False


if __name__ == "__main__":
    success = test_api_connectivity()
    sys.exit(0 if success else 1)
