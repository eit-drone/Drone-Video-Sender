import cv2
import paho.mqtt.client as mqtt
import struct
from mqtt_options import MQTT_BROKER, MQTT_TOPIC
from camera_handle import start_webcam, stop_webcam

SKIP_FRAMES = 10

def start_relay():
    client = mqtt.Client()
    #client.username_pw_set(MQTT_USER, MQTT_PASS)
    print("Connecting to MQTT broker")
    client.connect(MQTT_BROKER, port=1883)

    stream_url = start_webcam()
    cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)

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
    finally:
        cap.release()
        client.disconnect()
        stop_webcam()
        print("\nNow you can restart fresh")

if __name__ == "__main__":
    start_relay()