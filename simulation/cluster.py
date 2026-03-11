from simulation.node import Node
from simulation.task import Task
from simulation.monitor import Monitor
from simulation.failure_injector import FailureInjector
import random


class Cluster:

    def __init__(self, num_nodes):

        self.nodes = [Node(i) for i in range(num_nodes)]
        self.task_queue = []
        self.current_node = 0
        self.monitor = Monitor(self.nodes)
        self.failure_injector = FailureInjector(self.nodes)


    def generate_tasks(self, num_tasks):

        for i in range(num_tasks):
            task = Task(i)
            self.task_queue.append(task)


    def schedule_tasks(self):

        while self.task_queue:

            # Inject random failure during simulation
            self.inject_random_failure()

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


    def monitor_system(self):

        print("\n--- System Metrics ---")
        self.monitor.collect_metrics()


    def run_simulation(self):

        self.generate_tasks(10)

        self.schedule_tasks()

        if random.random() < 0.3:
            self.random_failure()

        self.monitor_system()


    def inject_random_failure(self):

        if random.random() < 0.3:
            self.failure_injector.inject_failure()