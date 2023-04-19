import cv2 as cv

def record_cap_to_file(
    cap, filename: str, fps: float = 30.0, size=None
):
    fourcc = cv.VideoWriter_fourcc(*"mp4v")
    out = None
    
    print("Press q to stop recording.")

    while True:
        if cv.waitKey(1) == ord("q"):
            break
        
        frame = cap.get_frame()
        if frame is None:
            continue

        if out is None:
            if size is None:
                size = frame.shape[1], frame.shape[0]
            out = cv.VideoWriter(filename, fourcc, fps, size)
        
        print(frame.shape)
        out.write(frame)
        cv.imshow("Frame", frame)

    out.release()
    cv.destroyAllWindows()
