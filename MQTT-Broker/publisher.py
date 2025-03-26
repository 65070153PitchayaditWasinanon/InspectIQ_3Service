import paho.mqtt.client as mqtt
import uuid
import json
import random
import time

BROKER = "test.mosquitto.org"  # หรือ IP ของ Broker ที่คุณใช้
PORT = 1883
TOPIC = "iot/sensor/data"  # กำหนด topic ที่ต้องการส่ง
DEVICE_NAME = "IoT_Device_01"
DEVICE_UUID = str(uuid.uuid4())

def publish_data():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)

    while True:
        data = {
            "id": DEVICE_UUID,
            "temperature": round(random.uniform(20.0, 35.0), 2),
            "humidity": round(random.uniform(30.0, 80.0), 2),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "name": DEVICE_NAME
        }
        payload = json.dumps(data)
        client.publish(TOPIC, payload)
        print(f"Published: {payload}")
        time.sleep(30)  # ส่งข้อมูลทุก 5 วินาที

if __name__ == "__main__":
    publish_data()
