import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_autorefresh import st_autorefresh
from pathlib import Path

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Distributed System Dashboard",
    layout="wide"
)

st_autorefresh(interval=2500, key="refresh")

# =====================================================
# STYLE
# =====================================================

st.markdown(
    """
    <style>
        .main {
            background-color: #0E1117;
        }

        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 1rem;
        }

        [data-testid="metric-container"] {
            background-color: #1b2130;
            border: 1px solid #2a3142;
            border-radius: 14px;
            padding: 12px;
        }

        .small-note {
            color: #9aa4b2;
            font-size: 0.92rem;
        }

        .section-title {
            margin-top: 0.5rem;
            margin-bottom: 0.25rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# PATHS
# =====================================================

DATA_PATH = Path("data/runtime_metrics.csv")
EVENT_PATH = Path("data/system_events.log")

# =====================================================
# TITLE
# =====================================================

st.markdown(
    """
    <h1 style="text-align:center; margin-bottom: 0.2rem;">
        🖥 Intelligent Distributed System Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<p class='small-note' style='text-align:center;'>Live monitoring of failure prediction, task reassignment, and self-healing.</p>",
    unsafe_allow_html=True
)

st.markdown("---")

# =====================================================
# LOAD DATA
# =====================================================

try:
    data = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    st.error("runtime_metrics.csv not found")
    st.stop()

if data.empty:
    st.warning("No runtime data available yet.")
    st.stop()

data.columns = [
    "node_id",
    "cpu_usage",
    "memory_usage",
    "latency",
    "status"
]

for col in ["node_id", "cpu_usage", "memory_usage", "latency"]:
    data[col] = pd.to_numeric(data[col], errors="coerce")

data["status"] = data["status"].astype(str)
data = data.dropna(subset=["node_id", "cpu_usage", "memory_usage", "latency", "status"])

if data.empty:
    st.warning("Runtime data exists, but it is not in the expected format.")
    st.stop()

# =====================================================
# INFER SIMULATION CYCLES
# =====================================================

nodes_per_cycle = max(1, int(data["node_id"].nunique()))
data = data.reset_index(drop=True)
data["cycle"] = (data.index // nodes_per_cycle) + 1

current_cycle = int(data["cycle"].max())
current = data[data["cycle"] == current_cycle].copy().sort_values("node_id")

cycle_summary = (
    data.groupby("cycle", as_index=False)
    .agg(
        avg_cpu=("cpu_usage", "mean"),
        avg_latency=("latency", "mean"),
        failed_nodes=("status", lambda s: (s == "failed").sum()),
        risky_nodes=("cpu_usage", lambda s: (s > 85).sum()),
    )
)

# =====================================================
# LOAD EVENTS
# =====================================================

events = []
if EVENT_PATH.exists():
    try:
        events = [
            line.strip()
            for line in EVENT_PATH.read_text(encoding="utf-8", errors="ignore").splitlines()
            if line.strip()
        ]
    except Exception:
        events = []

latest_events = events[-8:] if events else []

failure_events = sum("FAILURE" in e for e in events)
recovery_events = sum("RECOVERY" in e for e in events)
failover_events = sum("FAILOVER" in e for e in events)

# =====================================================
# CURRENT METRICS
# =====================================================

healthy_nodes = int((current["status"] == "alive").sum())
failed_nodes = int((current["status"] == "failed").sum())

avg_cpu = round(current["cpu_usage"].mean(), 2)
avg_latency = round(current["latency"].mean(), 2)

health_score = round((healthy_nodes / len(current)) * 100, 2) if len(current) else 0
critical_nodes = current[(current["status"] == "failed") | (current["cpu_usage"] > 85)].copy()

# =====================================================
# OVERVIEW CARDS
# =====================================================

st.subheader("📊 System Overview")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Current Cycle", current_cycle)
c2.metric("System Health", f"{health_score}%")
c3.metric("Healthy Nodes", healthy_nodes)
c4.metric("Failed Nodes", failed_nodes)
c5.metric("Task Migrations", failover_events)

st.caption(
    f"Average CPU: {avg_cpu}%  |  Average Latency: {avg_latency} ms  |  "
    f"Failure Events: {failure_events}  |  Recovery Events: {recovery_events}"
)

st.markdown("---")

# =====================================================
# LAYOUT
# =====================================================

left_col, right_col = st.columns([2.0, 1.0])

# =====================================================
# LEFT SIDE: INTERACTIVE GRAPHS
# =====================================================

with left_col:
    st.subheader("📈 Live Cycle Trend")

    trend_fig = make_subplots(specs=[[{"secondary_y": True}]])

    trend_fig.add_trace(
        go.Scatter(
            x=cycle_summary["cycle"],
            y=cycle_summary["avg_cpu"],
            name="Average CPU",
            mode="lines+markers",
            line=dict(width=3, color="#4dabf7"),
            hovertemplate="Cycle %{x}<br>Avg CPU: %{y:.2f}%<extra></extra>"
        ),
        secondary_y=False
    )

    trend_fig.add_trace(
        go.Scatter(
            x=cycle_summary["cycle"],
            y=cycle_summary["avg_latency"],
            name="Average Latency",
            mode="lines+markers",
            line=dict(width=3, color="#f59f00"),
            hovertemplate="Cycle %{x}<br>Avg Latency: %{y:.2f} ms<extra></extra>"
        ),
        secondary_y=True
    )

    trend_fig.update_layout(
        template="plotly_dark",
        height=360,
        margin=dict(l=20, r=20, t=25, b=20),
        legend=dict(orientation="h"),
        hovermode="x unified",
    )
    trend_fig.update_xaxes(title_text="Simulation Cycle")
    trend_fig.update_yaxes(title_text="Average CPU (%)", secondary_y=False)
    trend_fig.update_yaxes(title_text="Average Latency (ms)", secondary_y=True)

    st.plotly_chart(trend_fig, use_container_width=True)

    st.subheader("🫧 Current Cycle Node Load")

    bubble_fig = px.scatter(
        current,
        x="cpu_usage",
        y="latency",
        size="memory_usage",
        color="status",
        hover_name="node_id",
        size_max=35,
        color_discrete_map={
            "alive": "#2ca02c",
            "failed": "#d62728"
        },
        labels={
            "cpu_usage": "CPU Usage (%)",
            "latency": "Latency (ms)",
            "memory_usage": "Memory (MB)",
            "status": "Status"
        },
        title="Node Load vs Latency"
    )

    bubble_fig.update_traces(
        hovertemplate=(
            "Node %{hovertext}<br>"
            "CPU: %{x:.2f}%<br>"
            "Latency: %{y:.2f} ms<extra></extra>"
        )
    )

    bubble_fig.update_layout(
        template="plotly_dark",
        height=420,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    st.plotly_chart(bubble_fig, use_container_width=True)

# =====================================================
# RIGHT SIDE: EXPLANATION + EVENTS
# =====================================================

with right_col:
    st.subheader("🧭 System Flow")

    flow_dot = """
    digraph G {
        rankdir=LR;
        bgcolor="transparent";

        node [shape=box, style="rounded,filled", fontname="Arial", fontsize=11, color="#4dabf7", fontcolor="white", fillcolor="#1b2130"];
        edge [color="#9aa4b2"];

        Simulation [label="Simulation Engine"];
        Monitoring [label="Monitoring"];
        Prediction [label="Failure Prediction"];
        Failover [label="Task Reassignment"];
        Healing [label="Self-Healing"];
        Metrics [label="Runtime Metrics + Events"];

        Simulation -> Monitoring -> Prediction -> Failover -> Healing -> Metrics;
    }
    """
    st.graphviz_chart(flow_dot)

    st.markdown("---")

    st.subheader("📡 Recent Events")

    if latest_events:
        for event in reversed(latest_events):
            if "FAILURE" in event:
                st.error(event)
            elif "RECOVERY" in event:
                st.success(event)
            elif "FAILOVER" in event:
                st.warning(event)
            else:
                st.info(event)
    else:
        st.info("No system events yet")

    st.markdown("---")

    st.subheader("⚡ Current Cycle Summary")

    col_a, col_b = st.columns(2)
    col_a.metric("Risky Nodes", int((current["cpu_usage"] > 85).sum()))
    col_b.metric("Critical Nodes", len(critical_nodes))

    st.progress(min(max(health_score / 100, 0), 1.0))
    st.caption("Health score based on currently active nodes.")

    if len(critical_nodes) == 0:
        st.success("No critical nodes in the current cycle.")
    else:
        critical_nodes = critical_nodes.sort_values("cpu_usage", ascending=False)
        for _, row in critical_nodes.head(4).iterrows():
            if row["status"] == "failed":
                st.error(f"Node {int(row['node_id'])} has failed")
            else:
                st.warning(
                    f"Node {int(row['node_id'])} overloaded "
                    f"({row['cpu_usage']:.2f}% CPU)"
                )

# =====================================================
# BOTTOM: COMPACT SNAPSHOT
# =====================================================

st.markdown("---")

st.subheader("📋 Current Cycle Snapshot")

snapshot = current.copy()
snapshot["cpu_usage"] = snapshot["cpu_usage"].round(2)
snapshot["memory_usage"] = snapshot["memory_usage"].round(2)
snapshot["latency"] = snapshot["latency"].round(2)

snapshot["state"] = snapshot.apply(
    lambda r: "🔴 Failed" if r["status"] == "failed"
    else ("🟠 Risky" if r["cpu_usage"] > 85 else "🟢 Active"),
    axis=1
)

snapshot = snapshot[[
    "node_id",
    "state",
    "cpu_usage",
    "memory_usage",
    "latency"
]]

st.dataframe(
    snapshot,
    use_container_width=True,
    height=280
)