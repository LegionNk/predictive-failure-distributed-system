import random

class FailureInjector:

    def __init__(self, nodes):
        self.nodes = nodes

    def inject_failure(self):

        node = random.choice(self.nodes)

        failure_type = random.choice([
            "node_crash",
            "cpu_overload"
        ])

        if failure_type == "node_crash":

            node.status = "failed"
            print(f"[FAILURE] Node {node.node_id} crashed")

        elif failure_type == "cpu_overload":

            node.cpu_usage = 95
            print(f"[FAILURE] CPU overload on Node {node.node_id}")