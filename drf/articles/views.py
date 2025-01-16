from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Article
from django.core import serializers

# drf
from rest_framework import status # 상태코드가 어떤 메세지를 담고 있는지 상수로 미리 정의되어있는 모듈
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ArticleSerializer

# CBV (class based view)
# APIView - DRF CBV의 베이스 클래스
from rest_framework.views import APIView


# # 장고 시드로 심은 아티클 객체들을 화면으로 확인해보자!
# def article_list_html(request):
#     # 장고 시드로 만들어놓은 아티클 객체 다 들고와서 템플릿으로 넘겨줄게
#     articles = Article.objects.all()
#     context = {"articles": articles}
#     return render(request, "articles/articles.html", context)


# '''

# Serialization란

# ❗️직렬화(Serialization)

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

# FBV(function based view)
# # drf의 Serializer는 단순 Serialization외에도 Model을 이용한 다양한 기능을 제공한다.
# # ❗️웹페이지로 조회할 때랑은 다르게 예는 url 끝에 / 안 붙여주면 제대로 동작 안하더라 ❗️

# # 1️⃣ Read

# # 아티클 목록 전체 조회
# # drf 함수형으로 뷰를 작성할 때는 반드시 api_view 데코레이터를 달아줘야 한다. 
# # 그리고 그 안쪽에는 내가 허용할 http 메서드들을 넣어놓으면 됨.
# @api_view(["GET","POST"])
# def article_list(request):
#     # 아티클 목록 조회해달라고 들어왔으면
#     if request.method == "GET":
#         # 아티클 모델에 있는 객체 다 조회해서
#         articles = Article.objects.all()
#         # 조회한 객체를 직렬화해주기
#         # 조회한 객체가 현재 단일 객체가 아닌 상황이라 many=True를 넣어줘야 함
#         serializer = ArticleSerializer(articles, many=True)
#          # 시리얼라이저 안쪽에 serializer.data라는 속성으로 JSON 데이터가 들어있다. 이걸 그대로 응답으로 담아주기
#         return Response(serializer.data)
    
#     # 2️⃣ Create
#     # 아티클 생성하겠다고 바디에 데이터 담아왔으면
#     elif request.method == "POST":
#         # 입력데이터랑 바인딩된 시리얼라이저 만들어주고 (그 먼젓번에 맨날 바인딩 폼 만들어서 save 해줬던 것처럼)
#         serializer = ArticleSerializer(data=request.data)
#         # 유효하면, (만약 유효하지 않으면 drf가 알아서 제공해주는 에러나는 이유 serializer.errors를 보낸다. 상태코드는 400(Bad request로)으로)
#         if serializer.is_valid(raise_exception=True):
#             # DB에 저장하고
#             serializer.save()
#             # 응답보내 created 상태코드인 201 띄워서. 
#             return Response(serializer.data, status.HTTP_201_CREATED)


# # 아티클 상세 조회 (밑에 구조는 다 비슷비슷하제?!)
# @api_view(["GET","PUT","DELETE"])
# def article_detail(request, pk):
#     # 일단 해당 아티클 들고오고
#     article = get_object_or_404(Article, pk=pk)
    
#     # 상세글 보겠다고 GET으로 왔으면
#     if request.method == "GET":
#     # pk에 해당하는 아티클 객체 조회해서 가져와라
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)
    
#     # 4️⃣ Update
#     # 해당 객체 수정하겠다고 PUT 메서드로 들어오면 
#     elif request.method == "PUT":
#         # 시리얼라이저에 기존 아티클 담아서 보여주고, 이거 수정해서 오는 데이터 직렬화해줘, 그리고 부분 필드만 수정하는 것도 가능하도록  partial=True 옵션을 줘
#         serializer = ArticleSerializer(article, data=request.data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)
        
#     # 3️⃣ Delete
#     # 해당 pk 객체 삭제하겠다고 delete 메서드로 들어오면
#     elif request.method == "DELETE":
#         # 해당 객체 삭제해줘
#         article.delete()
#         # 응답 띄울 거 만들어놓기
#         data = {"delete": f"Article({pk}) is deleted."}
#         # 응답띄우고 상태코드는 ok를 뜻하는 200으로 ~
#         return Response(data, status=status.HTTP_200_OK)





# APIView 클래스 : HTTP 요청(request)을 받아 적절한 메서드(GET, POST 등)를 호출

# 현재 함수 기반인 article_list 뷰를 APIview 클래스를 상속받아 클래스기반뷰로 만들어보자 
# 안쪽 로직 자체는 변동없음!!
class ArticleListAPIView(APIView):
    '''
    ⭐️ 이제부터는, 요청이 들어오면 응답으로 데이터를 활용한 템플릿을 보여주는 것이 아닌,
    DB의 데이터 그 자체를 JSON 으로 변환해서 응답으로 주는 것이라고 생각해라! ⭐️
    우리는 이제 데이터를 다루는 백엔드만에 관여하고, 템플릿은 백엔드가 응답으로 준 JSON 데이터를 프론트엔드가 활용해서 따로 처리할 것이다!
    
    전체 작동 흐름
    1. 클라이언트가 URL로 GET 또는 POST 요청을 보낸다.
    2. 요청의 HTTP 메서드에 따라 ArticleListAPIView 클래스의 get 또는 post 메서드가 호출된다.
    3. 메서드 내부에서 요청 데이터 또는 데이터베이스 정보를 처리한다.
    4. 처리 결과를 JSON 형태로 응답한다.
    
    ⭐️ 클래스 기반 뷰(Class-Based Views, CBV)를 사용할 때는 요청이 관련 클래스로 전달되고, 
    그 클래스의 인스턴스(뷰 객체)가 생성된 후 요청을 처리한다. 이 과정에서 그 클래스의 뷰 객체가 self가 된다.
    
    ⭐️ self 는 클래스의 '현재 인스턴스'(현재 뷰 객체)를 가리킨다. 이를 통해 클래스에서 제공하는 속성과 메서드를 사용할 수 있다.
    
    예를 들어, 클라이언트가 url로 GET 요청을 보내면, Django는 ArticleListAPIView 클래스의 인스턴스를 생성한다.
    이 인스턴스가 요청(request)을 처리하며, 이를 처리하기 위해 get 메서드를 호출한다.
    이때 self는 생성된 ArticleListAPIView 인스턴스를 가리킨다.
    마찬가지로, POST 요청이 들어오면 같은 방식으로 인스턴스가 생성되고, post 메서드가 호출된다.
    
    ❗️ 클래스 안에 메서드 이름을 get이라고 정의하면, GET 요청이 들어왔을 때 해당 메서드가 자동으로 호출된다. 
    이것은 APIView 클래스가 제공하는 기본 기능으로,  HTTP 요청의 메서드 이름과 클래스 내부 메서드 이름을 연결해준다.
    ➡️
    RESTful API 설계에서 HTTP 메서드(GET, POST, PUT, DELETE 등)는 각기 다른 작업(읽기, 생성, 수정, 삭제)을 처리하기 위해 사용된다.
    APIView는 이러한 RESTful 설계를 지원하기 위해 요청의 메서드와 뷰 메서드를 자동으로 연결해주는 기능을 제공한다.
    
    장고 백엔드의 경우, POST 같은 HTTP 메서드에 담겨 오는 데이터도 기본적으로 JSON 데이터이다!
    DRF는 JSON을 주요 데이터 형식으로 사용하며, 클라이언트가 보내는 데이터를 쉽게 처리할 수 있도록 설계되어 있다.
    예를 들어,
    POST 요청의 경우에는, '클라이언트가 보낸 JSON 데이터'를 ArticleSerializer 를 통해 검증하고, 
    유효하면 save() 메서드를 통해 역직렬화해서 (즉 JSON이 아닌 일반적인 데이터 구조로) DB에 저장한다는 거임!
    '''
    
    
    # 1️⃣ Read
    # 아티클 목록 조회해달라고 GET요청으로 들어왔으면
    def get(self, request):
      # 아티클 모델에 있는 객체 다 가져와서
        articles = Article.objects.all()
        # ⭐️ 가져온 객체를 직렬화(JSON 형식으로 변환)해주기
        # 가져온 객체가 현재 단일 객체가 아닌 상황이라 many=True를 넣어줘야 함
        serializer = ArticleSerializer(articles, many=True)
        # 시리얼라이저 안쪽에 data라는 속성으로 JSON 데이터가 들어있다. 이렇게 직렬화된 데이터를 HTTP 응답 객체로 감싸 클라이언트에게 반환하는 코드
        # 💡 가져온 객체 context에 담아서 템플릿한테 보내줘야 되는 거 아니냐고? 
        # ❌ drf 부터는 아예 백엔드만 하는 거라, 우리는 데이터를 조회하고 그걸 저장, 전송을 위한 데이터 구조로 변환(직렬화)해서 (이는 데이터의 구조는 유지하면서 추후 재구성이 가능한 포맷) 응답을 만들어주는 것이다!
        # 그럼 프론트엔드가 이 응답을 활용해서 다시 작업해서 템플릿을 만드는 것!
        return Response(serializer.data)
    
    # 2️⃣ Create
    # 아티클 생성하겠다고 POST 요청으로 바디에 JSON 데이터 담아왔으면
    # 💡 지금 풀스택 장고 공부하던거 생각해서 응?? 지금 뭐 템플릿에서 폼에 정보입력하고 그런 거 하나도 안했는데? 하고 헷갈릴 수 있는데,
    # 이거는 지금 템플릿에서 뭐 작업하고 다시 뷰로 보내고 이런 활동이 아니라, 포스트맨을 사용해서 API(앱과 프로그래밍으로 소통하는 것) 를 만들고 있는 거다!
    # 그니까 그냥 어 아티클 뷰인데 겟요청이 들어왔다? 아, 아티클 조회해달라는 거구나~ 하고 응답 만들어주고, 아티클 뷰인데 포스트 요청이 들어왔다? 아, 아티클 작성해서 데이터 보낸거구나~
    # 그니까, 이 클래스의 이름을 아티클리스트뷰가 아니라 아티클뷰라고 생각하면 덜 헷갈릴 것이다. 지금 교재랑 맞춰서 하느라 일단 저 이름으로 해놨음.
    def post(self, request):
        # 입력데이터랑 바인딩된 시리얼라이저 객체 만들어주고 (그 먼젓번에 맨날 바인딩 폼 만들어서 save 해줬던 것처럼)
        # 사용자가 보낸 데이터를 ArticleSerializer를 통해 검증하고 저장하기 위한 코드
        # DRF에서는 request.data 를 사용하여 클라이언트가 보낸 요청 데이터를 받을 수 있다.
        serializer = ArticleSerializer(data=request.data)
        # 입력데이터의 유효성이 검증되면, (만약 유효하지 않으면 drf가 알아서 제공해주는 에러나는 이유 serializer.errors를 보낸다. 상태코드는 400(Bad request)으로)
        if serializer.is_valid(raise_exception=True):
            # ❗️❗️save 메서드는 JSON 상태 그대로 DB 에 저장하는 것이 아니라, 역직렬화 과정을 거쳐 우리가 아는 기본적인 형태로 Article 모델의 인스턴스로 저장한다 ❗️❗️
            # ❗️ 그니까 Article 테이블에는, JSON 데이터가 아닌, 그냥 우리가 이때까지 봤던 일반적인 형태의 데이터로 저장되어 있는 것!! 단지 그걸 활용해서 응답을 줄 때 JSON 데이터 구조로 변환해서 주는 것❗️
            serializer.save()
            # DB에는 역직렬화해서 저장하지만, 응답을 줄 때는 201 상태코드(created)와 함꼐 직렬화된 데이터를 준다.
            return Response(serializer.data, status.HTTP_201_CREATED)


# 현재 함수 기반인 article_detail 뷰를 APIview 클래스를 상속받아 클래스기반뷰로 만들어보자 
# 이것 역시 안쪽 로직 자체는 변동없음! 겹치는 get_object_404만 새로 함수로 빼줬음 
class ArticleDetailAPIView(APIView):

	# 💡 두 번 이상 반복되는 로직은 함수로 빼자
    # 일단 해당 아티클 들고오고
    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    # 상세글 보겠다고 GET으로 왔으면
    def get(self, request, pk):
        # pk에 해당하는 아티클 객체 조회해서 가져와라 
        article = self.get_object(pk)
        # 가져온 객체 ArticleSerializer를 통해 직렬화해서 
        serializer = ArticleSerializer(article)
        # 응답으로 보내줌
        return Response(serializer.data)

    # 4️⃣ Update
    # 해당 객체 수정하겠다고 PUT 메서드로 들어왔으면
    def put(self, request, pk):
        article = self.get_object(pk)
        # 시리얼라이저에 기존 아티클 담아서 보여주고, 이거 수정해서 오는 데이터 직렬화해줘, 그리고 부분 필드만 수정하는 것도 가능하도록  partial=True 옵션을 줘
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # 3️⃣ Delete
    # 해당 pk 객체 삭제하겠다고 delete 메서드로 들어왔으면
    def delete(self, request, pk):
        article = self.get_object(pk)
        # 해당 객체 DB에서 삭제해줘
        article.delete()
        # 응답 띄울 거 만들어놓기. ## drf에서 응답은 JSON이어야 하므로 응답으로 줄 data도 Json 형식으로 적는다.
        data = {"pk": f"{pk} is deleted."}
        # 응답띄우고 상태코드는 ok를 뜻하는 200으로 ~
        return Response(data, status=status.HTTP_200_OK)