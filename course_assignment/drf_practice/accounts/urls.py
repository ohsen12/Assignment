from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # JWT를 사용한 로그인(인증) 요청을 보낼 url. JSON 데이터로 로그인 정보를 담아 send하면 해당 사용자의 엑세스와 리프레시 토큰을 응답으로 준다.
    path("signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # 리프레시 토큰을 사용해서 다시 엑세스(이건 로테이션 옵션 True로 설정해줘서 주는 거고)랑 리프레시 토큰을 응답으로 발급 받을 요청을 보낼 url
    # 이 url로 요청 send하면 자동으로 TokenRefreshView로 넘어가서 새로운 리프레시 토큰 발급해주는 듯 
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
