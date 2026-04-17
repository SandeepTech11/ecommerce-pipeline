
import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path


class ECommercePipeline:
    def __init__(self, db_path=None):
        if db_path is None:
            # Default: resolve relative to this file's location
            db_path = str(Path(__file__).resolve().parent.parent / 'data' / 'ecommerce.db')
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                timestamp TEXT,
                event_type TEXT,
                user_id TEXT,
                session_id TEXT,
                product_id TEXT,
                product_name TEXT,
                category TEXT,
                price REAL,
                quantity INTEGER,
                total_value REAL,
                payment_method TEXT,
                country TEXT,
                processed_at TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT,
                metric_value REAL,
                timestamp TEXT
            )
        """)

        conn.commit()
        conn.close()
        print(f"[Pipeline] Database initialized at {self.db_path}")

    def process_event(self, event):
        product = event.get("product", {})
        quantity = event.get("quantity") or 0
        price = product.get("price", 0)
        total_value = quantity * price if event["event_type"] == "purchase" else 0

        processed_event = {
            "event_id": event["event_id"],
            "timestamp": event["timestamp"],
            "event_type": event["event_type"],
            "user_id": event["user_id"],
            "session_id": event["session_id"],
            "product_id": product.get("id"),
            "product_name": product.get("name"),
            "category": product.get("category"),
            "price": price,
            "quantity": quantity,
            "total_value": total_value,
            "payment_method": event.get("payment_method"),
            "country": event.get("country"),
            "processed_at": datetime.now().isoformat()
        }

        return processed_event

    def store_event(self, processed_event):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO events
            (event_id, timestamp, event_type, user_id, session_id,
             product_id, product_name, category, price, quantity,
             total_value, payment_method, country, processed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            processed_event["event_id"],
            processed_event["timestamp"],
            processed_event["event_type"],
            processed_event["user_id"],
            processed_event["session_id"],
            processed_event["product_id"],
            processed_event["product_name"],
            processed_event["category"],
            processed_event["price"],
            processed_event["quantity"],
            processed_event["total_value"],
            processed_event["payment_method"],
            processed_event["country"],
            processed_event["processed_at"]
        ))

        conn.commit()
        conn.close()

    def get_metrics(self):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM events")
        total_events = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM events WHERE event_type='purchase'")
        total_purchases = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(total_value) FROM events WHERE event_type='purchase'")
        total_revenue = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(DISTINCT user_id) FROM events")
        unique_users = cursor.fetchone()[0]

        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM events
            WHERE event_type='purchase'
            GROUP BY category
            ORDER BY count DESC
        """)
        category_sales = cursor.fetchall()

        conn.close()

        return {
            "total_events": total_events,
            "total_purchases": total_purchases,
            "total_revenue": round(total_revenue, 2),
            "unique_users": unique_users,
            "category_sales": category_sales
        }

    def run_batch(self, events):
        for event in events:
            processed = self.process_event(event)
            self.store_event(processed)
        print(f"[Pipeline] Processed {len(events)} events")


if __name__ == "__main__":
    from data_generator import DataGenerator

    pipeline = ECommercePipeline()
    generator = DataGenerator()

    events = generator.generate_batch(20)
    pipeline.run_batch(events)

    metrics = pipeline.get_metrics()
    print("\nCurrent Metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
