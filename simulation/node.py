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

        # Simulate workload changes

        self.cpu_usage += random.uniform(2, 8)

        self.memory_usage += random.uniform(10, 50)

        self.latency += random.uniform(0.5, 2)

        # Keep values within realistic limits

        self.cpu_usage = min(self.cpu_usage, 100)

        self.memory_usage = min(self.memory_usage, 1000)

        self.latency = min(self.latency, 20)
        
    def fail(self):

        self.status = "failed"
        print(f"Node {self.node_id} FAILED")