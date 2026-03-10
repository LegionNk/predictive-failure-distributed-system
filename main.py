from simulation.cluster import Cluster
from simulation.monitor import Monitor

def generate_dataset(iterations=500):

    cluster = Cluster(num_nodes=10)
    monitor = Monitor(cluster.nodes)

    for i in range(iterations):
        print(f"\nSimulation Cycle {i+1}")

        cluster.run_simulation()

        monitor.collect_metrics()


if __name__ == "__main__":
    generate_dataset(500)