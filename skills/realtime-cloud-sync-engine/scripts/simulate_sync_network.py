#!/usr/bin/env python3
"""
simulate_sync_network.py
Simulates network latency, packet loss, and exponential backoff retry for real-time cloud sync engines.
"""

import random
import time
import sys

def simulate_network_sync(latency_ms=100, loss_rate=0.2, attempts=5):
    print(f"--- Simulating Network Sync (Latency: {latency_ms}ms, Loss Rate: {loss_rate * 100}%) ---")
    ops = [
        {"id": "task_1", "action": "UPDATE", "status": "completed"},
        {"id": "task_2", "action": "UPDATE", "status": "completed"},
        {"id": "task_3", "action": "DELETE", "status": "deleted"},
    ]

    success_count = 0
    total_retries = 0

    for op in ops:
        print(f"\nProcessing Operation [{op['action']}] for ID: {op['id']}...")
        success = False
        attempt = 0
        backoff_ms = latency_ms

        while attempt < attempts and not success:
            attempt += 1
            # Simulate latency
            time.sleep(backoff_ms / 1000.0)

            # Check for simulated packet loss
            if random.random() < loss_rate:
                print(f"  Attempt {attempt}: ❌ Network drop/timeout simulated! Triggering local rollback...")
                total_retries += 1
                backoff_ms *= 2 # Exponential backoff
            else:
                print(f"  Attempt {attempt}: ✅ Server ACK received. Sync resolved in {backoff_ms}ms.")
                success = True
                success_count += 1

        if not success:
            print(f"  Operation [{op['id']}] FAILED after {attempts} attempts. Pushed to offline persistent queue.")

    print(f"\n--- Simulation Results: {success_count}/{len(ops)} succeeded, Total Retries: {total_retries} ---")
    sys.exit(0)

if __name__ == "__main__":
    simulate_network_sync()
