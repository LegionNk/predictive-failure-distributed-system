from simulation.metrics import Metrics


class Monitor:

    def __init__(self, nodes):
        self.nodes = nodes

    def collect_metrics(self):

        for node in self.nodes:

            metric = Metrics(
                node.node_id,
                node.cpu_usage,
                node.memory_usage,
                node.latency,
                node.status
            )

            metric.log()