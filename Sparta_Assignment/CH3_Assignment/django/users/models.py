from django.db import models
from django.contrib.auth.models import AbstractUser

# 커스텀 유저모델 정의
class CustomUser(AbstractUser):
    # upload_to 는 MEDIA_ROOT의 하위 경로를 지정한다. 즉, 이미지가 업로드 되는 경로
    profile_image = models.ImageField(upload_to="images/", blank = True)
    introduction = models.TextField(blank=True)
