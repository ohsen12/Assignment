from django.urls import path
from . import views

# 네임스페이스
app_name = "articles"

urlpatterns = [
    
    # path("html/", views.article_list_html, name="article_list_html"),
    # path("json-01/", views.json_01, name="json_01"),
    # path("json-02/", views.json_02, name="json_02"),
    # path("json-drf/", views.json_drf, name="json_drf"),
    
    # api/v1/articles/이렇게만 들어오면 article_list 뷰로 보내라
    path("", views.article_list, name="article_list"),
    # 엄 원래 그 템플릿 태그에서 article.pk 이런 식으로 url 변수에 할당해줬는데 이제 탬플릿 안하니까 그냥 직접 url에 변수 입력하시더라!
    path("<int:pk>/", views.article_detail, name="article_detail"),
    
]

