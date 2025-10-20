# predictive_engine.py
import random
import math
from collections import defaultdict
import numpy as np

class AdvancedChaoticDemand:
    def __init__(self, r=3.99, x0=0.5):
        self.r = r
        self.x = x0
        self.history = []

    def next(self):
        noise = random.gauss(0, 0.01)
        self.x = self.r * self.x * (1 - self.x) + noise
        self.x = max(0.001, min(0.999, self.x))
        self.history.append(self.x)
        return max(10, self.x * 1500)

    def get_volatility(self):
        if len(self.history) < 2:
            return 0
        return np.std(self.history)

class AdvancedPredictiveEngine:
    def __init__(self, inventory, categories=None):
        if categories is None:
            categories = ["electronics", "clothing", "food", "pharmaceuticals", "automotive"]
        self.inventory = inventory
        self.categories = categories
        self.demand_models = {
            cat: AdvancedChaoticDemand(
                r=3.8 + random.random() * 0.19,
                x0=0.1 + random.random() * 0.8
            ) for cat in categories
        }
        self.risk_history = defaultdict(list)
        self.RISK_THRESHOLDS = {"LOW": 0.2, "MEDIUM": 0.4, "HIGH": 0.6, "CRITICAL": 0.8}

    def monte_carlo_demand(self, category, social_factor, simulations=200):
        results = []
        for _ in range(simulations):
            base = self.demand_models[category].next()
            influenced = base * social_factor * random.uniform(0.8, 1.2)
            results.append(influenced)
        mean = np.mean(results)
        std = np.std(results)
        ci = (mean - 1.96*std, mean + 1.96*std)
        return mean, std, ci, results

    def calculate_risk_score(self, current_inventory, forecast_demand, demand_std, volatility):
        if forecast_demand <= 0:
            return 0.0
        days_supply = current_inventory / forecast_demand
        volatility_impact = volatility * 2
        service_risk = 0.5
        if demand_std > 0:
            z_score = (0 - (current_inventory - forecast_demand)) / demand_std
            service_risk = 1 - (1 / (1 + math.exp(-z_score)))
        base_risk = 1 / (1 + math.exp(0.3 * (days_supply - 8)))
        combined = base_risk * 0.6 + service_risk * 0.3 + volatility_impact * 0.1
        return min(1.0, combined)
