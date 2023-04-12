from restream.calib.recorder import record_cap_to_file
from restream.mqtt_recv import MQTTVideoStream
import os

REQUIRED_VIDEOS = {
    "cam": "Move SLOWLY around the board. We do not want motion blur or the rolling shutter to influence the result. Record for about 20-30s.",
    "imu_bias": "Place the GoPro on the floor or on a table and press record. Leave it there for 10-20s without touching it. This video will be used to estimate the current IMU bias. We assume it to be fixed during the calibration.",
    "cam_imu": "Again record the board and make sure that you have good lighting conditions. If possible set the shutter time of your GoPro the minimum (e.g. 1/480). Excite all 3 axis -> 3 translation and 3 rotation. Move fast, but not too fast (motion blur).",
}


def record_video_type(
    dataset: str, cap: MQTTVideoStream, type: str, counter: int
) -> int:
    desc = REQUIRED_VIDEOS[type]

    if not os.path.exists(f"{dataset}/{type}"):
        os.makedirs(f"{dataset}/{type}")

    while True:
        print(f"Please record a video for {type} calibration. {desc}")
        input("Press enter when you are ready to record.")
        print("Recording...")

        record_cap_to_file(cap, f"{dataset}/{type}/GH{counter:04d}.MP4", fps=6)

        print("Recording finished.")
        counter += 1

        if input("Do you want to record another video? [y/n]") != "y":
            break

    return counter


def make_dataset():
    counter = 0

    cap = MQTTVideoStream(silent=True)
    cap.listen_for_frames()

    dataset = input("Please enter the name of the dataset: ")

    if os.path.exists(dataset):
        print("Dataset already exists. Please choose another name.")
        return

    os.makedirs(dataset)

    for type in REQUIRED_VIDEOS.keys():
        counter = record_video_type(dataset, cap, type, counter)

    cap.shutdown()


if __name__ == "__main__":
    make_dataset()
