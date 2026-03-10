from simulation.metrics import Metrics

class Monitor:
    def __init__(self, nodes):
        self.nodes = nodes

    def collect_metrics(self):
        metrics_list = []

        for node in self.nodes:
            metric = Metrics(node.node_id)
            metrics_list.append(metric)
            metric.display()

        return metrics_list