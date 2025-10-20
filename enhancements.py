"""
ChaosChain-AI Enhancements
--------------------------
Experimental features for advanced supply chain simulation.
These are non-core, safe to extend without breaking main functionality.
"""

from sklearn.ensemble import RandomForestRegressor
import numpy as np

class MLParameterOptimizer:
    """Optimize simulation parameters using machine learning."""

    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=50, random_state=42)

    def fit(self, X, y):
        """Train model to predict optimal parameters."""
        self.model.fit(X, y)

    def predict(self, X):
        """Predict optimized parameters."""
        return self.model.predict(X)


class AnomalyDetector:
    """Detect anomalies in demand or inventory patterns."""

    def __init__(self, threshold=3.0):
        self.threshold = threshold  # number of standard deviations

    def detect(self, current_value, historical_values):
        """Return True if anomaly detected, False otherwise."""
        if len(historical_values) < 2:
            return False
        mean = np.mean(historical_values)
        std = np.std(historical_values)
        if std == 0:
            return False
        z_score = abs((current_value - mean) / std)
        return z_score > self.threshold
