class SelfHealer:

    def __init__(self, nodes):
        self.nodes = nodes


    def recover_node(self, node):

        if node.status == "failed":

            print(f"♻ Recovering Node {node.node_id}")

            node.status = "alive"

            node.cpu_usage = 20
            node.memory_usage = 200
            node.latency = 2

            print(f"Node {node.node_id} recovered")


    def recover_cluster(self):

        for node in self.nodes:

            if node.status == "failed":
                self.recover_node(node)