from .models import Video
from .service.hls import HLSService


def generate_hls_task(video_id):
    """
    Background task that generates HLS files for a video.
    """
    video = Video.objects.get(id=video_id)

    HLSService.create_hls(video)