
dropdown_mapping = {
    "Test": 1,
    "Short": 25, 
    "Medium": 50,
    "Long": 90
}

import serial
ser = serial.Serial('COM3', 115200, timeout = 1)

def timerToPico(timerVal):
    ser.write(f"{timerVal}\n".encode())

StudyTimers = {
    1:1,
    25:5,
    50:10,
    90:30
}

from flask import Flask, request

app = Flask(__name__)

@app.route("/startTimer", methods=["POST"])
def startTimer():
    userSelect = request.form.get("timer")
    timerVal = dropdown_mapping.get(userSelect)
    if timerVal is None:
        return "Please select a timer option.", 400
    
    timerToPico(timerVal)
    workTimer = StudyTimers[timerVal]
    breakTimer = StudyTimers.get(timerVal, 0)

    return f"Timer {timerVal} sent! Work: {workTimer} min, Break: {breakTimer} min"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

