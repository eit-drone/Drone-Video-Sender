import os
import numpy as np
import paho.mqtt.client as mqtt
from .mqtt_options import (
    MQTT_BROKER,
    MQTT_TOPIC,
    MQTT_USER,
    MQTT_PASS,
    parse_timing_frame,
)
import cv2
import restream.calib.recorder as recorder
import time


class MQTTVideoStream:
    def __init__(self, silent=False) -> None:
        self.frame = None
        self.client = None
        self.silent = silent

    def __info(self, msg):
        if not self.silent:
            print(msg)

    def get_frame(self):
        frame = self.frame
        self.frame = None
        return frame

    def on_connect(self, client, userdata, flags, rc):
        self.__info("Connected with result code " + str(rc))
        self.client.subscribe(MQTT_TOPIC)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        # Decoding the message
        # converting into numpy array from buffer
        npimg = parse_timing_frame(msg.payload, print_func=self.__info)
        # Decode to Original Frame
        self.frame = cv2.imdecode(npimg, 1)

    def listen_for_frames(self):
        self.client = mqtt.Client()
        self.client.username_pw_set(MQTT_USER, MQTT_PASS)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(MQTT_BROKER)

        # Starting thread which will receive the frames
        self.client.loop_start()

    def shutdown(self):
        # Stop the Thread
        self.client.loop_stop()


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


def record_stream():
    cap = MQTTVideoStream(silent=True)
    cap.listen_for_frames()

    if not os.path.exists("recordings"):
        os.makedirs("recordings")

    while True:
        recorder.record_cap_to_file(cap, f"recordings/record{time.strftime('%Y%m%d-%H%M%S')}.mp4", fps=6)

        if input("Do you want to record another video? [y/n]") != "y":
            break
    cap.shutdown()

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
