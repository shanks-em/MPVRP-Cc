"""
Parser robuste pour fichiers .dat
"""

from pathlib import Path
from typing import Union
from models import Instance, Vehicle, Depot, Garage, Station


def parse_instance(filepath: Union[str, Path]) -> Instance:
    """Parse un fichier .dat avec gestion d'erreurs"""
    
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Fichier introuvable: {filepath}")
    
    try:
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        if not lines:
            raise ValueError("Fichier vide")
        
        idx = 0
        
        # UUID
        uuid = lines[idx].replace('#', '').strip()
        idx += 1
        
        # Paramètres
        params = list(map(int, lines[idx].split()))
        if len(params) != 5:
            raise ValueError(f"Ligne paramètres invalide: {lines[idx]}")
        
        nb_products, nb_depots, nb_garages, nb_stations, nb_vehicles = params
        idx += 1
        
        # Matrice transition
        transition_costs = []
        for i in range(nb_products):
            row = list(map(float, lines[idx].split()))
            if len(row) != nb_products:
                raise ValueError(f"Matrice transition ligne {i} invalide")
            transition_costs.append(row)
            idx += 1
        
        # Véhicules
        vehicles = []
        for i in range(nb_vehicles):
            parts = list(map(int, lines[idx].split()))
            if len(parts) != 4:
                raise ValueError(f"Ligne véhicule {i} invalide")
            vehicles.append(Vehicle(*parts))
            idx += 1
        
        # Dépôts
        depots = []
        for i in range(nb_depots):
            parts = lines[idx].split()
            depot_id = int(parts[0])
            x, y = float(parts[1]), float(parts[2])
            stocks = [int(parts[3 + p]) for p in range(nb_products)]
            depots.append(Depot(depot_id, x, y, stocks))
            idx += 1
        
        # Garages
        garages = []
        for i in range(nb_garages):
            parts = lines[idx].split()
            garages.append(Garage(int(parts[0]), float(parts[1]), float(parts[2])))
            idx += 1
        
        # Stations
        stations = []
        for i in range(nb_stations):
            parts = lines[idx].split()
            station_id = int(parts[0])
            x, y = float(parts[1]), float(parts[2])
            demands = [int(parts[3 + p]) for p in range(nb_products)]
            stations.append(Station(station_id, x, y, demands))
            idx += 1
        
        return Instance(
            uuid=uuid,
            nb_products=nb_products,
            nb_depots=nb_depots,
            nb_garages=nb_garages,
            nb_stations=nb_stations,
            nb_vehicles=nb_vehicles,
            transition_costs=transition_costs,
            vehicles=vehicles,
            depots=depots,
            garages=garages,
            stations=stations
        )
    
    except Exception as e:
        raise ValueError(f"Erreur parsing {filepath.name}: {e}")
