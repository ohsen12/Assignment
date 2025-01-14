from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # 이미지 업로드 필드 (blank = True 옵션을 줘서 이 부분 없이 업로드하는 것도 가능하게 함)
    profile_image = models.ImageField(upload_to="images/", blank = True) 
    introduction = models.TextField(blank = True)