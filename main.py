from simulation.cluster import Cluster
import time

def main():
    cluster = Cluster(5)

    for cycle in range(5):
        print("\n--- Simulation Cycle ---")

        cluster.run_tasks()

        if cycle == 2:
            cluster.random_failure()

        time.sleep(2)

if __name__ == "__main__":
    main()