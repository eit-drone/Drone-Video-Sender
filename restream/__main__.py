import sys
from .mqtt_recv import listen_for_frames
from .mqtt_relay import start_relay
from .calib.calibration_tool import make_dataset
from .mqtt_webcam_relay import start_relay as start_webcam_relay

COMMANDS = {
    "start_stream": start_relay,
    "listen_stream": listen_for_frames,
    "run_calibration": make_dataset,
    "start_webcam_stream": start_webcam_relay,
}

command = sys.argv[1] if len(sys.argv) >= 2 else None

def print_help():
    print( "Available commands: ")
    for command in COMMANDS:
        print(f" - {command}")

    print("Usage: python -m restream <command>")

if not command:
    print_help()
    print("No command specified.")
    sys.exit(1)

command_func = COMMANDS.get(command)
if not command_func:
    print_help()
    print(f"Unknown command: {command}")
    sys.exit(1)

command_func()