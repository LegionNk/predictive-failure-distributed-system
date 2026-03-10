import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
data = pd.read_csv("data/metrics.csv")

# Remove spaces from column names
data.columns = data.columns.str.strip()

# Features
X = data[["cpu_usage", "memory_usage", "latency"]]

# Target
y = data["status"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)
print("Model Accuracy:", accuracy)

# Save model
joblib.dump(model, "ml/failure_model.pkl")
print("Model saved successfully")