# usb.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Nov 18 00:18:13 UTC 2022

"""Usb demo"""

import argparse
import cv2
import signal
from typing import Final
from pathlib import Path

from rich.console import Console

from open_gopro import WiredGoPro, Params
from open_gopro.util import setup_logging, display_video_blocking

console = Console()  # rich consoler printer

STREAM_URL: Final[str] = r"udp://0.0.0.0:8554"

import subprocess
import cv2


def resend_stream_to_rtmp(source: str, rtmp_url: str):
    # command and params for ffmpeg
    command = [
        "ffmpeg",
        "-i",
        f"{source}?overrun_nonfatal=1&fifo_size=500000",
        "-f",
        "flv",
        "-preset",
        "ultrafast",
        "-tune",
        "zerolatency",
        f"{rtmp_url}",
        "-loglevel",
        "debug",
    ]

    # using subprocess and pipe to fetch frame data
    subprocess.call(command)


def main(args: argparse.Namespace) -> None:
    setup_logging(__name__, args.log)

    with WiredGoPro(args.identifier) as gopro:
        # Start webcam
        gopro.http_command.wired_usb_control(control=Params.Toggle.DISABLE)
        assert gopro.http_command.webcam_start().is_ok

        def shutdown():
            assert gopro.http_command.webcam_stop().is_ok
            assert gopro.http_command.webcam_exit().is_ok

        orig_sigint = signal.getsignal(signal.SIGINT)
        orig_sigterm = signal.getsignal(signal.SIGTERM)

        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

        # Start player
        resend_stream_to_rtmp(STREAM_URL, "rtmp://localhost:8889/live/app")

        # Restore original signal handlers
        signal.signal(signal.SIGINT, orig_sigint)
        signal.signal(signal.SIGTERM, orig_sigterm)

        shutdown()

    console.print("Exiting...")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Setup and view a GoPro webcam.")
    parser.add_argument(
        "-i",
        "--identifier",
        type=str,
        help="Last 3 digits of GoPro serial number, which is the last 3 digits of the default camera SSID. If \
            not specified, first GoPro discovered via mDNS will be used",
    )
    parser.add_argument(
        "-l",
        "--log",
        type=Path,
        help="Location to store detailed log",
        default="gopro_demo.log",
    )
    return parser.parse_args()


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    main(parse_arguments())


if __name__ == "__main__":
    entrypoint()
