# app.py
import os
from flask import Flask, request, render_template, jsonify

# --- Optional serial support (falls back to mock if unavailable) ---
try:
    import serial  # pip install pyserial
except Exception:
    serial = None

SERIAL_PORT = os.getenv("SERIAL_PORT", "COM3" if os.name == "nt" else "/dev/ttyACM0")
BAUDRATE = int(os.getenv("BAUDRATE", "115200"))
TIMEOUT = float(os.getenv("SERIAL_TIMEOUT", "1"))

_ser = None

def _get_serial():
    """Lazy-open the serial port; return None if unavailable (mock mode)."""
    global _ser
    if serial is None:
        return None
    if _ser and getattr(_ser, "is_open", False):
        return _ser
    try:
        _ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=TIMEOUT)
        return _ser
    except Exception as e:
        print(f"[WARN] Could not open serial port {SERIAL_PORT}: {e}")
        return None

def timerToPico(timerVal: int):
    """Send the timer value to the device, or mock if serial is unavailable."""
    payload = f"{timerVal}\n"
    ser_obj = _get_serial()
    if ser_obj:
        try:
            ser_obj.write(payload.encode())
            ser_obj.flush()
            return True, f"Sent '{payload.strip()}' to {SERIAL_PORT}"
        except Exception as e:
            return False, f"Serial write failed: {e}"
    else:
        # Mock mode so the web app still works without hardware
        print(f"[MOCK] Would send to serial: {payload.strip()}")
        return True, "Serial unavailable; mock send OK"

# --- Timer mappings ---
# What the user picks in the dropdown -> "work length (minutes)"
dropdown_mapping = {
    "Test": 1,
    "Short": 25,
    "Medium": 50,
    "Long": 90
}

# Work length (minutes) -> break length (minutes), Pomodoro-style
StudyTimers = {
    1: 1,
    25: 5,
    50: 10,
    90: 30
}

# --- Flask setup ---
app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    # pass the human labels so Jinja can render the dropdown
    return render_template("index.html", options=list(dropdown_mapping.keys()))

@app.route("/startTimer", methods=["POST"])
def startTimer():
    userSelect = request.form.get("timer")
    timerVal = dropdown_mapping.get(userSelect)

    if timerVal is None:
        return jsonify(ok=False, message="Please select a valid timer option."), 400

    ok, serial_msg = timerToPico(timerVal)

    workTimer = timerVal                       # Work minutes = selected value
    breakTimer = StudyTimers.get(timerVal, 0)  # Break minutes from the mapping

    return jsonify(
        ok=ok,
        message=f"Timer {timerVal} sent! Work: {workTimer} min, Break: {breakTimer} min",
        serial=serial_msg
    )

if __name__ == "__main__":
    # Run on localhost:5000
    app.run(host="127.0.0.1", port=5000, debug=True)