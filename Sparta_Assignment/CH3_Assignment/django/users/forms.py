from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse

# 회원가입(유저생성) 폼
class CustomUserCreationForm(UserCreationForm):
    '''
    UserCreationForm: Django 기본 제공 폼으로, 새로운 사용자를 생성할 때 사용된다.
    기본 UserCreationForm에 포함된 필드:
    username : 새 사용자 계정의 사용자명을 입력받는 필드
    password1 : 사용자가 설정할 비밀번호를 입력받는 필드
    password2 : 사용자가 설정한 비밀번호를 재입력하여 확인하는 필드
    '''
    class Meta:
        # 이 폼은 현재 사용되고 있는 유저모델을 기반으로 한다.
        model = get_user_model()
        # 기존 필드에 커스텀 필드(profile_image, introduction)를 추가
        fields = ('username', 'password1', 'password2', 'profile_image', 'introduction')