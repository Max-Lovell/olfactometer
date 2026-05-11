"""
ETT Olfactometer S - Python Smoke Test
=======================================

Connects to the ETT Olfactometer S via the ETTAPI.dll (through ETT Direct Control)
and fires each stimulus valve in sequence to verify hardware communication.

Prerequisites:
    - ETT Direct Control must be running and connected to the olfactometer
    - The olfactometer must be in PC mode (PC LED lit on front panel)
    - The air pump must be on
    - pythonnet must be installed in this environment (pip install pythonnet)

Usage:
    python ett_smoketest.py
"""

import time
import clr  # type: ignore  (Pylance can't see into .NET DLLs — safe to ignore)

# Load the ETT API DLL - adjust path if your install location differs
clr.AddReference(r"C:\Program Files\ETTDirectControl\ETTAPI\ETTAPI.dll") # TODO: ADJUST PATH HERE
from ETTAPI import ETTDeviceAPI  # type: ignore


def connect_to_olfactometer(timeout_seconds=1):
    """
    Connect to ETT Direct Control and find the olfactometer.
    Returns (ett_device, address) or raises SystemExit on failure.
    """
    ett_device = ETTDeviceAPI()
    ett_device.Connect("127.0.0.1")
    time.sleep(timeout_seconds)

    print(f"IsConnected reports: {ett_device.IsConnected}")

    # IsConnected can be unreliable as a gate - try scanning regardless
    try:
        ett_device.ResetState()
    except Exception as e:
        print(f"ResetState failed (may be okay): {e}")

    try:
        found_devices = ett_device.ScanDeviceList()
        print(f"Device list: {list(found_devices)}")
    except Exception as e:
        print(f"ScanDeviceList failed: {e}")
        print("Is ETT Direct Control running and connected to the device?")
        raise SystemExit(1)

    address = ""
    for entry in found_devices:
        print(f"  Found device: {entry}")
        parts = entry.split(".")
        if len(parts) > 1 and "Olfactometer" in parts[1]:
            address = parts[0]
            print(f"  -> Olfactometer address: {address}")
            break

    if not address:
        print("No olfactometer found in device list.")
        print("Check: is the device powered on, in PC mode, and connected via USB?")
        raise SystemExit(1)

    return ett_device, address


def test_all_valves(ett_device, address, valve_count=6, duration_ms=2000, gap_seconds=2.5):
    """
    Open each valve in sequence for the given duration.
    Watch the Carrier flow column on the front panel - it should rise
    each time a valve opens.
    """
    ett_device.CloseAllChannels()
    time.sleep(1)

    print(f"\n--- Testing {valve_count} valves, {duration_ms} ms each ---\n")

    for valve_num in range(1, valve_count + 1):
        t = time.perf_counter()
        print(f"[{t:.4f}] Opening valve {valve_num} for {duration_ms} ms")
        ett_device.SetChannel(valve_num, duration_ms, address)
        time.sleep(gap_seconds)

    ett_device.CloseAllChannels()
    print("\nAll valves tested. Done.")


def print_api_methods(ett_device):
    """
    Print all available methods on the ETTDeviceAPI object.
    Useful for exploring what else the API can do (trigger out, respiration, etc.)
    """
    print("\n--- Available API methods ---\n")
    methods = [m for m in dir(ett_device) if not m.startswith("_")]
    for m in methods:
        print(f"  {m}")
    print()


def main():
    print("ETT Olfactometer S - Smoke Test")
    print("=" * 40)

    ett_device, address = connect_to_olfactometer()

    # Test all 6 stimulus valves
    test_all_valves(ett_device, address, valve_count=6, duration_ms=2000)

    # Uncomment the next line to see all available API methods:
    # print_api_methods(ett_device)


if __name__ == "__main__":
    main()