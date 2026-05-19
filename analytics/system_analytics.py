class SystemAnalytics:

    def __init__(self):

        self.total_failures = 0
        self.total_recoveries = 0
        self.total_reassignments = 0

        self.event_logs = []

    # ----------------------------
    # Failure Tracking
    # ----------------------------
    def log_failure(self, node_id):

        self.total_failures += 1

        event = f"FAILURE → Node {node_id} crashed"

        self.event_logs.append(event)

    # ----------------------------
    # Recovery Tracking
    # ----------------------------
    def log_recovery(self, node_id):

        self.total_recoveries += 1

        event = f"RECOVERY → Node {node_id} recovered"

        self.event_logs.append(event)

    # ----------------------------
    # Task Reassignment Tracking
    # ----------------------------
    def log_reassignment(self, task_id, node_id):

        self.total_reassignments += 1

        event = (
            f"FAILOVER → "
            f"Task {task_id} moved to Backup Node {node_id}"
        )

        self.event_logs.append(event)

    # ----------------------------
    # System Health Score
    # ----------------------------
    def calculate_health_score(self, nodes):

        total_nodes = len(nodes)

        alive_nodes = len(
            [node for node in nodes if node.status == "alive"]
        )

        avg_cpu = (
            sum(node.cpu_usage for node in nodes)
            / total_nodes
        )

        avg_latency = (
            sum(node.latency for node in nodes)
            / total_nodes
        )

        score = (
            (alive_nodes / total_nodes) * 100
            - (avg_cpu / 2)
            - (avg_latency * 2)
        )

        return max(0, round(score, 2))

    # ----------------------------
    # Display Dashboard
    # ----------------------------
    def display_dashboard(self, nodes, risk_data):

        print("\n")
        print("=" * 50)
        print(" INTELLIGENT DISTRIBUTED SYSTEM DASHBOARD ")
        print("=" * 50)

        health_score = self.calculate_health_score(nodes)

        print(f"\nSystem Health Score : {health_score}%")

        alive_nodes = len(
            [node for node in nodes if node.status == "alive"]
        )

        failed_nodes = len(nodes) - alive_nodes

        print(f"Currently Active Nodes : {alive_nodes}")
        print(f"Currently Failed Nodes : {failed_nodes}")

        print(f"Failure Events      : {self.total_failures}")
        print(f"Recovery Operations : {self.total_recoveries}")
        print(f"Tasks Reassigned    : {self.total_reassignments}")

        # ----------------------------
        # Top Risk Nodes
        # ----------------------------
        print("\nTop Risk Nodes:")

        sorted_risks = sorted(
            risk_data.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for node_id, prob in sorted_risks[:5]:

            print(f"Node {node_id} → {prob:.2f}")

        # ----------------------------
        # Recent Events
        # ----------------------------
        print("\nRecent Events:")

        for event in self.event_logs[-5:]:

            print(f"- {event}")

        print("=" * 50)