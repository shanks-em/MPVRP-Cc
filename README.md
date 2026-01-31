# MPVRP-Co
## Description 
Logistics optimization remains a major challenge for companies worldwide. Efficient distribution of goods directly impacts operational costs, customer satisfaction, and environmental footprint. Among the various optimization problems studied in operations research, vehicle routing problems (VRP) occupy a central place due to their practical relevance and computational complexity.

Each industrial sector introduces its own specific constraints. In petroleum distribution, for instance, tanker trucks must deliver multiple fuel types to service stations while managing product compatibility within their compartments. Changing the product carried by a vehicle requires tank cleaning, which incurs additional costs and time.

We present the Multi-Product Vehicle Routing Problem with Changeover Cost (MPVRP-CC), a variant of the classic VRP tailored to these challenges. The MPVRP-CC aims to organize the efficient distribution of multiple product types from a set of depots to a network of service stations, while accounting for the changeover cost when a vehicle switches between products.

## Documentation
Detailed problem specifications and instance structures can be found in the 
[overview](docs/problem_definition.pdf) and [data format](docs/instance_description.pdf) sections, respectively. 
Our dataset includes 50 instances partitioned into small, medium, and large categories to 
reflect varying scales of stations, depots, and product quantities. Although reference 
solutions are not included, the expected submission format is outlined 
[here](docs/solution_description.pdf).


## Structure
MPVRP-CC/
├── docs/
│   ├── .gitkeep
│   ├── Modelisation.pdf
│   ├── instance_description.pdf
│   ├── problem_definition.pdf
│   └── solution_description.pdf
├── instances/
│   ├── high/
│   ├── medium/
│   └── small/
├── scripts/
│   ├── .gitkeep
│   ├── generer_instances.py
│   ├── solve_batch.py
│   ├── test_validation.py
│   └── valider_solution.py
├── solutions/
│   └── .gitkeep
├── src/
│   ├── .gitkeep
│   ├── __init__.py
│   ├── api_client.py
│   ├── models.py
│   ├── parser.py
│   ├── solution_model.py
│   ├── solution_writer.py
│   ├── solver_simple.py
│   ├── test_api.py
│   └── validator.py
├── tests/
│   └── .gitkeep
├── README.md
├── main.py
├── requirements.txt
├── test_api.py
└── test_import.py
```  
## Installation
```bash
# Clone the repository
git clone https://github.com/shanks-em/MPVRP-Cc.git
cd MPVRP-Cc

# Install dependencies
pip install -r requirements.txt
```
 
## Use
# MPVRP-CC - Multi-Product Vehicle Routing Problem with Changeover Cost

## Installation & Setup

### Create Virtual Environment
```bash
cd MPVRP-CC
python3 -m venv venv
```

### Activate Virtual Environment
```bash
source venv/bin/activate
```

## Usage

### Test API Connection
```bash
python3 test_api.py
```

### Generate Instances
```bash
python3 scripts/generate_instances.py
```

### Solve Single Instance
```bash
python3 main.py instances/path/to/instance.dat
```

### Validate Solution
```bash
python3 scripts/test_validation.py instances/path/to/instance.dat solutions/path/to/Sol_instance.dat
```

### Batch Testing

**Small instances:**
```bash
python3 scripts/solve_batch.py instances/small/ --verify
```

**Medium instances:**
```bash
python3 scripts/solve_batch.py instances/medium/ --verify
```

**Large instances:**
```bash
python3 scripts/solve_batch.py instances/large/ --verify
```

### View Batch Results
```bash
gedit solutions/batch_results.csv
```

## Instances
Benchmark instances are available in three categories based on problem size:

| Category | Stations | Depots | Products |
|----------|----------|--------|----------|
| Small    | 5 – 50   | 2 – 4  | 2 – 5    |
| Medium   | 50 – 100 | 4 – 7  | 5 – 8    |
| Large    | 100 – 200| 6 – 10 | 8 – 12   |

Each category is designed to evaluate the scalability and performance of the proposed solution methods under increasing problem complexity.

