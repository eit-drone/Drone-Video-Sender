import base64
import numpy as np
import paho.mqtt.client as mqtt
from mqtt_options import MQTT_BROKER, MQTT_TOPIC, MQTT_USER, MQTT_PASS, parse_timing_frame
import cv2

frame = np.zeros((240, 320, 3), np.uint8)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global frame
    # Decoding the message
    # converting into numpy array from buffer
    npimg = parse_timing_frame(msg.payload)
    # Decode to Original Frame
    frame = cv2.imdecode(npimg, 1)


def listen_for_frames():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER)

    # Starting thread which will receive the frames
    client.loop_start()

    while True:
        cv2.imshow("Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Stop the Thread
    client.loop_stop()


if __name__ == "__main__":
    listen_for_frames()
