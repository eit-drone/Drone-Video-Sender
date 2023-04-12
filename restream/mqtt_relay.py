import cv2
import paho.mqtt.client as mqtt
from .mqtt_options import MQTT_BROKER, MQTT_TOPIC, MQTT_PASS, MQTT_USER, make_timing_data
from .camera_handle import start_webcam, stop_webcam

SKIP_FRAMES = 5


def start_relay():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    print("Connecting to MQTT broker")
    client.connect(MQTT_BROKER, port=1883)
    print("Connected to MQTT broker")

    print("Starting webcam")
    stream_url = start_webcam(None)
    print("Webcam started")
    cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
    print("VideoCapture started")

    try:
        frame_count = 0

        while cap.isOpened():
            cap.grab()
            ret, frame = cap.read()

            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            frame_count += 1
            if frame_count % SKIP_FRAMES != 0:
                continue
            
            print(f"Publishing frame {frame_count}")
            client.publish(MQTT_TOPIC, make_timing_data(frame_count, frame), qos=0, retain=False)
    finally:
        cap.release()
        client.disconnect()
        stop_webcam(None)
        print("\nNow you can restart fresh")


if __name__ == "__main__":
    start_relay()
