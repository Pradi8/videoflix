
from rest_framework import serializers
from videoflix.models import Video

class VideoSerializer(serializers.ModelSerializer):
    # Use a custom method to generate the thumbnail URL dynamically.
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the video_file field from the serializer output if it exists.
        # The API will not expose the original video file.
        self.fields.pop('video_file', None)

    def get_thumbnail_url(self, obj):
        if obj.thumbnail_url:
            # Build an absolute URL including the domain and protocol. 
            # Example: /media/thumbnails/image.jpg becomes: 
            # http://localhost:8000/media/thumbnails/image.jpg
            return self.context["request"].build_absolute_uri(
                obj.thumbnail_url.url
            )
        return None