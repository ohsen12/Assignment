# 관리자 페이지에서 사용할 '모델'은 직접 등록해주는 곳.
# 각 앱의 admin.py에서 설정해준다.


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.

# User 모델을 Django의 관리자 사이트에 등록하는 것.
# User: 등록할 모델 / UserAdmin 클래스 : 관리자 사이트에서 User 모델의 데이터를 어떻게 표시하고 관리할지를 정의
# 우리가 등록한 User를 UserAdmin으로 등록해줘
admin.site.register(User, UserAdmin)