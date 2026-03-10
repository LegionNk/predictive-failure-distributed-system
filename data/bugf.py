import pandas as pd

data = pd.read_csv("data/metrics.csv")
data.columns = data.columns.str.strip()

print(data["status"].value_counts())