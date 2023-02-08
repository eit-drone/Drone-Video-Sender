from rich.console import Console

from open_gopro import WiredGoPro, Params
from open_gopro.util import setup_logging

console = Console()  # rich consoler printer


def fetch_image(output_file: str = "img/download.png") -> None:
    setup_logging(__name__, "test.log")

    with WiredGoPro(serial=None) as gopro:
        gopro.http_setting.video_performance_mode.set(
            Params.PerformanceMode.MAX_PERFORMANCE
        )
        gopro.http_setting.max_lens_mode.set(Params.MaxLensMode.DEFAULT)
        gopro.http_setting.camera_ux_mode.set(Params.CameraUxMode.PRO)
        gopro.http_command.set_turbo_mode(mode=Params.Toggle.DISABLE)
        assert gopro.http_command.load_preset_group(
            group=Params.PresetGroup.PHOTO
        ).is_ok

        # Get the media list before
        media_set_before = set(
            x["n"] for x in gopro.http_command.get_media_list().flatten
        )
        # Take a photo
        console.print("Capturing a photo...")
        assert gopro.http_command.set_shutter(shutter=Params.Toggle.ENABLE).is_ok

        # Get the media list after
        media_set_after = set(
            x["n"] for x in gopro.http_command.get_media_list().flatten
        )
        # The photo is (most likely) the difference between the two sets
        photo = media_set_after.difference(media_set_before).pop()
        # Download the photo
        console.print("Downloading the photo...")
        gopro.http_command.download_file(camera_file=photo, local_file=output_file)
        console.print(f"Success!! :smiley: File has been downloaded to {output_file}")
        gopro.http_command.delete_file(camera_file=photo)
