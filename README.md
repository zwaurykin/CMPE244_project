***CMPE 244-Embedded Software- Semester long Project - MOBILE APP CONTROLLED STEPPER MOTOR with JETSON NANO


*Overview*
This repository contains the source code and documentation for an embedded system project aimed at designing a robust and efficient control system using the Jetson Nano platform to precisely drive a NEMA 17 stepper motor and calibrate it with the LSM303 sensor for applications requiring accurate positioning and motion control. 
Additionally, it involves developing a webserver with Chat-GPT integration and an Android app for remote control.

Project Structure:
/a_Summary_report: Holds project-related documentation, including requirements, system design, and user manuals.
/b_project_presentation: Contains presentation materials used to showcase the project.
/c_video_clip: Demo video clip of the project
/d_Code/: Contains the source code for the Jetson Nano application, including Python scripts for motor control, sensor calibration, and webserver integration.
/d_Code/Source_Code_ChatGPT: Contains the source code for the test and train models
/d_code/Source_Code_Website: Contains source cide for the website
/d_Code/android_app: Houses the Android app code developed for controlling the stepper motor and receiving sensor data.
/e_readme: Readme file


Setup and Installation

Hardware Requirements:
Jetson Nano Developer Kit
NEMA 17 Stepper Motor
Motor Driver (e.g., DRV8825 or A4988)
Power Supply for Jetson Nano and Stepper Motor
Wi-Fi Module (if not built into the Jetson Nano)
Feedback Sensors (optional)
Breadboard, Jumper Wires, Heat Sinks, and Fans for prototyping
Android Device for remote control

Software Requirements:
Jet Pack SDK for Jetson Nano
Python or C++ for application development on Jetson Nano
Android Studio for the Android app development
MQTT or WebSocket for real-time communication
PWM Libraries for stepper motor control
Git for version control and collaboration

Usage

Running the System:

Ensure all hardware components are connected properly based on the schematic provided in /documentation.
Upload the necessary scripts to the Jetson Nano and ensure they are executed in the correct order for system initialization.
Install the Android app on the mobile device and establish a connection with the Jetson Nano through Wi-Fi.
Use the app interface to control the motor angle, rotation direction, frequency, and duty cycle.
Monitor sensor data on the app received from the Jetson Nano's webserver.

Testing
Test Scripts:

d_Code/Source_Code_ChatGPT/: Ensure LSM303 sensor readings are accurately received and processed.
d_Code/Source_Code_Webserver/: Validate the wireless communication between the Jetson Nano and Android app.
d_Code/Source_Code_Website/: 

d_Code/Source_Code_AndroidApp/activity_main.xml: Android app layout file.
d_Code/Source_Code_AndroidApp/MainActivity.java: Android app layout file.

Unit Tests:
Unit tests for individual components can be found in the respective directories within /src.
Troubleshooting
In case of any issues, refer to the troubleshooting section in the user manual provided in /documentation.
Check hardware connections, power supply, and ensure software scripts are running without errors.

Contributors:
Prabhat Kumar (prabhat.kumar@sjsu.edu)
Sindhuja Ravi(sindhuja.ravi@sjsu.edu)

Acknowledgements
Special thanks to Dr. Harry Li for the guidance and support throughout this project.