import random


class SelfHealer:

    def __init__(self, nodes, analytics):

        self.nodes = nodes
        self.analytics = analytics


    def recover_node(self, node):

        if node.status == "failed":

            print(f"♻ Recovering Node {node.node_id}")

            node.status = "alive"

            node.cpu_usage = random.uniform(15, 30)
            node.memory_usage = random.uniform(150, 300)
            node.latency = random.uniform(1, 3)

            print(f"Node {node.node_id} recovered")

            self.analytics.log_recovery(node.node_id)


    def recover_cluster(self):

        for node in self.nodes:

            if node.status == "failed":
                self.recover_node(node)