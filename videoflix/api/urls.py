from django.urls import path
from .views import AllVideosView

# ------------------------------
# Endpoints Video:
# ------------------------------

urlpatterns = [
    path('video/', AllVideosView.as_view(), name='all_videos'),
]