from simulation.node import Node
from simulation.task import Task
import random

class Cluster:
    def __init__(self, num_nodes):
        self.nodes = [Node(i) for i in range(num_nodes)]
        self.task_queue = []
        self.current_node = 0

    def generate_tasks(self, num_tasks):
        for i in range(num_tasks):
            task = Task(i)
            self.task_queue.append(task)

    def schedule_tasks(self):
        while self.task_queue:
            task = self.task_queue.pop(0)

            node = self.nodes[self.current_node]

            if node.status == "alive":
                node.run_task(task)
            else:
                print(f"Skipping failed Node {node.node_id}")

            self.current_node = (self.current_node + 1) % len(self.nodes)

    def random_failure(self):
        node = random.choice(self.nodes)
        node.fail()