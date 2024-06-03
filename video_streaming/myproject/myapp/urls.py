from django.urls import path, include
from .views import VideoListCreateAPIView, VideoRetrieveUpdateDestroyAPIView, VideoStreamingView

urlpatterns = [
    path('videos/', VideoListCreateAPIView.as_view(), name='video-list-create'),
    path('videos/<int:pk>/', VideoRetrieveUpdateDestroyAPIView.as_view(), name='video-retrieve-update-destroy'),
    path('auth/', include('rest_framework.urls')),
    path('video_stream/',VideoStreamingView.as_view(),name="video_streaming")
]
