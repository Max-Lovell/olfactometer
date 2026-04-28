"""
ETT Olfactometer S - API Explorer
==================================

Connects to the olfactometer and prints all available methods on the
ETTDeviceAPI object. Useful for discovering trigger, respiration, and
other capabilities beyond basic valve control.

Usage:
    python ett_explore_api.py
"""

import time
import clr  # type: ignore
clr.AddReference(r"C:\Program Files\ETTDirectControl\ETTAPI\ETTAPI.dll")
from ETTAPI import ETTDeviceAPI  # type: ignore


def connect_to_olfactometer(timeout_seconds=5):
    """Connect and return (ett_device, address)."""
    ett_device = ETTDeviceAPI()
    ett_device.Connect("127.0.0.1")
    time.sleep(timeout_seconds)

    try:
        ett_device.ResetState()
        found_devices = ett_device.ScanDeviceList()
    except Exception as e:
        print(f"Connection failed: {e}")
        raise SystemExit(1)

    address = ""
    for entry in found_devices:
        parts = entry.split(".")
        if len(parts) > 1 and "Olfactometer" in parts[1]:
            address = parts[0]
            break

    if not address:
        print("No olfactometer found")
        raise SystemExit(1)

    print(f"Connected to olfactometer at: {address}")
    return ett_device, address


def explore_api(ett_device):
    """Print all public methods and properties on the device object."""
    print("\n" + "=" * 50)
    print("ETTDeviceAPI - Available Members")
    print("=" * 50)

    members = sorted([m for m in dir(ett_device) if not m.startswith("_")])

    for m in members:
        try:
            attr = getattr(ett_device, m)
            kind = "method" if callable(attr) else "property"
            print(f"  [{kind:8s}]  {m}")
        except Exception:
            print(f"  [unknown ]  {m}")

    print(f"\nTotal: {len(members)} members")
    print("\nLook for methods containing: Trigger, Respiration, Inhalation,")
    print("Subscribe, DIN, EEG, Channel, Valve, Flow, Connect")


def test_respiration_subscribe(ett_device):
    """
    Try to subscribe to inhalation events.
    This is how you'd get respiration-locked stimulus delivery in Python.
    """
    print("\n--- Testing respiration subscription ---\n")
    try:
        ett_device.SubscribeToInhalationEvents(True, True)
        print("SubscribeToInhalationEvents(True, True) — success")
        print("(Set respiration to 'Simulated' in ETT Direct Control Manual Mode")
        print(" if no belt is connected, to generate synthetic events)")
    except Exception as e:
        print(f"SubscribeToInhalationEvents failed: {e}")
        print("This may require respiration to be enabled in ETT Direct Control first.")


def main():
    ett_device, _address = connect_to_olfactometer()
    explore_api(ett_device)
    test_respiration_subscribe(ett_device)


if __name__ == "__main__":
    main()