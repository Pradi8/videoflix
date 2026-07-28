import os
import shutil
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.files import File
import django_rq
from .models import Video
from utils.thumbnail import generate_thumbnail


@receiver(post_save, sender=Video)
def create_thumbnail(sender, instance, created, **kwargs):
    """ 
    Signal receiver that automatically creates a thumbnail after a new Video object has been saved. 
    """
    if created and instance.video_file and not instance.thumbnail_url:

        thumb_path = generate_thumbnail(instance.video_file.path)

        with open(thumb_path, "rb") as f:
            instance.thumbnail_url.save(
                os.path.basename(thumb_path),
                File(f),
                save=False
            )

        instance.save(update_fields=["thumbnail_url"])


@receiver(post_save, sender=Video)
def generate_video_hls(sender, instance, created, **kwargs):
    """
    Signal receiver that automatically generates HLS files after a new Video object is created.
    """
    if created and instance.video_file:

        queue = django_rq.get_queue("default")

        queue.enqueue(
            "videoflix.tasks.generate_hls_task",
            instance.id
        )
        

@receiver(post_delete, sender=Video)
def delete_video_files(sender, instance, **kwargs):
    """Delete all files related to a video after the database object is deleted."""

    if instance.video_file:
        video_path = instance.video_file.path

        if os.path.isfile(video_path):
            os.remove(video_path)

    if instance.thumbnail_url:
        thumbnail_path = instance.thumbnail_url.path

        if os.path.isfile(thumbnail_path):
            os.remove(thumbnail_path)

    hls_directory = os.path.join(
        settings.MEDIA_ROOT,
        "movies",
        str(instance.pk)
    )

    if os.path.isdir(hls_directory):
        shutil.rmtree(hls_directory)