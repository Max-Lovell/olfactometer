# ETT Olfactometer S — Setup

Download the manuals from here: https://emergingtechtrans.com/support.php, contact ETT support at support@emergingtechtrans.com

## Hardware
1. Turn on the device and air pumps using switches on front and connect USB from the 'PC CONTROL' port on the device to the PC. 
2. Press the MANUAL/PC button on the front panel so "PC" LED is light up - lets you control device from computer, but the actual buttons on the device won't work if 'manual' light is off. 

SOME BROKEN STUFF:
1. Some of the buttons on the machine to open valves don't work, but they can be controlled by PC. 
2. Valve 3 is broken (I think).
3. The respiration belt is broken and the inner plastic pouch needs replacing. Should be cheap.

NOTES:
- There is a BNC port on the front that we probably won't use. It can be used to send a pulse out when a valve opens to a biopac or EEG recording device. USB should be enough here, however. 
  - You will want to get your hands on one of these: https://www.blackboxtoolkit.com/usbttl.html

### Tubes
1. Plug the respiration belt tube into the front (when we get one that actually works!)
2. The big bundle of several tubes in their own box are for delivering the air from out the back of the olfactometer to the jars. 
Connect tubing to back of the device paying attention to the numbers on each tube and each nozzle. 
The nozzles have a piece of plastic on the end which is a (fiddly) 'quick release' mechanism that needs to be pushed in slightly.
Make sure tubes aren't bent.
3. Screw odorant bottles into the big flat plastic 'carrier'. Every slot MUST have a bottle to have any pressure in the system.
4. There's also a smaller single transparent tube ('PTFE delivery tube') to attach to the 'output' nozzle of the carrier.
5. The adjustable plastic straw things are 'Loc-line' connectors - the tubes don't go in these, but are attached to the outside of them, so the transparent tube can sit under the participant's nose.

### Pressure
The front panel has two tubes with metal balls and dials below them:
- 'Air Flow' dial — total system air flow
- Flush: This always has pressure continuously as odorless baseline air.
- Carrier: air flows through whichever stimulus valve is open (through the
  odorant bottle). Only flows when a stimulus valve is active.

Set the valves to about 6 L/min on both columns. The carrier valve's pressure should change to when you open and close valves.

There's also a separate plastic encased tube with a metal ball inside that can be used to test air pressure on the output delivery tube.

---

## Software
You must run ETT Direct Control to use the device (including using APIs). 
Direct Control can be used to create entire experiments, or can be triggered through APIs (so you can control the device with code) in MATLAB, Eprime and Python. 
So far I've only tested the Python one, which will work with PsychoPy. 

Note I've seen DC being quite buggy, but we're stuck with it for now. Often nees to be shutdown and reopened.

### ETT Direct Control
#### install
1. Download it from here: https://emergingtechtrans.com/support.php 
2. Run as Administrator (required for USB drivers).
3. During install, ensure both prerequisites are checked:
   - Microsoft .NET Framework 4
   - FTDI USB drivers
4. After install, launch ETT Direct Control as Administrator if needed).
5. The olfactometer should appear in the 'Manual Mode' tab as
   "ETT Olfactometer S - Connection state: Connected".

If the device isn't recognised, try rebooting the PC.

#### Usage
#### Manual Mode
  - Click each valve button and flush button. Should be able to feel pressure or smell through appropriate tube, see/feel changes in air pressure
  - 'Respiration': can click this to 'Enabled' when we have a working belt.
    - For now click twice to switch to 'simulated' which will fake breathing signal. NOTE I think this feature is broken? Seems to only work for a minute or so...

#### Paradigm Designer
- You could make the entire experiment using the Paradigm Designer. 
- Or, the "External TTL Triggered Start" allows you to use the API to send a start signal. 
- You could also just make small 'groups' of behaviour (e.g. opening a valve) in ETT DC and trigger those with the API. 

Note one thing we probably want is to delay sending the smells until an inhalation has occurred. 
Direct Control has a "Delay onset until" -> "respiratoryAnalogInhalationOnset" option for this.
The python API has something like `device.SubscribeToInhalationEvents(True, True)` and then you need to attach a function to the `device.InhalationDetected` method - can be tricky.

#### APIs
- APIs and their documentation/examples are included with ETT Direct Control: `C:\Program Files\ETTDirectControl\ETTAPI`.
- Try go to 'file:///C:/Program%20Files/ETTDirectControl/ETTAPI/AutoDoc/index.html#CSharpClass:ETTAPI.ETTDeviceAPI' in your browser, might work. You can see sample code for python and MATLAB there.

### Python API
If you want to test things out these Python scripts will run through the valves automatically. 
The code here will also help with running the experiment in PsychoPy.

1. Prerequisites: Install Python from [www.python.org/downloads](www.python.org/downloads) (any recent version — this just gets you the `py` launcher). Then double-click setup.bat — it will install Python 3.12 automatically if needed. Note read the install options carefully, and you MUST click 'Add to PATH' when prompted. Also can try running `py install 3.12` yourself.
2. You can code python in VSCode, but I recommend PyCharm instead, which is free for students. It helps with the venv stuff next.
3. To run the python scripts included here it's best to use a 'virtual environment' - double click `setup.bat` to create one (`ett-venv`)
4. If not running `setup.bat` or if in PsychoPy, install the `pythonnet` package.
5. You'll know you're in the 'venv' if your terminal is prepended with `ett-venv>`. If your IDE doesn't detect it automatically:
    - VsCode: Ctrl+Shift+P, type "Python: Select Interpreter", choose ett-venv (something like \ett-venv\Scripts\python.exe).
    - PyCharm: File>Settings>Project>Python Interpreter>gear icon>Add>Existing Environment>ett-venv\Scripts\python.exe.

Test scripts included:
Test scripts included:
- `test.py` — runs through triggering each valve in sequence. Use this
  first to confirm hardware communication. You might need to change the
  path `C:\Program Files\ETTDirectControl\ETTAPI\ETTAPI.dll` inside the
  script if your install location differs.
- `api.py` — prints all public methods on the ETTDeviceAPI object.
  Useful for discovering what the API can do beyond basic valve control
  (trigger out, respiration subscription, etc.).
- `sebastian.py` — ETT's official Python sample, lightly annotated.
  Demonstrates the `__overloads__` pattern for explicitly resolving
  the bool vs. duration variants of `SetChannel`.
- `psychopy.py` — minimal connection + helper functions
  (`set_valve`, `close_all_valves`) ready to paste into a PsychoPy
  Builder Code Component. Handles the `IsConnected` quirk (see below)
  and uses explicit overload resolution so both `set_valve(2, True)`
  (manual open) and `set_valve(2, 6000)` (open with auto-close) work
  unambiguously.
- `triggers.py` — examples of sending event markers via pyxid2
  (Cedrus devices) and pyserial (generic serial-port triggers).
  Independent of the olfactometer; included for reference when adding
  EEG/biopac markers to a PsychoPy experiment.
- `isconnected_bug.py` — minimal repro for a quirk in the ETT API:
  `device.IsConnected` returns `False` even when the connection is
  fully working. Run this to confirm before contacting ETT support,
  or just read it to understand why `psychopy.py` gates on
  `ScanDeviceList()` rather than `IsConnected`.
- `setup.bat` — installs Python 3.12 if needed and creates the
  `ett-venv` virtual environment with `pythonnet` installed.
- `repo-structure.txt` — text dump of the repo layout for reference.

You can run any of the test scripts by activating the venv and running
e.g. `python test.py` in your terminal, or by clicking 'play' in your
IDE. ETT Direct Control must be running first in all cases.