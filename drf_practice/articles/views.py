from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Article
from django.core import serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ArticleSerializer

# Create your views here.

# 아티클 객체 다 보여주기
def article_list_html(request):
    articles = Article.objects.all()
    context = {"articles":articles}
    return render(request, "articles/articles.html", context)


# JSON response 주기
def json_01(request):
    # 아티클 다 들고와서 
    articles = Article.objects.all()
    # 빈 리스트에 
    json_res = []

    # 아티클 객체 다 돌면서 다음 딕셔너리 추가해주기
    for article in articles:
        json_res.append(
            {
                "title": article.title,
                "content": article.content,
                "created_at": article.created_at,
                "updated_at": article.updated_at,
            }
        )
    # JSON으로 인코딩된 response를 만드는 HttpResponse의 서브 클래스
    # dict 타입이 아닌 객체를 직렬화(Serialization)하기 위해서는 False로 설정해야 함
    return JsonResponse(json_res, safe=False) # safe=False는 딕셔너리를 주면 안 적어도 되는데 지금 리스트가 들어가서 적어주는 것.


# 장고가 제공하는 serialize 기능. 모델 구조로 저장되어있는 데이터를 export 하는 용도
def json_02(request):
    articles = Article.objects.all()
    # 근데 이 방법은 모델 구조에 의존도가 크기 때문에 커스텀하기가 어려워 유연하지 않다.
    res_data = serializers.serialize("json", articles)
    return HttpResponse(res_data, content_type="application/json") # content_type으로 클라이언트가 내가 받는 데이터의 타입이 JSON 형식이구나 인식하게 해줌.


# ❗️ 위의 두 방법은 뭐 할 수는 있지만, 불편하다. 모델에 종속적이지 않고 유연한 시리얼라이즈가 없을까? 고민하다가 나온 것이 Django RESTfull API ❗️

# 원래 drf에서 뷰를 함수형으로 달 떄에는 api_view 데코레이터를 달아주고 안 쪽에 허용할 메서드를 넣어줘야 한다.
@api_view(["GET"])
def json_drf(request):
    # 데이터를 다 가져와서 
    articles = Article.objects.all()
    # 내가 정의해놓은 시리얼라이저를 갖고 와서 시러얼라이즈 해줄 것이다.
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)