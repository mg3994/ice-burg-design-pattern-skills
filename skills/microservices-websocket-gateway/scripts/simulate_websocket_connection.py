#!/usr/bin/env python3
"""
simulate_websocket_connection.py
Simulates a WebSocket connection with heartbeat ping-pong framing and automatic reconnection backoff.
"""

import time
import random
import sys

def simulate_websocket():
    print("--- Simulating WebSocket Microservice Gateway Connection ---")
    connected = False
    attempts = 0
    backoff = 1.0

    while attempts < 4:
        attempts += 1
        print(f"\nAttempt {attempts}: Connecting to wss://gateway.example.com/v1/stream...")
        if random.random() < 0.3:
            print(f"  ❌ Connection Refused / Timeout. Backing off for {backoff:.1f}s...")
            time.sleep(0.1)
            backoff *= 2.0
        else:
            connected = True
            print("  ✅ WebSocket Handshake Successful! Submerging event stream into streamSignal...")
            break

    if connected:
        for ping in range(1, 4):
            print(f"  💓 Heartbeat Ping {ping} -> Gateway Pong ACK received (latency: 12ms)")
            time.sleep(0.05)
        print("\n✅ Simulation Complete: Stream active and stable.")
        sys.exit(0)
    else:
        print("\n❌ Gateway unreachable after max attempts.")
        sys.exit(1)

if __name__ == "__main__":
    simulate_websocket()
