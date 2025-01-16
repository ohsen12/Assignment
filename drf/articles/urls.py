from django.urls import path
from . import views

# 네임스페이스
app_name = "articles"

urlpatterns = [
    
    # path("html/", views.article_list_html, name="article_list_html"),
    # path("json-01/", views.json_01, name="json_01"),
    # path("json-02/", views.json_02, name="json_02"),
    # path("json-drf/", views.json_drf, name="json_drf"),
    
    # # api/v1/articles/이렇게만 들어오면 article_list 뷰로 보내라
    # path("", views.article_list, name="article_list"),
    # # 엄 경로변수.. 원래 그 템플릿 태그에서 article.pk 이런 식으로 url 변수에 할당해줬는데 이제 탬플릿 안하니까 그냥 직접 url에 변수 입력하시더라!
    # path("<int:pk>/", views.article_detail, name="article_detail"),
    
    # CBV를 사용할 때는 참조하는 형식이 변경된다.
    # CBV 는 .뷰이름 + .as_view()까지 필요함
    # 💡 얘는 지금 함수가 아니라 클래스니까, 클래스 자체를 넘기는 것이 아니라 as_view()메서드를 사용해서 호출 가능한 함수로 변환해야 함!
    path("", views.ArticleListAPIView.as_view(), name="article_list"),
    path("<int:pk>/", views.ArticleDetailAPIView.as_view(), name="article_detail"),
    
    # 아티클에 게시글 달기 위한 url
    path("<int:article_pk>/comments/", views.CommentListAPIView.as_view(), name="comment_list"),
    # 어차피 댓글 pk은 고유하기 떄문에 경로 변수에 굳이 아티클 pk까지는 필요 없다.
    path("comments/<int:comment_pk>/", views.CommentDetailAPIView.as_view(), name="comment_detail"),


]

