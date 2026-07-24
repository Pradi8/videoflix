from django.db import models

class Video(models.Model):

    category_choices = [
        ('Action', 'Action'),
        ('Romance', 'Romance'),
        ('Drama', 'Drama'),
        ('Comedy', 'Comedy')
    ]

    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_url = models.FileField(upload_to='thumbnails/', blank=True, null=True)
    category = models.CharField(max_length=10, choices=category_choices, default='Action')

    def __str__(self):
        return self.title
    
    def hls_directory(self):
        return f"movies/{self.id}"

    def hls_master_path(self):
        return f"movies/{self.id}/master.m3u8"

    def hls_resolution_path(self, resolution):
        return (
            f"movies/{self.id}/{resolution}/index.m3u8"
        )