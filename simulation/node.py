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

        if self.status == "alive":

            print(f"Node {self.node_id} executing Task {task.task_id}")

            # simulate system load changes
            self.cpu_usage = random.uniform(10, 95)
            self.memory_usage = random.uniform(200, 900)
            self.latency = random.uniform(1, 15)

        else:
            print(f"Node {self.node_id} is failed and cannot run tasks")


    def fail(self):

        self.status = "failed"
        print(f"Node {self.node_id} FAILED")