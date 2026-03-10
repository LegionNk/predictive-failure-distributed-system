import random
import time

class Metrics:

    def __init__(self, node_id, workload):

        self.node_id = node_id

        # CPU increases with workload
        self.cpu_usage = 20 + workload * 10 + random.uniform(-5, 5)

        # Memory increases with workload
        self.memory_usage = 200 + workload * 80 + random.uniform(-40, 40)

        # Simulated network / processing latency
        self.latency = random.uniform(0.5, 3.5)

        # ----- Probabilistic failure model -----
        failure_probability = 0.05

        if self.cpu_usage > 70:
            failure_probability += 0.25

        if self.memory_usage > 600:
            failure_probability += 0.25

        if self.latency > 2:
            failure_probability += 0.20

        self.status = 1 if random.random() < failure_probability else 0

        self.timestamp = time.time()


    def display(self):

        print(
            f"Node {self.node_id} | CPU: {self.cpu_usage:.2f}% | "
            f"Memory: {self.memory_usage:.2f}MB | "
            f"Latency: {self.latency:.2f}s | "
            f"FailureRisk: {self.status}"
        )