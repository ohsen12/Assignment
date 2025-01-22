from django.urls import path
from . import views


app_name = "users"
urlpatterns = [
    
    # as_view() 메서드를 통해 뷰 클래스 안의 http 요청에 따른 메서드가 실제 요청을 처리하는 뷰 함수로 변환되어 URL 패턴과 연결된다.
    path("signup/", views.UserSignupView.as_view(), name="signup"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    
]
