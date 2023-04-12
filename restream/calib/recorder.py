import cv2 as cv
from restream.mqtt_recv import MQTTVideoStream


def record_cap_to_file(
    cap: MQTTVideoStream, filename: str, fps: float = 30.0, size=(1920, 1080)
):
    fourcc = cv.VideoWriter_fourcc(*"MP4V")
    out = cv.VideoWriter(filename, fourcc, fps, size)
    
    print("Press q to stop recording.")

    while True:
        if cv.waitKey(1) == ord("q"):
            break
        
        frame = cap.get_frame()
        if frame is None:
            continue

        # write the flipped frame
        out.write(frame)
        cv.imshow("Frame", frame)

    out.release()
    cv.destroyAllWindows()
