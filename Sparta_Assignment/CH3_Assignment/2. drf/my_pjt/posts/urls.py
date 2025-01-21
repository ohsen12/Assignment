from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    # Read(GET) , Create(Post)
    # 이 url은 GET이나 POST 요청을 받아 게시글을 조회하거나, 게시글을 생성하는 뷰로 연결해준다. (물론 drf니까 반환하는 건 JSON 응답임.)
    path("", views.PostAPIView.as_view(), name="post"),
]
