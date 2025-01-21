from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer


# 💡 APIView 클래스 : HTTP 요청(request)을 받아 적절한 메서드(GET, POST 등)로 연결(호출)


class PostAPIView(APIView):
    '''
    posts/ 라는 url로 들어왔을 때 HTTP 메서드에 따라 그에 맞는 get 메서드나 post 메서드를 호출하여 로직을 처리한다.
    '''
    # Read (게시글 목록 조회)
    def get(self, request):
        # Post 모델(게시글 테이블)에 있는 인스턴스 전부 가져오기
        posts = Post.objects.all()
        # ⭐️ 가져온 객체를 시리얼라이저를 통해 직렬화(JSON 형식으로 변환) 해주기 (가져온 객체가 단일 객체가 아니라서 many=True를 넣어줘야 함)
        serializer = PostSerializer(posts, many=True)
        # 직렬화 객체 안쪽에 data라는 속성으로 JSON 데이터가 들어있다. 
        # 이렇게 직렬화된 데이터를 HTTP 응답 객체로 감싸 반환한다. (그럼 프론트엔드 단에서 이거 받아서 활용해서 사용자에게 시각적인 최종 결과물을 제공하는 것!)
        return Response(serializer.data)
    
    # Create (게시글 생성)
    def post(self, request):
        # 전달된 입력데이터랑 바인딩된 시리얼라이저 객체 만들어주고 (⭐️ 퓨어장고에서 form이 하던 역할을 drf에서는 시리얼라이저가 대체한다! 유효성 검사 이런 거 다 해줌.)
        # drf에서는 request.data 를 사용하여 클라이언트가 요청에 보낸 데이터를 받을 수 있다.
        serializer = PostSerializer(data=request.data)
        # 입력데이터의 유효성이 검증되면, (raise_exception=True : 만약 유효하지 않으면 drf가 알아서 상태코드 400(Bad request)와 함께 에러나는 이유를 내려준다.)
        if serializer.is_valid(raise_exception=True):
            # ⭐️ save 메서드는 JSON 상태 그대로 DB 에 저장하는 것이 아니라, '역직렬화' 과정을 거쳐 우리가 아는 기본적인 형태의 Post 모델의 인스턴스로 저장한다 ⭐️
            serializer.save()
            # DB에는 역직렬화해서 저장하지만, 응답을 줄 때는 201 상태코드(created)와 함꼐 직렬화된 데이터를 준다. (그래야 프론트엔드가 이 데이터 받아서 다른 작업에 활용함!)
            return Response(serializer.data, status.HTTP_201_CREATED)
    