import random
import time

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.status = "alive"

    def run_task(self):
        if self.status == "alive":
            print(f"Node {self.node_id} is running a task")
            time.sleep(random.uniform(0.5, 1.5))
        else:
            print(f"Node {self.node_id} is down and cannot run tasks")

    def fail(self):
        self.status = "failed"
        print(f"Node {self.node_id} has FAILED")

    def recover(self):
        self.status = "alive"
        print(f"Node {self.node_id} has RECOVERED")