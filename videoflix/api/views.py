from rest_framework.views import APIView, Response
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