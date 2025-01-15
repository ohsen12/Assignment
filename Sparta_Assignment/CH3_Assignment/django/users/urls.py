from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    
    path("login/", views.login, name = "login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("user_delete/", views.user_delete, name="user_delete"),
    path("user_update/", views.user_update, name="user_update"),
    
    # url 태그로 전달해줄 변수
    path("user_profile/<str:username>", views.user_profile, name="user_profile"),
    
]