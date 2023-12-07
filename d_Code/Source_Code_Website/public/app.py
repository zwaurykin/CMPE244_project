# app.py

from flask import Flask, request, jsonify
from mqtt_lsm_publish import MotorController  
app = Flask(__name__)
motor_controller = MotorController()

@app.route('/run-motor', methods=['POST'])
def run_motor():
    data = request.json
    motor_controller.web_run_motor(data['angle'], data['direction'], data['frequency'], data['dutyCycle'])
    return jsonify({"message": "Motor command executed"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
