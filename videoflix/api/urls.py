from django.urls import path
from .views import AllVideosView, SingleVideosView, VideoplaylistView

# ------------------------------
# Endpoints Video:
# ------------------------------

urlpatterns = [
    path('video/', AllVideosView.as_view(), name='all_videos'),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', VideoplaylistView.as_view(), name='video_playlist'),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>', SingleVideosView.as_view(), name='single_video'),
]