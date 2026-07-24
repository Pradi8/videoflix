from django.http import FileResponse, Http404
from rest_framework.views import APIView, Response, settings
from videoflix.api.serializers import VideoSerializer
from videoflix.models import Video
from rest_framework.permissions import AllowAny, IsAuthenticated

class AllVideosView(APIView):
    """
    API endpoint that returns a list of all videos.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(
            videos, many=True, 
            context={"request": request}
            )
        return Response(serializer.data)
    
class VideoplaylistView(APIView):
    """
    API endpoint that returns the HLS playlist (.m3u8) file for a specific
    video resolution.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, movie_id, resolution):
        """
        Returns the HLS playlist (.m3u8) file for a specific video resolution.
        """
        file_path = (
            settings.MEDIA_ROOT
            / "movies"
            / str(movie_id)
            / resolution
            / "index.m3u8"
        )

        if not file_path.exists():
            raise Http404("HLS playlist not found")

        return FileResponse(
            open(file_path, "rb"),
            content_type="application/vnd.apple.mpegurl"
        )
    
class SingleVideosView(APIView):
    """
    API endpoint that returns a single video by its ID.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, movie_id, resolution, segment):

        file_path = (
            settings.MEDIA_ROOT
            / "movies"
            / str(movie_id)
            / resolution
            / segment
        )

        if not file_path.exists():
            raise Http404("Segment not found")

        return FileResponse(
            open(file_path, "rb"),
            content_type="video/mp2t"
        )