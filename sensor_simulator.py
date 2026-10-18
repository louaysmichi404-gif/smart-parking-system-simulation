
import json
import random
import time
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "smartpark_demo_louay_2026/P1/status"

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id=f"smartpark_sensor_{random.randint(1000, 999999)}"
)

print("Connecting to MQTT broker...")
client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    while True:
        occupied = random.choice([True, False])

        message = {
            "parking_space": "P1",
            "occupied": occupied,
            "timestamp": time.time()
        }

        client.publish(TOPIC, json.dumps(message))
        print("Sent:", message)

        time.sleep(5)

except KeyboardInterrupt:
    print("Sensor simulator stopped.")

finally:
    client.loop_stop()
    client.disconnect()
