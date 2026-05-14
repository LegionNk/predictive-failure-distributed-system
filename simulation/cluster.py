from simulation.node import Node
from self_healing.healer import SelfHealer
from simulation.task import Task
from simulation.monitor import Monitor
from simulation.failure_injector import FailureInjector
from prediction.predict_failure import FailurePredictor
import random


class Cluster:

    def __init__(self, num_nodes):

        self.nodes = [Node(i) for i in range(num_nodes)]
        self.task_queue = []
        self.current_node = 0
        self.monitor = Monitor(self.nodes)
        self.failure_injector = FailureInjector(self.nodes)
        self.predictor = FailurePredictor()
        self.healer = SelfHealer(self.nodes)


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

                cpu = node.cpu_usage
                memory = node.memory_usage
                latency = node.latency

                prediction, prob = self.predictor.predict(cpu, memory, latency)

                print(f"Node {node.node_id} | Failure Probability: {prob:.2f}")

                if prediction == 1:
                    print(f"→ Node {node.node_id} risky")

                    backup_node = self.get_healthy_node(node)
                    
                    if backup_node:
                        print(
                            f"Reassigning Task {task.task_id} "
                            f"to Node {backup_node.node_id}"
                        )
                        
                        backup_node.run_task(task)
                        
                    else:
                        print("No healthy nodes available")

                else:
                    node.run_task(task)

            else:
                print(f"Skipping failed Node {node.node_id}")

            self.current_node = (self.current_node + 1) % len(self.nodes)
            
    def get_healthy_node(self, exclude_node=None):

        healthy_nodes = []

        for node in self.nodes:

            if (
                node.status == "alive"
                and node.cpu_usage < 85
                and node != exclude_node
            ):
                healthy_nodes.append(node)

        if not healthy_nodes:
            return None

        best_node = min(
            healthy_nodes,
            key=lambda node: node.cpu_usage
        )

        return best_node


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
        
        self.healer.recover_cluster()


    def inject_random_failure(self):

        if random.random() < 0.3:
            self.failure_injector.inject_failure()