import cv2
import paho.mqtt.client as mqtt
import struct
from mqtt_options import MQTT_BROKER, MQTT_TOPIC, MQTT_TIMING_TOPIC, MQTT_PASS, MQTT_USER
import datetime

SKIP_FRAMES = 10

def start_relay():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    print("Connecting to MQTT broker")
    client.connect(MQTT_BROKER, port=1883)

    cap = cv2.VideoCapture(0)

    try:
        frame_count = 0

        while True:
            ret, frame = cap.read()

            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            frame_count += 1
            if frame_count % SKIP_FRAMES != 0:
                continue

            buffer = cv2.imencode(".jpg", frame)[1].tobytes()
            jpg_as_packed = struct.pack(f"{len(buffer)}B", *buffer)

            client.publish(MQTT_TOPIC, jpg_as_packed, qos=0)
            client.publish(MQTT_TIMING_TOPIC, datetime.datetime.utcnow().isoformat(), qos=0, retain=False)
    finally:
        cap.release()
        client.disconnect()
        print("\nNow you can restart fresh")

if __name__ == "__main__":
    start_relay()