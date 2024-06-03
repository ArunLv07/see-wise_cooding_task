from rest_framework import generics, permissions
from .models import Video
from .serializers import VideoSerializer
from django.conf import settings
from rest_framework.views import APIView
import cv2 as cv
from django.conf import settings
import os
from django.http import StreamingHttpResponse


class VideoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

class VideoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]


class VideoStreamingView(APIView):
    def get(self, request):
        video_file = request.query_params.get('video')
        video_path = os.path.join(settings.STATIC_ROOT, 'video', video_file)

        def generate():
            cap = cv.VideoCapture(video_path)
            if not cap.isOpened():
                print("Cannot open camera")
                return
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break

                _, jpeg = cv.imencode('.jpg', frame)
                frame = jpeg.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

            cap.release()

        return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')

    