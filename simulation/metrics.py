import csv
import os


class Metrics:

    def __init__(self, node_id, cpu, memory, latency, status):

        self.node_id = node_id
        self.cpu = cpu
        self.memory = memory
        self.latency = latency
        self.status = status

    def log(self):

        print(
            f"Node {self.node_id} | CPU: {self.cpu:.2f}% | "
            f"Memory: {self.memory:.2f}MB | "
            f"Latency: {self.latency:.2f}ms | "
            f"Status: {self.status}"
        )

        file_exists = os.path.isfile("data/runtime_metrics.csv")

        with open("data/runtime_metrics.csv", "a", newline="") as file:

            writer = csv.writer(file)

            if not file_exists:

                writer.writerow([
                    "node_id",
                    "cpu_usage",
                    "memory_usage",
                    "latency",
                    "status"
                ])

            writer.writerow([
                self.node_id,
                self.cpu,
                self.memory,
                self.latency,
                self.status
            ])