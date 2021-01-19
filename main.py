import paho.mqtt.client as mqtt
import json
import time
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

broker = "demo.thingsboard.io"
port = 1883
username = "ixrN3vNdkHnpGmXYDic8"
password = ""
topic = "v1/devices/me/telemetry"

client = mqtt.Client()
client.username_pw_set(username, password)
client.connect(broker, port)
print("Connection Establish..")

dataUltra = {}
dataMag = {}
dataRfid = {}
dataPir = {}
while True:
	if(ser.in_waiting > 0):
		data = ser.readline().decode().split()
		if data[0] == "U":
			print(f"Ultrasonic {data[1]}")
			dataUltra["Ultrasonic"] = data[1]
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
			client.publish(topic, json.dumps(dataPir))
