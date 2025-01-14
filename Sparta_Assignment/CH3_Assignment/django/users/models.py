from django.db import models
from django.contrib.auth.models import AbstractUser

# 커스텀 유저모델 정의
class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to="images/", blank = True)
    introduction = models.TextField(blank=True)
