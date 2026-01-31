"""
Client API MPVRP-CC - Version robuste avec affichage métriques amélioré
"""

import requests
from pathlib import Path
from typing import Union, Dict, Any, Optional


class MPVRPAPIClient:
    """Client pour l'API MPVRP-CC"""
    
    DEFAULT_URL = "https://mpvrp-cc.onrender.com"
    
    def __init__(self, base_url: str = None):
        self.base_url = (base_url or self.DEFAULT_URL).rstrip('/')
    
    def health_check(self, timeout: int = 5) -> bool:
        """Vérifie si l'API est disponible"""
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=timeout
            )
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def verify_solution(
        self,
        instance_path: Union[str, Path],
        solution_path: Union[str, Path],
        timeout: int = 60
    ) -> Dict[str, Any]:
        """
        Vérifie une solution via l'API.
        
        Args:
            instance_path: Chemin vers le fichier instance
            solution_path: Chemin vers le fichier solution
            timeout: Timeout en secondes
        
        Returns:
            dict: Résultat de la vérification
                {
                    'feasible': bool,
                    'errors': List[str],
                    'metrics': dict
                }
        """
        instance_path = Path(instance_path)
        solution_path = Path(solution_path)
        
        if not instance_path.exists():
            return {
                'feasible': False,
                'errors': [f"Fichier instance introuvable: {instance_path}"],
                'metrics': {}
            }
        
        if not solution_path.exists():
            return {
                'feasible': False,
                'errors': [f"Fichier solution introuvable: {solution_path}"],
                'metrics': {}
            }
        
        try:
            with open(instance_path, 'rb') as f_inst, \
                 open(solution_path, 'rb') as f_sol:
                
                files = {
                    'instance_file': (instance_path.name, f_inst, 'application/octet-stream'),
                    'solution_file': (solution_path.name, f_sol, 'application/octet-stream')
                }
                
                response = requests.post(
                    f"{self.base_url}/model/verify",
                    files=files,
                    timeout=timeout
                )
            
            if response.status_code == 200:
                data = response.json()
                
                # DEBUG: Afficher la réponse brute
                print(f"\n[DEBUG] Réponse API brute:")
                print(f"  feasible: {data.get('feasible')}")
                print(f"  errors: {len(data.get('errors', []))} erreur(s)")
                print(f"  metrics présentes: {bool(data.get('metrics'))}")
                if data.get('metrics'):
                    print(f"  contenu metrics: {list(data.get('metrics', {}).keys())}")
                
                return data
            else:
                return {
                    'feasible': False,
                    'errors': [f"Erreur HTTP {response.status_code}: {response.text[:200]}"],
                    'metrics': {}
                }
        
        except requests.Timeout:
            return {
                'feasible': False,
                'errors': ["Timeout de l'API (> 60s)"],
                'metrics': {}
            }
        except requests.RequestException as e:
            return {
                'feasible': False,
                'errors': [f"Erreur de connexion: {str(e)}"],
                'metrics': {}
            }
        except Exception as e:
            return {
                'feasible': False,
                'errors': [f"Erreur inattendue: {str(e)}"],
                'metrics': {}
            }
    
    def generate_instance(
        self,
        params: Dict[str, Any],
        timeout: int = 30
    ) -> Optional[str]:
        """
        Génère une instance via l'API.
        
        Args:
            params: Paramètres de l'instance
            timeout: Timeout en secondes
        
        Returns:
            str: Contenu du fichier .dat ou None
        """
        try:
            response = requests.post(
                f"{self.base_url}/generator/generate",
                json=params,
                timeout=timeout
            )
            
            if response.status_code == 200:
                return response.text
            else:
                print(f"Erreur génération: {response.status_code}")
                return None
        
        except requests.RequestException as e:
            print(f"Erreur connexion: {e}")
            return None


def print_verification_result(result: Dict[str, Any], verbose: bool = True):
    """
    Affiche le résultat de vérification de manière formatée.
    
    Args:
        result: Résultat de la vérification
        verbose: Afficher les détails
    """
    print("\n" + "=" * 70)
    print("RÉSULTAT DE VÉRIFICATION API")
    print("=" * 70)
    
    # Statut principal
    if result.get('feasible'):
        print("✅ SOLUTION VALIDE")
    else:
        print("❌ SOLUTION INVALIDE")
    
    # Erreurs
    errors = result.get('errors', [])
    if errors:
        print(f"\nErreurs ({len(errors)}):")
        for i, error in enumerate(errors[:10], 1):
            print(f"  {i}. {error}")
        
        if len(errors) > 10:
            print(f"  ... et {len(errors) - 10} autres erreurs")
    
    # Métriques - AMÉLIORÉ
    metrics = result.get('metrics')
    
    if metrics:
        print("\n📊 Métriques de la Solution:")
        print("-" * 70)
        
        # Essayer différentes clés possibles
        distance_keys = ['total_distance', 'distance', 'totalDistance']
        transition_keys = ['total_changeover_cost', 'total_transition_cost', 
                          'changeover_cost', 'transition_cost', 'totalChangeoverCost']
        vehicles_keys = ['nb_vehicles_used', 'vehicles_used', 'nbVehiclesUsed']
        changes_keys = ['nb_product_changes', 'product_changes', 'nbProductChanges', 'transitions']
        
        # Distance
        distance = None
        for key in distance_keys:
            if key in metrics:
                distance = metrics[key]
                break
        
        if distance is not None:
            print(f"  Distance totale      : {distance:.2f}")
        else:
            print(f"  Distance totale      : N/A")
            if verbose:
                print(f"    [DEBUG] Clés cherchées: {distance_keys}")
        
        # Coût transition
        transition = None
        for key in transition_keys:
            if key in metrics:
                transition = metrics[key]
                break
        
        if transition is not None:
            print(f"  Coût transition      : {transition:.2f}")
        else:
            print(f"  Coût transition      : N/A")
            if verbose:
                print(f"    [DEBUG] Clés cherchées: {transition_keys}")
        
        # Véhicules
        vehicles = None
        for key in vehicles_keys:
            if key in metrics:
                vehicles = metrics[key]
                break
        
        if vehicles is not None:
            print(f"  Véhicules utilisés   : {vehicles}")
        else:
            print(f"  Véhicules utilisés   : N/A")
        
        # Changements
        changes = None
        for key in changes_keys:
            if key in metrics:
                changes = metrics[key]
                break
        
        if changes is not None:
            print(f"  Changements produit  : {changes}")
        else:
            print(f"  Changements produit  : N/A")
        
        # Coût total
        if distance is not None and transition is not None:
            total = distance + transition
            print(f"  {'─' * 68}")
            print(f"  COÛT TOTAL           : {total:.2f}")
        
        # Afficher toutes les clés disponibles en mode verbose
        if verbose:
            print(f"\n[DEBUG] Clés disponibles dans metrics:")
            for key, value in metrics.items():
                print(f"    {key}: {value}")
    
    elif result.get('feasible'):
        # Solution valide mais pas de métriques
        print("\n⚠️  Métriques non disponibles")
        print("    L'API a validé la solution mais n'a pas retourné de métriques.")
        print("    Ceci peut arriver si:")
        print("    - L'API a un problème temporaire")
        print("    - Le format de réponse a changé")
        print("\n    Les métriques calculées localement sont dans le fichier solution.")
    
    print("=" * 70)


def compare_metrics(local_solution, api_result):
    """
    Compare les métriques locales avec celles de l'API
    
    Args:
        local_solution: Solution object
        api_result: Résultat de l'API
    """
    if not api_result.get('feasible'):
        return
    
    metrics = api_result.get('metrics', {})
    if not metrics:
        return
    
    print("\n" + "=" * 70)
    print("COMPARAISON MÉTRIQUES LOCALES vs API")
    print("=" * 70)
    
    # Distance
    local_dist = local_solution.total_distance()
    api_dist = metrics.get('total_distance') or metrics.get('distance')
    
    if api_dist:
        diff_dist = abs(local_dist - api_dist)
        match_dist = "✅" if diff_dist < 0.01 else "⚠️"
        print(f"\nDistance:")
        print(f"  Locale : {local_dist:.2f}")
        print(f"  API    : {api_dist:.2f}")
        print(f"  {match_dist} Différence : {diff_dist:.2f}")
    
    # Coût transition
    local_trans = local_solution.total_transition_cost()
    api_trans = (metrics.get('total_changeover_cost') or 
                 metrics.get('total_transition_cost') or
                 metrics.get('changeover_cost'))
    
    if api_trans:
        diff_trans = abs(local_trans - api_trans)
        match_trans = "✅" if diff_trans < 0.01 else "⚠️"
        print(f"\nCoût transition:")
        print(f"  Local  : {local_trans:.2f}")
        print(f"  API    : {api_trans:.2f}")
        print(f"  {match_trans} Différence : {diff_trans:.2f}")
    
    # Véhicules
    local_veh = local_solution.nb_vehicles_used()
    api_veh = (metrics.get('nb_vehicles_used') or 
               metrics.get('vehicles_used'))
    
    if api_veh:
        match_veh = "✅" if local_veh == api_veh else "⚠️"
        print(f"\nVéhicules utilisés:")
        print(f"  Local  : {local_veh}")
        print(f"  API    : {api_veh}")
        print(f"  {match_veh}")
    
    print("=" * 70)
