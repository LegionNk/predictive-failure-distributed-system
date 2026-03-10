import random
import time

class Metrics:
    def __init__(self, node_id, workload):
        self.node_id = node_id

        # CPU increases with workload
        self.cpu_usage = 20 + workload * 15 + random.uniform(-5, 5)

        # Memory increases with workload
        self.memory_usage = 200 + workload * 120 + random.uniform(-50, 50)

        # Simulated latency
        self.latency = random.uniform(0.5, 3.5)

        # Failure condition
        if self.cpu_usage > 85 or self.memory_usage > 800:
            self.status = 1
        else:
            self.status = 0

        self.timestamp = time.time()

    def display(self):
        print(
            f"Node {self.node_id} | CPU: {self.cpu_usage:.2f}% | "
            f"Memory: {self.memory_usage:.2f}MB | "
            f"Latency: {self.latency:.2f}s"
        )