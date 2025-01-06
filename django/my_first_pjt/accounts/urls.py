# 각각의 앱 안에 직접 urls.py 파일을 만들어줄 수도 있다.
# 구조는 기본 프로젝트의 urls.py 랑 동일하게 해주면 된다. urlpatterns가 필요함


from django.urls import path
from . import views


# url 네임스페이스
app_name = "accounts"

urlpatterns = [

    path("login/", views.login, name = "login"),
    path("logout/", views.logout, name="logout"),
    
]