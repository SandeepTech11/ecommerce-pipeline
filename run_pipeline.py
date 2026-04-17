
#!/usr/bin/env python3
"""
Real-Time E-Commerce Data Pipeline

This script runs the complete pipeline:
1. Generates mock e-commerce events
2. Processes and stores them in SQLite
3. Displays metrics

Usage:
    python run_pipeline.py --mode continuous    # Run continuously generating events
    python run_pipeline.py --mode batch         # Run one batch and exit
    python run_pipeline.py --mode dashboard     # Start the dashboard server
"""

import sys
import time
import argparse
from pathlib import Path

sys.path.append('src')

from data_generator import DataGenerator
from pipeline import ECommercePipeline


def run_batch_mode(pipeline, generator, batch_size=50):
    print(f"[INFO] Generating {batch_size} events...")
    events = generator.generate_batch(batch_size)
    pipeline.run_batch(events)

    metrics = pipeline.get_metrics()
    print("\n" + "=" * 50)
    print("CURRENT METRICS")
    print("=" * 50)
    print(f"Total Events:      {metrics['total_events']}")
    print(f"Total Purchases:   {metrics['total_purchases']}")
    print(f"Total Revenue:     ${metrics['total_revenue']:,.2f}")
    print(f"Unique Users:      {metrics['unique_users']}")
    print("\nSales by Category:")
    for category, count in metrics['category_sales']:
        print(f"  {category}: {count}")
    print("=" * 50)


def run_continuous_mode(pipeline, generator, interval=2, batch_size=10):
    print("[INFO] Starting continuous mode...")
    print(f"[INFO] Generating {batch_size} events every {interval} seconds")
    print("[INFO] Press Ctrl+C to stop\n")

    try:
        while True:
            events = generator.generate_batch(batch_size)
            pipeline.run_batch(events)

            metrics = pipeline.get_metrics()
            print(f"\rEvents: {metrics['total_events']} | "
                  f"Purchases: {metrics['total_purchases']} | "
                  f"Revenue: ${metrics['total_revenue']:,.2f}", end='', flush=True)

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\n[INFO] Stopping pipeline...")
        metrics = pipeline.get_metrics()
        print("\nFinal Metrics:")
        print(f"  Total Events: {metrics['total_events']}")
        print(f"  Total Purchases: {metrics['total_purchases']}")
        print(f"  Total Revenue: ${metrics['total_revenue']:,.2f}")


def main():
    parser = argparse.ArgumentParser(description='E-Commerce Data Pipeline')
    parser.add_argument('--mode', choices=['batch', 'continuous', 'dashboard'],
                        default='batch', help='Run mode')
    parser.add_argument('--batch-size', type=int, default=50,
                        help='Number of events per batch')
    parser.add_argument('--interval', type=int, default=2,
                        help='Seconds between batches in continuous mode')

    args = parser.parse_args()

    if args.mode == 'dashboard':
        import subprocess
        import os
        os.chdir('dashboard')
        subprocess.run([sys.executable, 'app.py'])
        return

    print("=" * 60)
    print("  Real-Time E-Commerce Data Pipeline")
    print("=" * 60)
    print("\n[INIT] Initializing pipeline components...")

    generator = DataGenerator()
    pipeline = ECommercePipeline()

    print("[INIT] Pipeline ready!\n")

    if args.mode == 'batch':
        run_batch_mode(pipeline, generator, args.batch_size)
    elif args.mode == 'continuous':
        run_continuous_mode(pipeline, generator, args.interval, args.batch_size)


if __name__ == "__main__":
    main()
