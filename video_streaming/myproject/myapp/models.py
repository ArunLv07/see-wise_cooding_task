# videos/models.py
from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    name = models.CharField(max_length=255)
    video_url = models.CharField(max_length=255,blank=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)



