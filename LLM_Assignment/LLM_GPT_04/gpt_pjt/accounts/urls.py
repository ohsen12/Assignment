from django.urls import path
from . import views
# JWT 구현(로그인을 위한 클래스 뷰)
from rest_framework_simplejwt.views import TokenObtainPairView

app_name="accounts"

urlpatterns = [
    
    # 회원가입
    path("signup/", views.UserSignupView.as_view(), name="signup"),
    
    # JWT를 사용한 로그인 로직 (따로 뷰 작성할 필요 ❌)
    # 이 url 에서 JSON 데이터에 회원의 username과 password를 담아 POST 요청으로 보내면, TokenObtainPairView는 이를 통해 인증(로그인)하고, 인증에 성공하면 액세스 토큰과 리프레시 토큰을 생성하여 반환한다.
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    
    # JWT 를 사용한 로그아웃 로직
    # 클라이언트는 로그아웃을 요청할 때 리프레시 토큰을 POST 방식으로 서버에 보낸다
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    
    # 회원탈퇴 (Delete)
    path("user_delete/", views.UserDeleteView.as_view(), name="user_delete"),
    
]
