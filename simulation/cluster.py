from simulation.node import Node
from simulation.task import Task
import random

class Cluster:
    def __init__(self, num_nodes):
        self.nodes = [Node(i) for i in range(num_nodes)]
        self.task_queue = []

    def generate_tasks(self, num_tasks):
        for i in range(num_tasks):
            task = Task(i)
            self.task_queue.append(task)

    def schedule_tasks(self):
        while self.task_queue:
            task = self.task_queue.pop(0)

            alive_nodes = [n for n in self.nodes if n.status == "alive"]

            if not alive_nodes:
                print("No available nodes!")
                break

            node = min(alive_nodes, key=lambda n: n.workload)

            node.run_task(task)

    def random_failure(self):
        node = random.choice(self.nodes)
        node.fail()