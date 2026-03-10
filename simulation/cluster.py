from simulation.node import Node
import random

class Cluster:
    def __init__(self, num_nodes):
        self.nodes = [Node(i) for i in range(num_nodes)]

    def run_tasks(self):
        for node in self.nodes:
            node.run_task()

    def random_failure(self):
        node = random.choice(self.nodes)
        node.fail()

    def recover_all(self):
        for node in self.nodes:
            if node.status == "failed":
                node.recover()