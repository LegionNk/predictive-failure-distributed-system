import csv
import os
from simulation.metrics import Metrics

class Monitor:
    def __init__(self, nodes):
        self.nodes = nodes
        self.dataset_file = "data/metrics.csv"

        # Create dataset file with header if it doesn't exist
        if not os.path.exists(self.dataset_file):
            with open(self.dataset_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["cpu", "memory", "latency", "status"])

    def collect_metrics(self):
        metrics_list = []

        for node in self.nodes:
            metric = Metrics(node.node_id, node.workload)

            metric.display()

            metrics_list.append(metric)

            with open(self.dataset_file, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    metric.cpu_usage,
                    metric.memory_usage,
                    metric.latency,
                    metric.status
                ])

        return metrics_list