# 각각의 앱 안에 직접 urls.py 파일을 만들어줄 수도 있다.
# 구조는 기본 프로젝트의 urls.py 랑 동일하게 해주면 된다. urlpatterns가 필요함


from django.urls import path
from . import views # 내 위치랑 같은 곳에서 임포트 하겠다.


# 특정 url 패턴으로 들어왔을 때(주소창), 어떠한 뷰로 보낼지를 결정하는 곳
# /의 유무와 상관없이 오늘 날의 웹에서는 이를 같은 것으로 인식하나, 장고에서는 /를 끝에 붙이는 것을 권장한다.
urlpatterns = [


    path("hello/", views.hello),
    path("data-throw/", views.data_throw),
    path("data-catch/", views.data_catch),


]