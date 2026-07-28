
from rest_framework import serializers
from videoflix.models import Video

class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Video model.
    - Serializes the Video model fields and generates dynamic URLs for thumbnail and HLS playlist.
    """
    thumbnail_url = serializers.SerializerMethodField()
    hls_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url','hls_url', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('video_file', None)
        self.fields.pop('hls_path', None)  

    def get_thumbnail_url(self, obj):
        if obj.thumbnail_url:
            return self.context["request"].build_absolute_uri(
                obj.thumbnail_url.url
            )
        return None
    
    def get_hls_url(self, obj):
        request = self.context.get("request")

        url = f"/api/video/{obj.id}/720p/index.m3u8"

        if request:
            return request.build_absolute_uri(url)

        return url