import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File
import django_rq
from videoflix.service.hls import HLSService
from .models import Video
from utils.thumbnail import generate_thumbnail


@receiver(post_save, sender=Video)
def create_thumbnail(sender, instance, created, **kwargs):
    """ 
    Signal receiver that automatically creates a thumbnail after a new Video object has been saved. 
    """
    # Only create a thumbnail if: 
    # - a new video was created # - a video file exists 
    # - no thumbnail has been generated yet
    if created and instance.video_file and not instance.thumbnail_url:

        # Generate a thumbnail image from the uploaded video file. 
        # Returns the temporary path of the generated JPG file.
        thumb_path = generate_thumbnail(instance.video_file.path)

        # Open the generated thumbnail file in binary read mode.
        with open(thumb_path, "rb") as f:
            instance.thumbnail_url.save(
                os.path.basename(thumb_path),
                File(f),
                save=False
            )

        # Save only the thumbnail_url field to the database. 
        instance.save(update_fields=["thumbnail_url"])


@receiver(post_save, sender=Video)
def generate_video_hls(sender, instance, created, **kwargs):
    """
    Signal receiver that automatically generates HLS files after a new Video object is created.
    """
    # sOnly generate HLS files if:
    # - a new video object was created
    # - a video file exists
    if created and instance.video_file:

        queue = django_rq.get_queue("default")

        queue.enqueue(
            "videoflix.tasks.generate_hls_task",
            instance.id
        )