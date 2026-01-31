"""
Script de test de validation API
"""

import sys
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from api_client import MPVRPAPIClient, print_verification_result


def test_validation(instance_path: Path, solution_path: Path):
    """
    Test de validation d'une solution via l'API
    
    Args:
        instance_path: Chemin vers le fichier instance
        solution_path: Chemin vers le fichier solution
    """
    print(f"\n{'='*70}")
    print("TEST DE VALIDATION API")
    print(f"{'='*70}")
    print(f"Instance : {instance_path}")
    print(f"Solution : {solution_path}")
    print(f"{'='*70}\n")
    
    # Vérifier que les fichiers existent
    if not instance_path.exists():
        print(f"❌ Instance introuvable: {instance_path}")
        return False
    
    if not solution_path.exists():
        print(f"❌ Solution introuvable: {solution_path}")
        return False
    
    # Client API
    client = MPVRPAPIClient()
    
    # Test de connexion
    print("1. Test de connexion API...")
    if not client.health_check():
        print("   ❌ API indisponible")
        print(f"   URL: {client.base_url}")
        return False
    print("   ✅ API disponible\n")
    
    # Validation
    print("2. Validation de la solution...")
    result = client.verify_solution(instance_path, solution_path)
    
    # Afficher le résultat
    print_verification_result(result)
    
    return result.get('feasible', False)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Test de validation API",
        epilog="""
Exemples:
  python test_validation.py instances/small/MPVRP_S_001.dat solutions/Sol_MPVRP_S_001.dat
        """
    )
    
    parser.add_argument('instance', help="Fichier instance")
    parser.add_argument('solution', help="Fichier solution")
    
    args = parser.parse_args()
    
    instance_path = Path(args.instance)
    solution_path = Path(args.solution)
    
    success = test_validation(instance_path, solution_path)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
