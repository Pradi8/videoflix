import os
import subprocess

from django.conf import settings


class HLSService:
    """
    Creates an adaptive HLS stream with multiple resolutions.
    """

    RESOLUTIONS = {
        "480p": {
            "width": 854,
            "height": 480,
            "bitrate": "1000k",
        },
        "720p": {
            "width": 1280,
            "height": 720,
            "bitrate": "3000k",
        },
        "1080p": {
            "width": 1920,
            "height": 1080,
            "bitrate": "6000k",
        },
    }

    @staticmethod
    def create_hls(video):
        """
        Generate HLS playlists and segments for every resolution.
        """

        # Original uploaded video
        input_file = video.video_file.path

        # Output directory for this video
        output_dir = settings.MEDIA_ROOT / "movies" / str(video.id)
        output_dir.mkdir(parents=True, exist_ok=True)

        playlists = []

        # Create one HLS stream per resolution
        for resolution, config in HLSService.RESOLUTIONS.items():

            resolution_dir = output_dir / resolution
            resolution_dir.mkdir(parents=True, exist_ok=True)

            playlist_file = resolution_dir / "index.m3u8"

            command = [
                "ffmpeg",

                # Overwrite existing files
                "-y",

                # Input video
                "-i", input_file,

                # Resize video
                "-vf",
                f"scale={config['width']}:{config['height']}",

                # Video codec
                "-c:v",
                "libx264",

                # Video bitrate
                "-b:v",
                config["bitrate"],

                # Audio codec
                "-c:a",
                "aac",

                # Create a keyframe every 2 seconds (assuming 30 FPS)
                "-g",
                "60",

                # Disable automatic scene-cut keyframes
                "-sc_threshold",
                "0",

                # HLS segment duration
                "-hls_time",
                "4",

                # Create a Video-on-Demand playlist
                "-hls_playlist_type",
                "vod",

                # Mark every segment as independently decodable
                "-hls_flags",
                "independent_segments",

                # Segment filename pattern
                "-hls_segment_filename",
                str(resolution_dir / "segment_%03d.ts"),

                # Output playlist
                str(playlist_file),
            ]

            subprocess.run(command, check=True)

            playlists.append(
                {
                    "bandwidth": config["bitrate"],
                    "resolution": resolution,
                    "path": f"{resolution}/index.m3u8",
                }
            )

        # Create the master playlist
        HLSService.create_master_playlist(output_dir, playlists)

    @staticmethod
    def create_master_playlist(output_dir, playlists):
        """
        Create the master playlist that references all quality levels.
        """

        master_playlist = output_dir / "master.m3u8"

        with open(master_playlist, "w") as file:

            file.write("#EXTM3U\n")

            for playlist in playlists:

                bandwidth = playlist["bandwidth"].replace("k", "000")

                file.write(
                    f"#EXT-X-STREAM-INF:BANDWIDTH={bandwidth}\n"
                )

                file.write(
                    f"{playlist['path']}\n"
                )