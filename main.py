print("=" * 50)
print(" INITIALIZING DISTRIBUTED CLUSTER...")
print(" LOADING FAILURE PREDICTION MODEL...")
print(" STARTING NODE MONITORING...")
print("=" * 50)
from simulation.cluster import Cluster

def generate_dataset(iterations=5):

    cluster = Cluster(num_nodes=10)

    for i in range(iterations):
        print("\n=================================")
        print(f" Simulation Cycle {i+1}")
        print("=================================")
        cluster.run_simulation()


if __name__ == "__main__":
    generate_dataset(5)  