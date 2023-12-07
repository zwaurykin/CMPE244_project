# app.py

from flask import Flask, render_template, request, jsonify, url_for   
from mqtt_lsm_publish import MotorController  
app = Flask(__name__, static_url_path='/static')
motor_controller = MotorController()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run-motor', methods=['POST'])
def run_motor():
    data = request.json
    motor_controller.web_run_motor(data['angle'], data['direction'], data['frequency'], data['dutyCycle'])
    return jsonify({"message": "Motor command executed"}), 200

@app.route('/get-sensor-data', methods=['GET'])
def get_sensor_data():
    # Fetch the latest sensor data. This part depends on how you're storing/accessing this data
    sensor_data = motor_controller.read_sensor_data()  # Example call to a method to get sensor data
    return jsonify({
        "mag_x": sensor_data[4],
        "mag_y": sensor_data[5],
        "mag_z": sensor_data[6],
        "acc_x": sensor_data[0],
        "acc_y": sensor_data[1],
        "acc_z": sensor_data[2]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
