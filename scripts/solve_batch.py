"""
Résolution en batch de plusieurs instances
"""

import sys
from pathlib import Path
import time
import csv

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from parser import parse_instance
from solver_simple import SimpleSolver
from solution_writer import write_solution
from validator import validate_solution
from api_client import MPVRPAPIClient


def solve_batch(
    instance_dir: Path,
    output_dir: Path = None,
    verify_api: bool = False,
    changeover_weight: float = 0.5
):
    """
    Résout toutes les instances d'un dossier
    
    Args:
        instance_dir: Dossier contenant les instances
        output_dir: Dossier de sortie pour les solutions
        verify_api: Vérifier avec l'API
        changeover_weight: Poids du coût de changeover
    """
    if output_dir is None:
        output_dir = Path("solutions")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Trouver toutes les instances
    instances = sorted(instance_dir.glob("*.dat"))
    
    if not instances:
        print(f"❌ Aucune instance trouvée dans {instance_dir}")
        return
    
    print(f"\n{'='*70}")
    print(f"RÉSOLUTION EN BATCH")
    print(f"{'='*70}")
    print(f"Instances trouvées: {len(instances)}")
    print(f"Dossier sortie: {output_dir}")
    print(f"{'='*70}\n")
    
    # Résultats
    results = []
    
    # Client API
    client = None
    if verify_api:
        client = MPVRPAPIClient()
        if not client.health_check():
            print("⚠️  API indisponible, vérification désactivée\n")
            verify_api = False
    
    # Résoudre chaque instance
    for i, instance_path in enumerate(instances, 1):
        print(f"\n[{i}/{len(instances)}] {instance_path.name}")
        print("-" * 70)
        
        try:
            # Parsing
            instance = parse_instance(instance_path)
            
            # Résolution
            start = time.time()
            solver = SimpleSolver(instance, changeover_weight)
            solution = solver.solve()
            solve_time = time.time() - start
            
            # Validation locale
            is_valid, errors = validate_solution(solution)
            
            if not is_valid:
                print(f"❌ Solution invalide ({len(errors)} erreurs)")
                for error in errors[:3]:
                    print(f"   - {error}")
                continue
            
            # Export
            solution_path = output_dir / f"Sol_{instance_path.name}"
            write_solution(solution, solution_path)
            
            # Métriques
            result = {
                'instance': instance_path.name,
                'stations': instance.nb_stations,
                'products': instance.nb_products,
                'vehicles_used': solution.nb_vehicles_used(),
                'distance': solution.total_distance(),
                'transition_cost': solution.total_transition_cost(),
                'total_cost': solution.total_cost(),
                'transitions': solution.total_transitions(),
                'solve_time': solve_time,
                'valid_local': is_valid,
                'valid_api': None
            }
            
            print(f"✅ Résolu en {solve_time:.2f}s")
            print(f"   Coût total: {solution.total_cost():.2f}")
            print(f"   Distance: {solution.total_distance():.2f}")
            print(f"   Transition: {solution.total_transition_cost():.2f}")
            
            # Vérification API
            if verify_api:
                print("   Vérification API...", end=" ")
                api_result = client.verify_solution(instance_path, solution_path)
                result['valid_api'] = api_result.get('feasible', False)
                
                if result['valid_api']:
                    print("✅")
                else:
                    print("❌")
                    errors = api_result.get('errors', [])
                    for error in errors[:2]:
                        print(f"      - {error}")
            
            results.append(result)
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
    
    # Rapport final
    print(f"\n{'='*70}")
    print("RAPPORT FINAL")
    print(f"{'='*70}")
    
    if results:
        print(f"\nInstances résolues: {len(results)}/{len(instances)}")
        
        # Statistiques
        avg_cost = sum(r['total_cost'] for r in results) / len(results)
        avg_time = sum(r['solve_time'] for r in results) / len(results)
        
        print(f"\nCoût moyen: {avg_cost:.2f}")
        print(f"Temps moyen: {avg_time:.2f}s")
        
        if verify_api:
            valid_api = sum(1 for r in results if r['valid_api'])
            print(f"Validées API: {valid_api}/{len(results)}")
        
        # Export CSV
        csv_path = output_dir / "batch_results.csv"
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        
        print(f"\n📊 Rapport détaillé: {csv_path}")
    
    print(f"{'='*70}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Résolution en batch")
    parser.add_argument('instance_dir', help="Dossier d'instances")
    parser.add_argument('-o', '--output', help="Dossier de sortie")
    parser.add_argument('--verify', action='store_true', help="Vérifier avec API")
    parser.add_argument('-w', '--weight', type=float, default=0.5, help="Poids changeover")
    
    args = parser.parse_args()
    
    instance_dir = Path(args.instance_dir)
    output_dir = Path(args.output) if args.output else None
    
    if not instance_dir.exists():
        print(f"❌ Dossier introuvable: {instance_dir}")
        sys.exit(1)
    
    solve_batch(instance_dir, output_dir, args.verify, args.weight)


if __name__ == "__main__":
    main()
