# action_engine.py
class RiskLevel:
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class AdvancedActionEngine:
    def __init__(self, inventory, predictive_engine):
        self.inventory = inventory
        self.predictive = predictive_engine
        self.action_history = []

    def execute(self, risks):
        actions = []
        for risk in risks:
            rtype, level, target, score, forecast = risk
            if rtype == "demand":
                cat = target
                current = self.inventory.get_available_inventory(cat)
                safety_stock = forecast * 1.3 if forecast else 500
                order_qty = max(0, round(safety_stock - current))
                if order_qty > 0 and level >= RiskLevel.MEDIUM:
                    lead_time = self.inventory.lead_times[cat]
                    self.inventory.adjust_inventory(cat, order_qty, lead_time)
                    actions.append({'type': 'order', 'category': cat, 'quantity': order_qty})
            elif rtype in ["weather", "logistics", "supplier"]:
                actions.append({'type': rtype, 'action': f"Mitigation for {rtype}"})
        self.action_history.extend(actions)
        return actions
