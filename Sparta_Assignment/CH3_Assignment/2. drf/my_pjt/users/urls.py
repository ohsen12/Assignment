from django.urls import path
from . import views
# JWT 구현
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = "users"

urlpatterns = [
    
    # as_view() 메서드를 통해 뷰 클래스 안의 http 요청에 따른 메서드가 실제 요청을 처리하는 뷰 함수로 변환되어 URL 패턴과 연결된다.
    path("signup/", views.UserSignupView.as_view(), name="signup"),
    
    # 이 url 에서 JSON 데이터에 회원의 username과 password를 담아 POST 요청으로 보내면, TokenObtainPairView는 이를 통해 인증(로그인)하고, 인증에 성공하면 액세스 토큰과 리프레시 토큰을 생성하여 반환한다.
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # 엑세스 토큰이 만료된 경우, 클라이언트는 이 url 에서 리프레시 토큰을 사용해 새로운 액세스 토큰을 발급 받는다.
    # 이 url에 리프레시 토큰을 담아 send하면 자동으로 TokenRefreshView로 넘어가서 새로운 리프레시 토큰을 발급해준다.
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    
]
