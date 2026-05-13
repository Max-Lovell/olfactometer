import time
import clr  # type: ignore
clr.AddReference(r"C:\Program Files\ETTDirectControl\ETTAPI\ETTAPI.dll")
from System import Int32, Int64, Boolean, String  # type: ignore
from ETTAPI import ETTDeviceAPI  # type: ignore

ett_device = ETTDeviceAPI()
ett_device.Connect("127.0.0.1")

# IsConnected is unreliable in this API — gate on ScanDeviceList instead.
devices = []
for _ in range(20):  # up to ~2s
    try:
        devices = list(ett_device.ScanDeviceList())
        if devices:
            break
    except Exception:
        pass
    time.sleep(0.1)

if not devices:
    raise RuntimeError(
        "Could not reach ETT Direct Control or no device found. "
        "Check it's running and the olfactometer is in PC mode."
    )

ett_device.ResetState()
print(f"Olfactometer connected: {devices[0]}")

DEVICE_ID = "0"
FLUSH_CHANNEL = 7

# Explicitly resolve the two SetChannel overloads so pythonnet can't pick the wrong one.
_set_channel_bool = ett_device.SetChannel.__overloads__[Int32, Boolean, String]
_set_channel_duration = ett_device.SetChannel.__overloads__[Int32, Int64, String]

def set_valve(valve_num, state_or_duration):
    """
    valve_num: 0 for flush, 1-6 for stimulus channels
    state_or_duration:
        True  -> open the valve, leave it open
        False -> close the valve
        int   -> open the valve for this many milliseconds, then auto-close
    """
    channel = FLUSH_CHANNEL if valve_num == 0 else valve_num
    if isinstance(state_or_duration, bool):
        _set_channel_bool(channel, state_or_duration, DEVICE_ID)
    elif isinstance(state_or_duration, int):
        _set_channel_duration(channel, state_or_duration, DEVICE_ID)
    else:
        raise TypeError(
            f"set_valve expects bool or int, got {type(state_or_duration).__name__}"
        )

def close_all_valves():
    ett_device.CloseAllChannels(DEVICE_ID)

close_all_valves()

# END EXPERIMENT ---------------------------------------------------------
try:
    ett_device.CloseAllChannels()
except Exception as e:
    print(f"Cleanup warning: {e}")

# END ROUTINE -----------------------------
# Safety net in case routine was terminated early
# close_all_valves()

# --------------------------------------
# NOTE Several ways to trigger this code below, depending on your needs.
# The frame-based close is bounded by refresh rate (~16 ms jitter at 60 Hz) and so less accurate (arguably) than option 1
# Probably always want to call close_all_valves() in End Routine.


# OPTION 1 ---------------------------------------------------------
# BEGIN ROUTINE -----------------------------
# stim_valve comes from your conditions file column (1-6)
# stim_duration_ms is e.g. 6000 for a 6-second stimulus
# set_valve(int(stim_valve), int(stim_duration_ms)


# OPTION 2 ---------------------------------------------------------
# # BEGIN ROUTINE -----------------------------
# valve_opened = False
# valve_closed = False
# # EACH FRAME -----------------------------
# if odour_image.status == STARTED and not valve_opened:
#     valve_opened = True
#     set_valve(int(stim_valve), True)  # open and hold
# if odour_image.status == FINISHED and not valve_closed:
#     valve_closed = True
#     set_valve(int(stim_valve), False)  # close


# OPTION 3 ---------------------------------------------------------
# # BEGIN ROUTINE -----------------------------
# ODOUR_TO_VALVE = {
#     "lavender": 1,
#     "rose": 2,
#     "vanilla": 3,
#     "control": 0,  # 0 → flush in our wrapper, i.e. odourless
# }
# valve_opened = False
# valve_closed = False
# this_valve = ODOUR_TO_VALVE[odour]  # `odour` from conditions file
# # EACH FRAME -----------------------------
# if odour_image.status == STARTED and not valve_opened:
#     valve_opened = True
#     set_valve(this_valve, True)
# if odour_image.status == FINISHED and not valve_closed:
#     valve_closed = True
#     set_valve(this_valve, False)


# OPTION 4 ---------------------------------------------------------
# # BEGIN ROUTINE -----------------------------
# if acqBlockLoop.thisN == 0:
#     # Block start: pulse valve 6 for 1 ms as a marker
#     set_valve(6, 1)
# # END ROUTINE -----------------------------
# if acqBlockLoop.nRemaining == 0:
#     set_valve(6, 1)  # block end marker
# close_all_valves()


# OPTION 5 ---------------------------------------------------------
# # BEGIN ROUTINE -----------------------------
# valve_opened = False
# # EACH FRAME -----------------------------
# if response_key.keys and not valve_opened:
#     valve_opened = True
#     set_valve(int(stim_valve), int(stim_duration_ms))  # auto-close variant
