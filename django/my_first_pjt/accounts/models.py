from django.db import models
from django.contrib.auth.models import AbstractUser


# 기본 User Model을 대체할 커스텀 유저모델인 AUTH_USER_MODEL 설정해주기(반드시 최초 마이그레이션과 함꼐하기)
# Create your models here.
class User(AbstractUser):
    pass