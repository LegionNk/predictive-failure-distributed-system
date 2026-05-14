import random


class Node:

    def __init__(self, node_id):

        self.node_id = node_id
        self.status = "alive"

        # System metrics
        self.cpu_usage = random.uniform(10, 90)
        self.memory_usage = random.uniform(200, 800)
        self.latency = random.uniform(1, 10)


    def run_task(self, task):

        print(f"Node {self.node_id} executing Task {task.task_id}")

        # Simulate workload increase
        self.cpu_usage += random.randint(5, 15)

        self.memory_usage += random.randint(20, 50)

        self.latency += random.uniform(0.5, 2.0)

        # Prevent unrealistic values
        self.cpu_usage = min(self.cpu_usage, 100)

        self.memory_usage = min(self.memory_usage, 1000)

        self.latency = min(self.latency, 20)

    def fail(self):

        self.status = "failed"
        print(f"Node {self.node_id} FAILED")