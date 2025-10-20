# advanced_control_tower.py
import threading
import logging
from collections import deque, defaultdict
from inventory_system import AdvancedInventorySystem
from predictive_engine import AdvancedPredictiveEngine
from action_engine import AdvancedActionEngine, RiskLevel

# Mock APIs for demo
class WeatherAPI:
    def forecast(self):
        return {"severity": "low"}

class SocialMediaMonitor:
    def analyze(self, categories):
        return {cat: {"factor": 1.0} for cat in categories}

class LogisticsAPI:
    def get_route(self, loc):
        return {"status": "ok"}

class SupplierAPI:
    def assess(self, supplier):
        return {"status": "ok"}

class AdvancedAIControlTower:
    def __init__(self):
        self.categories = ["electronics", "clothing", "food", "pharmaceuticals", "automotive"]
        self.inventory = AdvancedInventorySystem(self.categories)
        self.weather = WeatherAPI()
        self.social = SocialMediaMonitor()
        self.logistics = LogisticsAPI()
        self.supplier = SupplierAPI()
        self.predictive = AdvancedPredictiveEngine(self.inventory, self.categories)
        self.actions = AdvancedActionEngine(self.inventory, self.predictive)
        self.alert_queue = deque(maxlen=1000)
        self.history_inventory = defaultdict(list)
        self.history_risks = defaultdict(list)
        self.lock = threading.Lock()

    def monitor_location(self, loc):
        self.inventory.receive_shipments()
        social = self.social.analyze(self.categories)
        weather = self.weather.forecast()
        route = self.logistics.get_route(loc)
        supplier = self.supplier.assess(loc)

        # Simplified demo: generate mock risks
        risks = []
        for cat in self.categories:
            mean, std, ci, _ = self.predictive.monte_carlo_demand(cat, social[cat]["factor"])
            inv = self.inventory.get_available_inventory(cat)
            vol = self.predictive.demand_models[cat].get_volatility()
            score = self.predictive.calculate_risk_score(inv, mean, std, vol)
            level = RiskLevel.HIGH if score > 0.6 else RiskLevel.MEDIUM
            risks.append(("demand", level, cat, score, mean))

        actions = self.actions.execute(risks)

        with self.lock:
            for cat in self.categories:
                self.history_inventory[cat].append(self.inventory.get_available_inventory(cat))
                self.history_risks[cat].append(score)

        return {"location": loc, "risks": risks, "actions": actions}

    def run_cycle(self):
        threads = []
        results = []
        for loc in ["Asia", "Europe", "Americas"]:
            t = threading.Thread(target=lambda l=loc: results.append(self.monitor_location(l)))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        return results

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    tower = AdvancedAIControlTower()
    for i in range(3):
        result = tower.run_cycle()
        logging.info(f"Cycle {i+1} results: {result}")
