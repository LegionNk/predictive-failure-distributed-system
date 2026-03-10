import time
import random

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.status = "alive"
        self.workload = 0

    def run_task(self, task):
        if self.status == "alive":
            self.workload += 1
            print(f"Node {self.node_id} executing Task {task.task_id}")

            time.sleep(random.uniform(0.5, 1.5))

            self.workload -= 1
        else:
            print(f"Node {self.node_id} is down")

    def fail(self):
        self.status = "failed"
        print(f"Node {self.node_id} FAILED")

    def recover(self):
        self.status = "alive"
        print(f"Node {self.node_id} RECOVERED")