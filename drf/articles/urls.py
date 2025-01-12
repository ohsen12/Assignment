from django.urls import path
from . import views


# url 네임스페이스 지정
app_name = "articles"

urlpatterns = [
    
    path("html/", views.article_list_html, name="article_list_html"),
    path("json-01/", views.json_01, name="json_01"),
    path("json-02/", views.json_02, name="json_02"),

]
