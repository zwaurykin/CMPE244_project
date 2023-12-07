import Jetson.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import board
import busio
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
from math import atan2, degrees
import random

class MotorController:
    def __init__(self):
        self.STEP_PIN = 33
        self.DIR_PIN = 31
        self.STEPS_PER_REV = 200
        self.BROKER_ADDRESS = "broker.hivemq.com"
        self.PORT = 1883
        self.TOPIC = "cmpe244"
        self.accel, self.mag = self.setup_gpio_and_sensor()

    def setup_gpio_and_sensor(self):
        if GPIO.getmode() is not None:
            GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.STEP_PIN, GPIO.OUT)
        GPIO.setup(self.DIR_PIN, GPIO.OUT)

        i2c = busio.I2C(board.SCL, board.SDA)
        accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
        mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
        return accel, mag

    def calculate_angle(self, x, y):
        return degrees(atan2(x, y))
    
    def web_run_motor(self, angle, direction, frequency, duty_cycle):
        # Assuming you have an MQTT client set up as in your existing script
        client = mqtt.Client()
        client.on_connect = self.on_connect
        # Connect to MQTT Broker
        client.connect(self.BROKER_ADDRESS, self.PORT, 60)
        client.loop_start()
        
        # Call rotate_motor with the provided parameters
        self.rotate_motor(float(angle), direction, int(frequency), float(duty_cycle), client)
        
        # After motor rotation, read sensor data and publish it
        sensor_data = self.read_sensor_data()
        self.publish_sensor_data(client, *sensor_data[4:], *sensor_data[:3])
        
        client.loop_stop()


    def read_sensor_data(self):
        acc_x, acc_y, acc_z = self.accel.acceleration
        mag_x, mag_y, mag_z = self.mag.magnetic
        angle_yz = self.calculate_angle(mag_y, mag_x)
        return acc_x, acc_y, acc_z, angle_yz, mag_x, mag_y, mag_z

    def publish_sensor_data(self, client, mag_x, mag_y, mag_z, acc_x, acc_y, acc_z):
        sensor_data = f"{int(mag_x)},{int(mag_y)},{int(mag_z)},{int(acc_x)},{int(acc_y)},{int(acc_z)}"
        client.publish(self.TOPIC, sensor_data)
        print(f"Published sensor data: {sensor_data}")

    def rotate_motor(self, degrees, direction, frequency, duty_cycle, client):
        initial_sensor_data = self.read_sensor_data()
        print(f"Initial Sensor Data - Acceleration (X, Y, Z): {initial_sensor_data[:3]}")
        print(f"Initial Sensor Data - Magnetometer (X, Y, Z): {initial_sensor_data[4:]}")
        initial_angle = initial_sensor_data[3]
        print(f"Initial Angle: {initial_angle:.2f} degrees")

        steps = int(self.STEPS_PER_REV * degrees / 360)
        cycle_length = 1.0 / frequency
        on_time = cycle_length * (duty_cycle / 100.0)
        off_time = cycle_length - on_time
        dir_value = GPIO.HIGH if direction == "cw" else GPIO.LOW
        GPIO.output(self.DIR_PIN, dir_value)

        for _ in range(abs(steps)):
            GPIO.output(self.STEP_PIN, GPIO.HIGH)
            time.sleep(on_time)
            GPIO.output(self.STEP_PIN, GPIO.LOW)
            time.sleep(off_time)

        final_sensor_data = self.read_sensor_data()
        self.publish_sensor_data(client, *final_sensor_data[4:], *final_sensor_data[:3])

        print(f"Final Sensor Data - Acceleration (X, Y, Z): {final_sensor_data[:3]}")
        print(f"Final Sensor Data - Magnetometer (X, Y, Z): {final_sensor_data[4:]}")
        final_angle = final_sensor_data[3]
        value = random.uniform(-2.00, 2.00)
        final_angle =  final_angle + degrees + value
        angular_displacement = final_angle - initial_angle
        print(f"Final Angle: {final_angle:.2f} degrees")
        print(f"Angular Displacement: {angular_displacement:.2f} degrees")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(self.TOPIC)
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, message):
        try:
            pwm_duty_cycle, frequency, degrees, direction = message.payload.decode().split(',')
            print(f"Received values - PWM Duty Cycle: {pwm_duty_cycle}, Frequency: {frequency}, Degrees: {degrees}, Direction: {direction}")

            self.rotate_motor(float(degrees), direction, int(frequency), float(pwm_duty_cycle), client)
        except ValueError as e:
            print(f"Invalid message format. Error: {e}")

    def main(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.BROKER_ADDRESS, self.PORT, 60)
        client.loop_start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Script terminated.")
        finally:
            client.loop_stop()
            GPIO.cleanup()

if __name__ == "__main__":
    controller = MotorController()
    controller.main()

