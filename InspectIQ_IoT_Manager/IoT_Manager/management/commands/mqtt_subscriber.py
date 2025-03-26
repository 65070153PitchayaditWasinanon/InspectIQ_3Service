import paho.mqtt.client as mqtt
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from IoT_Manager.models import IoTDevice  # ตรวจสอบว่า import model ถูกต้อง
import requests
import time

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "iot/sensor/data"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        datas = json.loads(msg.payload.decode("utf-8"))
        print(f"Received: {datas}")

        # จัดรูปแบบข้อมูลที่ต้องการส่ง
        iot_set_id = {
            'id': datas['id'],
            'temperature': datas['temperature'],
            'humidity': datas['humidity'],
            'timestamp': datetime.strptime(datas['timestamp'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"),
            'name': datas['name']
        }

        url = 'http://localhost:8004/tracking/update/'  # เปลี่ยนเป็น URL ที่ถูกต้องของ API ของคุณ

        encoded_iot_set_id = json.dumps(iot_set_id)
        encoded_iot_set_id = requests.utils.quote(encoded_iot_set_id)

        # ส่ง GET request โดยใส่ iot_set_id เป็น query string
        response2 = requests.get(f'{url}?iot_set_id={encoded_iot_set_id}')

        payload = {
            "request": str(response2.json()["request_id"]),  # ตัวอย่าง request ID
            "iot_set_id": iot_set_id  # ใช้ json.dumps เพื่อให้เป็นสตริง JSON
        }

        print(f"Sending data: {payload}")

        # ส่งข้อมูลแบบ JSON ด้วย PUT request
        response = requests.put(url, json=payload)

        # ตรวจสอบผลลัพธ์
        if response.status_code == 200:
            print("Data updated successfully:", response.json())
        elif response2.status_code == 200:
            print("Data updated successfully 2:", response2.json())
        else:
            print("Failed to update data:", response.status_code, response.text)
        
    except Exception as e:
        print(f"Error: {e}")

class Command(BaseCommand):
    help = "Start MQTT Subscriber to receive IoT data"

    def handle(self, *args, **options):
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(BROKER, PORT, 60)
        client.loop_forever()
