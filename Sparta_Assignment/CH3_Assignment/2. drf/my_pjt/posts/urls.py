from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    
    # Read(GET), Create(Post)
    # 이 url은 GET이나 POST 요청을 받아 게시글을 조회하거나, 게시글을 생성하는 뷰로 연결해준다. (물론 drf니까 반환하는 건 JSON 응답임.)
    path("", views.PostAPIView.as_view(), name="post"),
    
    # Read(GET:상세글), Update(PUT), Delete(DELETE)
    # 이 url은 GET이나 PUT이나 DELETE 요청을 받아 상세게시글과 관련된 로직을 수행하는 뷰로 연결해준다.
    # 💡 url 태그로 경로 변수를 넘겨줬던 퓨어 장고와 다르게, 지금 이거 실습할 때는 경로변수를 postman url에 직접쳐야 함
    path("<int:post_pk>/", views.PostDetailAPIView.as_view(), name="post_detail"),
    
    # 특정 게시글의 댓글 목록 조회 및 댓글 생성
    path('<int:post_pk>/comments/', views.CommentAPIView.as_view(), name='comment_list_create'),
    # 특정 댓글 조회, 수정, 삭제
    path('<int:post_pk>/comments/<int:comment_pk>/', views.CommentAPIView.as_view(), name='comment_detail'),

]
