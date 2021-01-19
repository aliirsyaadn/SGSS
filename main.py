import paho.mqtt.client as mqtt
import json
import time
import serial
from ObjectDetection import *

# Serial Initialization
ser = serial.Serial('/dev/ttyACM0', 9600) # Change into your Arduino Port

# Declare variable to connect to Thingsboard
broker = "demo.thingsboard.io"
port = 1883
username = "ixrN3vNdkHnpGmXYDic8" # Change into your user id in thingsboard
password = ""
topic = "v1/devices/me/telemetry"

# Connect to thingsboard
client = mqtt.Client()
client.username_pw_set(username, password)
client.connect(broker, port)
print("Connection Establish..")

# Main Program
dataUltra = {}
dataMag = {}
dataRfid = {}
dataPir = {}
dataCam = {}
while True:
	if(ser.in_waiting > 0):
		data = ser.readline().decode().split()
		if data[0] == "U":
			if int(data[1]) < 200 :
				print(f"Ultrasonic {data[1]}")
				dataUltra["Ultrasonic"] = data[1]
				if int(data[1]) < 100 and dataMag["Magnetic Switch"] == "Closed":
					detected = capturePhoto()
					if detected:
						dataCam["Camera"] = "Person Detected"
						print(f"Camera {dataCam['Camera']}")
						client.publish(topic, json.dumps(dataCam))
				client.publish(topic, json.dumps(dataUltra))
		elif data[0] == "M":
			status = "Opened" if data[1] == "1" else "Closed"
			print(f"Magnetic {status}")
			dataMag["Magnetic Switch"] = status
			client.publish(topic, json.dumps(dataMag))
		elif data[0] == "R":
			status = ""
			if data[1] == "0" :
				status = f"Unauthenticated User ID {data[2]}"
			elif data[1] == "1":
				status = f"Authenticated User {data[2]}"
			print(f"RFID {status}")
			dataRfid["RFID"] = status
			client.publish(topic, json.dumps(dataRfid))
		elif data[0] == "P":
			status = "Motion Detected" if data[1] == "1" else "Motion Ended"
			print(f"PIR {status}")
			dataPir["PIR"] = status
			if int(data[1]):
				detected = capturePhoto()
				if detected:
					dataCam["Camera"] = "Person Detected"
					print(f"Camera {dataCam['Camera']}")
					client.publish(topic, json.dumps(dataCam))
			client.publish(topic, json.dumps(dataPir))
