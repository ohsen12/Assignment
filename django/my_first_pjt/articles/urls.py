# 각각의 앱 안에 직접 urls.py 파일을 만들어줄 수도 있다.
# 구조는 기본 프로젝트의 urls.py 랑 동일하게 해주면 된다. urlpatterns가 필요함


from django.urls import path
from . import views # 내 위치랑 같은 곳에서 임포트 하겠다.


# 특정 url 패턴으로 들어왔을 때(주소창), 어떠한 뷰로 보낼지를 결정하는 곳
# /의 유무와 상관없이 오늘 날의 웹에서는 이를 같은 것으로 인식하나, 장고에서는 /를 끝에 붙이는 것을 권장한다.
urlpatterns = [

    path("", views.articles, name = "articles"),
    path("new/", views.new, name = 'new'),
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.article_detail, name="article_detail"), # <>는 변수로 들어올 값. 따라서 뷰 함수에서 이를 받을 매개변수를 만들어놔야 한다.
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/edit", views.edit, name="edit"),
    path("<int:pk>/update/", views.update, name="update"),
    
    path("data-throw/", views.data_throw, name = "data-throw"),
    path("data-catch/", views.data_catch, name = "data-catch"),

]