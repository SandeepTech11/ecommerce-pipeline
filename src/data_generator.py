
import json
import random
import time
from datetime import datetime
from faker import Faker

fake = Faker()

PRODUCTS = [
    {"id": "PROD-001", "name": "Wireless Headphones", "category": "Electronics", "price": 79.99},
    {"id": "PROD-002", "name": "Running Shoes", "category": "Sports", "price": 129.99},
    {"id": "PROD-003", "name": "Yoga Mat", "category": "Sports", "price": 34.99},
    {"id": "PROD-004", "name": "Coffee Maker", "category": "Home", "price": 89.99},
    {"id": "PROD-005", "name": "Laptop Stand", "category": "Electronics", "price": 45.99},
    {"id": "PROD-006", "name": "Water Bottle", "category": "Sports", "price": 24.99},
    {"id": "PROD-007", "name": "Desk Lamp", "category": "Home", "price": 38.99},
    {"id": "PROD-008", "name": "Bluetooth Speaker", "category": "Electronics", "price": 59.99},
]

EVENT_TYPES = ["page_view", "add_to_cart", "purchase", "remove_from_cart"]
PAYMENT_METHODS = ["credit_card", "paypal", "debit_card", "apple_pay"]


class DataGenerator:
    def __init__(self):
        self.active_users = {}
        self.session_counter = 0

    def generate_user_id(self):
        return f"USR-{fake.uuid4()[:8].upper()}"

    def generate_session_id(self):
        self.session_counter += 1
        return f"SES-{self.session_counter:06d}"

    def generate_event(self):
        event_type = random.choices(
            EVENT_TYPES,
            weights=[60, 20, 12, 8],
            k=1
        )[0]

        product = random.choice(PRODUCTS)
        user_id = self.generate_user_id()
        session_id = self.generate_session_id()

        event = {
            "event_id": f"EVT-{fake.uuid4()[:12].upper()}",
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "session_id": session_id,
            "product": product,
            "quantity": random.randint(1, 3) if event_type in ["add_to_cart", "purchase"] else None,
            "payment_method": random.choice(PAYMENT_METHODS) if event_type == "purchase" else None,
            "user_agent": fake.user_agent(),
            "ip_address": fake.ipv4(),
            "country": fake.country_code(),
        }

        return event

    def generate_batch(self, count=10):
        return [self.generate_event() for _ in range(count)]


if __name__ == "__main__":
    generator = DataGenerator()
    print("Sample events:")
    for event in generator.generate_batch(3):
        print(json.dumps(event, indent=2))
        print("-" * 50)
