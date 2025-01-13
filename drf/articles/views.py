from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Article
from django.core import serializers

# drf
from rest_framework import status # 상태코드가 어떤 메세지를 담고 있는지 상수로 미리 정의되어있는 모듈
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ArticleSerializer


# # 장고 시드로 심은 아티클 객체들을 화면으로 확인해보자!
# def article_list_html(request):
#     # 장고 시드로 만들어놓은 아티클 객체 다 들고와서 템플릿으로 넘겨줄게
#     articles = Article.objects.all()
#     context = {"articles": articles}
#     return render(request, "articles/articles.html", context)


# '''

# Serialization란

# 직렬화(Serialization)

# - 객체 또는 데이터 구조를 저장, 전송을 위해 다른 포맷으로 변경하는 것입니다.
    
#     → 데이터의 구조는 유지하면서 추후 재구성이 가능한 포맷으로 변환해요!
    
# - 현재 Python 객체 형태인 Queryset 혹은 Model의 Instance를 전송 가능한 형태로 직렬화를 통해 JSON, XML, YAML 등의 형태로 변환하는 것입니다.
# - Django도 내부적으로 다른 데이터 포맷으로 쉽게 직렬화 할 수 있는 기능을 제공합니다.

# '''


# # Json Response 를 줘보자!
# def json_01(request):
#     articles = Article.objects.all()
#     json_res = []
#     # 아티클 객체 다 담아와서 빈리스트에 JSON 형식으로? 채워주기
#     for article in articles:
#         json_res.append(
#             {
#                 "title": article.title,
#                 "content": article.content,
#                 "created_at": article.created_at,
#                 "updated_at": article.updated_at,
#             }
#         )
#     # JSON으로 인코딩된 response를 만드는 HttpResponse의 서브 클래스
#     # dict 타입이 아닌 객체를 직렬화(Serialization)하기 위해서는 safe=False 로 설정해야 한다.
#     return JsonResponse(json_res, safe=False)


# # Django는 아래와 같이 내부적으로 serializer를 제공하지만 모델 구조에 한정되어 유연하지 못하다.
# # serializers는 유연한 API를 위한 기능이라기보다 모델 구조로 저장되어있는 데이터를 export 하는 용도에 가깝다
# def json_02(request):
#     articles = Article.objects.all()
#     res_data = serializers.serialize("json", articles)
#     return HttpResponse(res_data, content_type="application/json")

# '''
# 위와 같은 문제를 해결하기 위해, 모델에 종속적이지 않고 유연하지만 사용하기 편한 Serializer의 필요성이 대두되었고
# 이를 위해 등장한 것이 바로 Django RESTfull API 이다!

# 📕 Django REST Framework (DRF)

# - Django를 이용해서 API를 구축하는 기능을 제공하는 라이브러리
# - Django의 Form, ModelForm과 굉장히 비슷하게 구성 및 작동

# '''

# # drf 함수형으로 뷰를 작성할 때는 반드시 api_view 데코레이터를 달아줘야 한다. 
# # 그리고 그 안쪽에는 내가 허용할 http 메서드들을 넣어놓으면 됨
# # ❗️이렇게 들어가면 drf가 알아서 템플릿을 적용해서 예쁘게 보여준다.
# @api_view(["GET"])
# def json_drf(request):
#     articles = Article.objects.all()
#     # 조회한 객체를 직렬화해주기
#     # 조회한 객체가 현재 단일 객체가 아닌 상황이라 many=True를 넣어줘야 함
#     serializer = ArticleSerializer(articles, many=True)
#     # 시리얼라이저 안쪽에 serializer.data라는 속성으로 JSON 데이터가 들어있다. 이걸 그대로 응답으로 담아주기
#     return Response(serializer.data)

# # ⬆️ 이제는 모델에 종속된 게 아니라 모델을 사용해서, 유연하게 나만의 응답을 만들 수 있다! 
# # serializers.py 에다가 원하는대로 보여줄 필드나, 보여질 필드의 형식이나(두 필드를 더한다든지) 이런 거를 커스텀해서 정의해놓고 직렬화하면 되는 거다!


# '''

# 근데 이렇게 해서 계속 콜하는 거 너무 불편하잖아?
# API를 제공하는 서버를 개발하고나면, 해당 API를 Call 하고 결과도 볼 수 있는 무언가가 필요하다!

# ➡️ Postman 📮
# - 개발자가 API를 디자인, 테스트, 문서화, 공유를 할 수 있도록 도와주는 소프트웨어.
# - API 테스트, 환경 관리, 협업 등을 위한 강력한 기능을 제공하여 보다 효율적으로 API를 개발하고 테스트 할 수 있게 도와줌.

# '''



# drf의 Serializer는 단순 Serialization외에도 Model을 이용한 다양한 기능을 제공한다.
# ❗️웹페이지로 조회할 때랑은 다르게 예는 url 끝에 / 안 붙여주면 제대로 동작 안하더라 ❗️

# 1️⃣ Read

# 아티클 목록 전체 조회
# drf 함수형으로 뷰를 작성할 때는 반드시 api_view 데코레이터를 달아줘야 한다. 
# 그리고 그 안쪽에는 내가 허용할 http 메서드들을 넣어놓으면 됨.
@api_view(["GET","POST"])
def article_list(request):
    # 아티클 목록 조회해달라고 들어왔으면
    if request.method == "GET":
        # 아티클 모델에 있는 객체 다 조회해서
        articles = Article.objects.all()
        # 조회한 객체를 직렬화해주기
        # 조회한 객체가 현재 단일 객체가 아닌 상황이라 many=True를 넣어줘야 함
        serializer = ArticleSerializer(articles, many=True)
         # 시리얼라이저 안쪽에 serializer.data라는 속성으로 JSON 데이터가 들어있다. 이걸 그대로 응답으로 담아주기
        return Response(serializer.data)
    
    # 2️⃣ Create
    # 아티클 생성하겠다고 바디에 데이터 담아왔으면
    elif request.method == "POST":
        # 입력데이터랑 바인딩된 시리얼라이저 만들어주고 (그 먼젓번에 맨날 바인딩 폼 만들어서 save 해줬던 것처럼)
        serializer = ArticleSerializer(data=request.data)
        # 유효하면, (만약 유효하지 않으면 drf가 알아서 제공해주는 에러나는 이유 serializer.errors를 보낸다. 상태코드는 400(Bad request로)으로)
        if serializer.is_valid(raise_exception=True):
            # DB에 저장하고
            serializer.save()
            # 응답보내 created 상태코드인 201 띄워서. 
            return Response(serializer.data, status.HTTP_201_CREATED)


# 아티클 상세 조회 (밑에 구조는 다 비슷비슷하제?!)
@api_view(["GET","PUT","DELETE"])
def article_detail(request, pk):
    # 일단 해당 아티클 들고오고
    article = get_object_or_404(Article, pk=pk)
    
    # 상세글 보겠다고 GET으로 왔으면
    if request.method == "GET":
    # pk에 해당하는 아티클 객체 조회해서 가져와라
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    # 4️⃣ Update
    # 해당 객체 수정하겠다고 PUT 메서드로 들어오면 
    elif request.method == "PUT":
        # 시리얼라이저에 기존 아티클 담아서 보여주고, 이거 수정해서 오는 데이터 직렬화해줘, 그리고 부분 필드만 수정하는 것도 가능하도록  partial=True 옵션을 줘
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    # 3️⃣ Delete
    # 해당 pk 객체 삭제하겠다고 delete 메서드로 들어오면
    elif request.method == "DELETE":
        # 해당 객체 삭제해줘
        article.delete()
        # 응답 띄울 거 만들어놓기
        data = {"delete": f"Article({pk}) is deleted."}
        # 응답띄우고 상태코드는 ok를 뜻하는 200으로 ~
        return Response(data, status=status.HTTP_200_OK)



