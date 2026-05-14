import pandas as pd
import matplotlib.pyplot as plt


def plot_cpu_usage():

    data = pd.read_csv("data/runtime_metrics.csv")
    data.columns = data.columns.str.strip()

    latest_data = data.groupby("node_id").last()

    plt.figure(figsize=(10, 6))

    plt.bar(
        latest_data.index,
        latest_data["cpu_usage"]
    )

    plt.xlabel("Node ID")
    plt.ylabel("CPU Usage (%)")
    plt.title("CPU Usage Per Node")

    plt.grid(True)

    plt.show()


if __name__ == "__main__":

    plot_cpu_usage()