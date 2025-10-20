# inventory_system.py
import random
import threading
import time
from collections import deque

class AdvancedInventorySystem:
    def __init__(self, categories=None):
        if categories is None:
            categories = ["electronics", "clothing", "food", "pharmaceuticals", "automotive"]
        self.inventory = {cat: 1200 for cat in categories}
        self.in_transit = {cat: 0 for cat in categories}
        self.lead_times = {cat: random.randint(1, 3) for cat in categories}
        self.lock = threading.Lock()
        self.order_history = []

    def adjust_inventory(self, category, amount, lead_time_cycles=1):
        with self.lock:
            if amount > 0:  # Placing order
                self.in_transit[category] += amount
                self.order_history.append({
                    'timestamp': time.time(),
                    'category': category,
                    'quantity': amount,
                    'expected_arrival': time.time() + (lead_time_cycles * 0.3)
                })
            else:  # Consuming inventory
                self.inventory[category] = max(0, self.inventory[category] + amount)

    def receive_shipments(self):
        with self.lock:
            current_time = time.time()
            for order in self.order_history[:]:
                if current_time >= order['expected_arrival']:
                    self.inventory[order['category']] += order['quantity']
                    self.in_transit[order['category']] -= order['quantity']
                    self.order_history.remove(order)

    def get_available_inventory(self, category):
        with self.lock:
            return self.inventory[category] + self.in_transit[category]

    def get_inventory_levels(self):
        with self.lock:
            return self.inventory.copy()
