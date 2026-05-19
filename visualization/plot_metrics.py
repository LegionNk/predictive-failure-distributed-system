import pandas as pd
import matplotlib.pyplot as plt


def plot_dashboard():

    data = pd.read_csv("data/runtime_metrics.csv")

    latest_data = data.groupby("node_id").last()

    node_ids = latest_data.index

    cpu = latest_data["cpu_usage"]
    memory = latest_data["memory_usage"]
    latency = latest_data["latency"]

    status = latest_data["status"].apply(
        lambda x: 1 if x == "alive" else 0
    )

    plt.figure(figsize=(14, 10))

    # CPU Usage
    plt.subplot(2, 2, 1)
    plt.bar(node_ids, cpu)
    plt.title("CPU Usage")
    plt.xlabel("Node ID")
    plt.ylabel("CPU %")

    # Memory Usage
    plt.subplot(2, 2, 2)
    plt.bar(node_ids, memory)
    plt.title("Memory Usage")
    plt.xlabel("Node ID")
    plt.ylabel("Memory MB")

    # Latency
    plt.subplot(2, 2, 3)
    plt.bar(node_ids, latency)
    plt.title("Network Latency")
    plt.xlabel("Node ID")
    plt.ylabel("Latency ms")

    # Node Status
    plt.subplot(2, 2, 4)
    plt.bar(node_ids, status)
    plt.title("Node Health Status")
    plt.xlabel("Node ID")
    plt.ylabel("1 = Alive | 0 = Failed")

    plt.tight_layout()

    plt.show()


plot_dashboard()