import joblib
import pandas as pd


class FailurePredictor:

    def __init__(self):
        self.model = joblib.load("ml/failure_model.pkl")

    def predict(self, cpu, memory, latency):

        # Create dataframe with same feature names used in training
        data = pd.DataFrame({
            "cpu_usage": [cpu],
            "memory_usage": [memory],
            "latency": [latency]
        })

        prediction = self.model.predict(data)[0]
        probability = self.model.predict_proba(data)[0][1]

        return prediction, probability