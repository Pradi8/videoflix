import subprocess
from tempfile import NamedTemporaryFile

def generate_thumbnail(video_path, time="00:00:01"):
    """
    Extracts a frame from the video (default: second 1)
    The default frame is taken at the 1-second mark.
    """
    # Create a temporary JPG file where FFmpeg will save the thumbnail. 
    # delete=False keeps the file after closing so it can be used later.
    temp_thumb = NamedTemporaryFile(suffix=".jpg", delete=False)
    temp_thumb.close()

    # Build the FFmpeg command:
    # -y               -> overwrite the output file if it already exists
    # -ss              -> seek to the specified time in the video
    # -i               -> input file (the video)
    # -frames:v 1      -> extract only one frame
    # -q:v 2           -> set the output image quality
    # temp_thumb.name  -> output JPG file path

    command = [
        "ffmpeg",
        "-y",
        "-ss", time,
        "-i", video_path,
        "-frames:v", "1",
        "-q:v", "2",
        temp_thumb.name
    ]

    # Execute the FFmpeg command.
    # stdout and stderr are captured so errors can be checked manually.

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # If FFmpeg fails, raise an exception with the error message.
    if result.returncode != 0:
        raise Exception(result.stderr.decode())

    return temp_thumb.name