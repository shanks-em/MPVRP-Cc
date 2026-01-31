"""
Programme principal MPVRP-CC
"""

import argparse
import sys
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from parser import parse_instance
from solver_simple import SimpleSolver
from solution_writer import write_solution, format_solution_summary
from validator import validate_solution
from api_client import MPVRPAPIClient, print_verification_result


def solve_instance_file(
    instance_path: Path,
    output_path: Path = None,
    changeover_weight: float = 0.5,
    verify_api: bool = False,
    verbose: bool = True
) -> bool:
    """Résout une instance"""
    try:
        # 1. LECTURE
        if verbose:
            print(f"\n{'='*70}")
            print(f"Instance: {instance_path.name}")
            print(f"{'='*70}")
            print("\n1️⃣  Lecture...", end=" ")
        
        instance = parse_instance(instance_path)
        
        if verbose:
            print("✅")
            print(f"   • {instance.nb_stations} stations")
            print(f"   • {instance.nb_products} produits")
            print(f"   • {instance.nb_vehicles} véhicules")
        
        # 2. RÉSOLUTION
        if verbose:
            print(f"\n2️⃣  Résolution...", end=" ")
        
        solver = SimpleSolver(instance, changeover_weight)
        solution = solver.solve()
        
        if verbose:
            print("✅")
            print(f"   • Coût: {solution.total_cost():.2f}")
        
        # 3. VALIDATION
        if verbose:
            print("\n3️⃣  Validation locale...", end=" ")
        
        is_valid, errors = validate_solution(solution)
        
        if is_valid:
            if verbose:
                print("✅")
        else:
            print("❌")
            for error in errors[:3]:
                print(f"   {error}")
            return False
        
        # 4. EXPORT
        if output_path is None:
            output_path = Path("solutions") / f"Sol_{instance_path.name}"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if verbose:
            print(f"\n4️⃣  Export...", end=" ")
        
        write_solution(solution, output_path)
        
        if verbose:
            print("✅")
            print(f"   📄 {output_path}")
        
        # 5. VALIDATION API
        if verify_api:
            if verbose:
                print("\n5️⃣  Vérification API...")
            
            client = MPVRPAPIClient()
            
            if not client.health_check():
                print("   ⚠️  API indisponible")
            else:
                result = client.verify_solution(instance_path, output_path)
                print_verification_result(result)
        
        if verbose:
            print("\n" + format_solution_summary(solution))
        
        return True
    
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="MPVRP-CC Solver",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python main.py instances/small/MPVRP_S_001.dat
  python main.py instances/small/MPVRP_S_001.dat --verify
  python main.py instances/small/MPVRP_S_001.dat -o ma_solution.dat
        """
    )
    
    parser.add_argument('instance', nargs='?', help="Fichier instance (.dat)")
    parser.add_argument('-o', '--output', help="Fichier sortie")
    parser.add_argument('-w', '--weight', type=float, default=0.5, help="Poids changeover (default: 0.5)")
    parser.add_argument('--verify', action='store_true', help="Valider avec API")
    parser.add_argument('-q', '--quiet', action='store_true', help="Mode silencieux")
    
    args = parser.parse_args()
    
    if args.instance:
        instance_path = Path(args.instance)
        
        if not instance_path.exists():
            print(f"❌ Erreur: Fichier introuvable: {instance_path}")
            sys.exit(1)
        
        output_path = Path(args.output) if args.output else None
        
        success = solve_instance_file(
            instance_path,
            output_path,
            args.weight,
            args.verify,
            not args.quiet
        )
        
        sys.exit(0 if success else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
