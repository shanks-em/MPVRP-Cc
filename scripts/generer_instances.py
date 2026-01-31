"""
Script pour générer des instances de test via l'API
"""

import sys
import os

# Ajouter le dossier parent au path pour importer src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api_client import MPVRPAPIClient


def generer_instances():
    """Génère plusieurs instances de test"""
    
    client = MPVRPAPIClient()
    
    # Vérifier que l'API fonctionne
    print("🔍 Vérification de l'API...")
    if not client.health_check():
        print("❌ API indisponible")
        return
    
    print("✅ API disponible\n")
    
    # Configurations des instances
    configs = {
        "small": [
            {
                "id_instance": "small_01",
                "nb_vehicles": 2,
                "nb_depots": 1,
                "nb_garages": 1,
                "nb_stations": 5,
                "nb_produits": 2,
                "max_coord": 100,
                "min_capacite": 15000,
                "max_capacite": 20000,
                "min_transition_cost": 10,
                "max_transition_cost": 30,
                "min_demand": 1000,
                "max_demand": 3000,
                "seed": 42
            },
            {
                "id_instance": "small_02",
                "nb_vehicles": 3,
                "nb_depots": 2,
                "nb_garages": 1,
                "nb_stations": 10,
                "nb_produits": 3,
                "max_coord": 100,
                "min_capacite": 15000,
                "max_capacite": 20000,
                "min_transition_cost": 10,
                "max_transition_cost": 40,
                "min_demand": 800,
                "max_demand": 2500,
                "seed": 43
            }
        ],
        "medium": [
            {
                "id_instance": "medium_01",
                "nb_vehicles": 5,
                "nb_depots": 3,
                "nb_garages": 2,
                "nb_stations": 25,
                "nb_produits": 4,
                "max_coord": 150,
                "min_capacite": 18000,
                "max_capacite": 25000,
                "min_transition_cost": 15,
                "max_transition_cost": 60,
                "min_demand": 500,
                "max_demand": 3000,
                "seed": 44
            }
        ],
        "large": [
            {
                "id_instance": "large_01",
                "nb_vehicles": 8,
                "nb_depots": 4,
                "nb_garages": 3,
                "nb_stations": 50,
                "nb_produits": 5,
                "max_coord": 200,
                "min_capacite": 20000,
                "max_capacite": 30000,
                "min_transition_cost": 20,
                "max_transition_cost": 80,
                "min_demand": 500,
                "max_demand": 4000,
                "seed": 45
            }
        ]
    }
    
    # Générer les instances
    for category, instances in configs.items():
        print(f"\n📦 Génération catégorie {category.upper()}...")
        
        # Créer le dossier si nécessaire
        folder = os.path.join("instances", category)
        os.makedirs(folder, exist_ok=True)
        
        for params in instances:
            try:
                print(f"   Génération {params['id_instance']}...", end=" ")
                
                content = client.generate_instance(params)
                
                filename = os.path.join(folder, f"MPVRP_{params['id_instance']}.dat")
                with open(filename, 'w') as f:
                    f.write(content)
                
                print(f"✅")
                
            except Exception as e:
                print(f"❌ Erreur: {e}")
    
    print("\n✅ Génération terminée !")
    print("\nInstances créées dans le dossier 'instances/'")


if name == "__main__":
    generer_instances()
