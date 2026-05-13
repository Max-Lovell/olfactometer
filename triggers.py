"""
Hardware triggers via pyxid2 (Cedrus) and pyserial — usage examples
====================================================================

Two ways to send TTL/event markers from PsychoPy:

  1. pyxid2 — Cedrus C-POD / StimTracker / Lumina response pads.
     Bitmask-based; each "line" is a bit (1, 2, 4, 8, 16, ...).
     Lines can be held open and cleared manually.

  2. pyserial — generic serial port. Any device that accepts byte
     codes over RS-232/USB-serial (most EEG systems, BIOPAC, etc.).
     You send a byte; what it means is up to the receiving device.

Install:
    pip install pyxid2 pyserial
"""

import sys
import time
from unittest.mock import MagicMock


# =====================================================================
# PART 1: pyxid2 (Cedrus devices)
# =====================================================================

# Stub out pyxid2 if it's not installed — lets the script run on any
# machine for development. Remove this block in production.
if "pyxid2" not in sys.modules:
    sys.modules["pyxid2"] = MagicMock()

import pyxid2  # type: ignore

# --- Connect ---
xid_devices = pyxid2.get_xid_devices()
if not xid_devices:
    raise RuntimeError("No Cedrus XID devices found. Is it plugged in and powered?")

xid = xid_devices[0]
print(f"Connected to: {xid}")

# pulse_duration controls auto-clear behaviour:
#   0   -> line stays active until you call clear_line
#   N>0 -> line auto-clears after N milliseconds
xid.set_pulse_duration(0)

# Start clean — bitmask=0 closes all lines
xid.clear_line(bitmask=0)

# --- Helpers ---
def xid_pulse(line, duration_ms=10):
    """Open a line for duration_ms, then close it. Blocking via core.wait."""
    from psychopy import core
    xid.activate_line(line)
    core.wait(duration_ms / 1000.0)
    xid.clear_line(line)

def xid_open(line, leave_others=True):
    """Open a line and leave it open until cleared."""
    xid.activate_line(line, leave_remaining_lines=leave_others)

def xid_close(line, leave_others=True):
    """Close a single line."""
    xid.clear_line(line, leave_remaining_lines=leave_others)

def xid_close_all():
    xid.clear_line(bitmask=0)


# =====================================================================
# PART 2: pyserial (generic serial-port triggers)
# =====================================================================

import serial  # type: ignore

# --- Connect ---
# COM port name depends on your machine — check Device Manager on Windows
# or `ls /dev/tty.*` on Mac/Linux. Common values: "COM3", "/dev/ttyUSB0".
SERIAL_PORT = "COM3"
BAUD_RATE = 115200  # match whatever the receiving device expects

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(0.5)  # some devices need a moment after the port opens
    print(f"Serial port {SERIAL_PORT} open at {BAUD_RATE} baud")
except serial.SerialException as e:
    raise RuntimeError(f"Could not open serial port {SERIAL_PORT}: {e}")

# --- Helpers ---
def serial_send(code):
    """
    Send a single byte (0-255) as a trigger code.
    Most EEG amplifiers reading parallel/serial triggers expect a byte.
    """
    if not 0 <= code <= 255:
        raise ValueError(f"Trigger code must be 0-255, got {code}")
    ser.write(bytes([code]))
    ser.flush()  # ensure it actually goes out now, not when buffer fills


# =====================================================================
# USAGE PATTERNS IN PSYCHOPY ROUTINES
# =====================================================================
#
# The same patterns you used for line-based triggers in your existing
# code carry over directly. Examples below assume these are pasted
# into a Code Component in the relevant tab.
#
# ----------------------------------------------------------------------
# PATTERN A: Event-marker pulse at routine start
# ----------------------------------------------------------------------
# Begin Routine:
#
#     if trial_loop.thisN == 0:
#         xid_pulse(1, duration_ms=10)   # block-start marker
#         serial_send(254)               # same idea via serial
#
# ----------------------------------------------------------------------
# PATTERN B: Open a line when a stimulus appears, close when it ends
# ----------------------------------------------------------------------
# Begin Routine:
#
#     stim_marked_on = False
#     stim_marked_off = False
#
# Each Frame:
#
#     if stim_image.status == STARTED and not stim_marked_on:
#         stim_marked_on = True
#         xid_open(2)
#         serial_send(10)  # "stimulus on" code
#
#     if stim_image.status == FINISHED and not stim_marked_off:
#         stim_marked_off = True
#         xid_close(2)
#         serial_send(11)  # "stimulus off" code
#
# End Routine:
#
#     xid_close_all()  # safety net
#
# ----------------------------------------------------------------------
# PATTERN C: Condition-dependent codes
# ----------------------------------------------------------------------
# Trigger codes per stimulus type, looked up from the conditions file:
#
# Begin Routine:
#
#     STIM_CODES = {
#         "Hexagon": 3,
#         "Circle":  4,
#         "Face1":   5,
#         "Face2":   6,
#     }
#     this_code = STIM_CODES[stim_shape]   # column from conditions
#     stim_marked_on = False
#
# Each Frame:
#
#     if stim_image.status == STARTED and not stim_marked_on:
#         stim_marked_on = True
#         xid_open(this_code)
#         serial_send(this_code)
#
# End Routine:
#
#     xid_close_all()
#
# ----------------------------------------------------------------------
# PATTERN D: Sound-onset marker (your aversive sound example)
# ----------------------------------------------------------------------
# Begin Routine:
#
#     sound_marked = False
#
# Each Frame:
#
#     if aversive_sound.isPlaying and not sound_marked:
#         sound_marked = True
#         xid_open(7)
#         serial_send(100)
#
# End Routine:
#
#     xid_close(7)
#     serial_send(101)  # sound-off marker
#
# =====================================================================
# CLEANUP (End Experiment tab)
# =====================================================================
#
#     try:
#         xid_close_all()
#     except Exception as e:
#         print(f"XID cleanup warning: {e}")
#
#     try:
#         ser.close()
#     except Exception as e:
#         print(f"Serial cleanup warning: {e}")