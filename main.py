from simulation.cluster import Cluster
import time

def main():
    cluster = Cluster(5)

    cluster.generate_tasks(10)

    cluster.schedule_tasks()

    cluster.random_failure()

    cluster.monitor_system()

if __name__ == "__main__":
    main()