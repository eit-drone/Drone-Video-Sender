from typing import Final

from open_gopro import WiredGoPro, Params

STREAM_URL: Final[str] = r"udp://0.0.0.0:8554"


def stop_webcam(identifier: str) -> None:
    with WiredGoPro(identifier) as gopro:
        assert gopro.http_command.webcam_stop().is_ok
        assert gopro.http_command.webcam_exit().is_ok


def start_webcam(identifier: str) -> str:
    with WiredGoPro(identifier) as gopro:
        # Start webcam
        gopro.http_command.wired_usb_control(control=Params.Toggle.DISABLE)
        assert gopro.http_command.webcam_start(
            resolution=Params.WebcamResolution.RES_480
        ).is_ok

        return f"{STREAM_URL}?overrun_nonfatal=1&fifo_size=500000"
