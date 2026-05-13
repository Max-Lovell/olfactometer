"""
Minimal repro: ETTDeviceAPI.IsConnected returns False even when the
connection is fully functional.
"""
import time
import clr  # type: ignore
clr.AddReference(r"C:\Program Files\ETTDirectControl\ETTAPI\ETTAPI.dll")
from ETTAPI import ETTDeviceAPI  # type: ignore

device = ETTDeviceAPI()
device.Connect("127.0.0.1")

# Poll IsConnected for 5 seconds — does it ever flip?
print("\nPolling IsConnected for 5s:")
for i in range(50):
    print(f"  t={i*0.1:.1f}s  IsConnected={device.IsConnected}")
    time.sleep(0.1)

# Now try actually using the connection
print("\nCalling ScanDeviceList anyway:")
try:
    devices = list(device.ScanDeviceList())
    print(f"  Got devices: {devices}")
    print(f"  IsConnected after ScanDeviceList: {device.IsConnected}")
except Exception as e:
    print(f"  Failed: {e}")

# Open and close a valve to prove the connection works
if devices:
    addr = devices[0].split(".")[0]
    print(f"\nFiring valve 1 on {addr}:")
    device.SetChannel(1, 500, addr)
    print(f"  IsConnected after SetChannel: {device.IsConnected}")
    time.sleep(1)
    device.CloseAllChannels()