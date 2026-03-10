import random
import time

class Metrics:
    def __init__(self, node_id):
        self.node_id = node_id
        self.cpu_usage = random.uniform(10, 90)
        self.memory_usage = random.uniform(100, 800)
        self.timestamp = time.time()

    def display(self):
        print(
            f"Node {self.node_id} | CPU: {self.cpu_usage:.2f}% | "
            f"Memory: {self.memory_usage:.2f}MB"
        )