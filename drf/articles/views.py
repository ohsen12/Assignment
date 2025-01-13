from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Article
from django.core import serializers

# drf
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ArticleSerializer


# 장고 시드로 심은 아티클 객체들을 화면으로 확인해보자!
def article_list_html(request):
    # 장고 시드로 만들어놓은 아티클 객체 다 들고와서 템플릿으로 넘겨줄게
    articles = Article.objects.all()
    context = {"articles": articles}
    return render(request, "articles/articles.html", context)


'''
<aside>
Serialization란

직렬화(Serialization)

- 객체 또는 데이터 구조를 저장, 전송을 위해 다른 포맷으로 변경하는 것입니다.
    
    → 데이터의 구조는 유지하면서 추후 재구성이 가능한 포맷으로 변환해요!
    
- 현재 Python 객체 형태인 Queryset 혹은 Model의 Instance를 전송 가능한 형태로 직렬화를 통해 JSON, XML, YAML 등의 형태로 변환하는 것입니다.
- Django도 내부적으로 다른 데이터 포맷으로 쉽게 직렬화 할 수 있는 기능을 제공합니다.

'''


# Json Response 를 줘보자!
def json_01(request):
    articles = Article.objects.all()
    json_res = []
    # 아티클 객체 다 담아와서 빈리스트에 JSON 형식으로? 채워주기
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
    # dict 타입이 아닌 객체를 직렬화(Serialization)하기 위해서는 safe=False 로 설정해야 한다.
    return JsonResponse(json_res, safe=False)


# Django는 아래와 같이 내부적으로 serializer를 제공하지만 모델 구조에 한정되어 유연하지 못하다.
# serializers는 유연한 API를 위한 기능이라기보다 모델 구조로 저장되어있는 데이터를 export 하는 용도에 가깝다
def json_02(request):
    articles = Article.objects.all()
    res_data = serializers.serialize("json", articles)
    return HttpResponse(res_data, content_type="application/json")


# 위와 같은 문제를 해결하기 위해, 모델에 종속적이지 않고 유연하지만 사용하기 편한 Serializer의 필요성이 대두되었고
# 이를 위해 등장한 것이 바로 Django RESTfull API 이다!

# 원래 함수형으로 뷰를 작성할 때는 반드시 api_view 데코레이터를 달아줘야 한다. 
# 그리고 그 안쪽에는 내가 허용할 http 메서드들을 넣어놓으면 됨
# ❗️이렇게 들어가면 drf가 알아서 템플릿을 적용해서 예쁘게 보여준다.
@api_view(["GET"])
def json_drf(request):
    articles = Article.objects.all()
    # 조회한 객체를 직렬화해주기
    # 조회한 객체가 현재 단일 객체가 아닌 상황이라 many=True를 넣어줘야 함
    serializer = ArticleSerializer(articles, many=True)
    # 시리얼라이저 안쪽에 serializer.data라는 속성으로 JSON 데이터가 들어있다. 이걸 그대로 응답으로 담아주기
    return Response(serializer.data)

# ⬆️ 이제는 더 이상 모델에 종속된 게 아니라 serializers.py 에다가 원하는대로 필드나 이런 거를 커스텀해서 정의해놓고 직렬화하면 되는 거다!

