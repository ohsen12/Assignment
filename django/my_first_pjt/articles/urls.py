# 각각의 앱 안에 직접 urls.py 파일을 만들어줄 수도 있다.
# 구조는 기본 프로젝트의 urls.py 랑 동일하게 해주면 된다. urlpatterns가 필요함


from django.urls import path
from . import views # 내 위치랑 같은 곳에서 임포트 하겠다.


# articles url의 네임스페이스 지정(같은 별명을 가진 url을 구분해주기 위함) 이제 템플릿 태그에서 {% url 'articles:create'%} 이런식으로 써주면 됨
app_name = "articles"

# 특정 url 패턴으로 들어왔을 때(주소창), 어떠한 뷰로 보낼지를 결정하는 곳
# /의 유무와 상관없이 오늘 날의 웹에서는 이를 같은 것으로 인식하나, 장고에서는 /를 끝에 붙이는 것을 권장한다.
urlpatterns = [

    path("", views.articles, name = "articles"),
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.article_detail, name="article_detail"), # <>는 변수로 들어올 값. 따라서 뷰 함수에서 이를 받을 매개변수를 만들어놔야 한다.
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/comments/", views.comment_create, name="comment_create"), # 댓글 작성하는 뷰로 연결시켜주는 url
    # 댓글 삭제 (해당 글의 pk, 해당 글의 댓글의 pk 둘 다 필요함. 일단 해당 글까지 들어왔으니까 그 뒤로 ~ 아오 복잡해)
    path(
        "<int:pk>/comments/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
    
    path("index/", views.index, name='index'), 
    
    path("data-throw/", views.data_throw, name = "data-throw"),
    path("data-catch/", views.data_catch, name = "data-catch"),

]