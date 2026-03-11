from simulation.cluster import Cluster

def generate_dataset(iterations=5):

    cluster = Cluster(num_nodes=10)

    for i in range(iterations):
        print(f"\nSimulation Cycle {i+1}")

        cluster.run_simulation()


if __name__ == "__main__":
    generate_dataset(5)