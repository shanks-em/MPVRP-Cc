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
  A faire
  
## Installation
```bash
# Clone the repository
git clone https://github.com/shanks-em/MPVRP-Cc.git
cd MPVRP-Cc

# Install dependencies
pip install -r requirements.txt
```
 
## Use
A faire

## Instances
Benchmark instances are available in three categories based on problem size:

| Category | Stations | Depots | Products |
|----------|----------|--------|----------|
| Small    | 5 – 50   | 2 – 4  | 2 – 5    |
| Medium   | 50 – 100 | 4 – 7  | 5 – 8    |
| Large    | 100 – 200| 6 – 10 | 8 – 12   |

Each category is designed to evaluate the scalability and performance of the proposed solution methods under increasing problem complexity.

