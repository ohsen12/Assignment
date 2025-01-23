from rest_framework import status
# 요거는 drf 에서 함수형 뷰를 만들 때 꼭 달아줘야 하는 데코레이터(여기선 사용한하는데 그냥 참고하라고 ~)
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, LikedUsersSerializer
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


# 💡 APIView 클래스 : HTTP 요청(request)을 받아 적절한 메서드(GET, POST 등)로 연결(호출)
# drf(백엔드)의 역할은 url로 HTTP 요청이 들어오면 해당 로직 수행해서 JSON 응답(response)을 주는 것!


class PostAPIView(APIView):
    '''
    posts/ 라는 url로 들어왔을 때 HTTP 메서드에 따라 그에 맞는 get 메서드나 post 메서드를 호출하여 로직을 처리한다.
    
    post 요청에서 보내는 JSON 데이터의 예시
    {
        "title": "New Post Title",
        "content": "This is the content of the new post.",
        "author": 42  # 작성자 ID (ForeignKey)
    }
    여기서 author 필드는 ForeignKey이기 때문에, 실제로 커스텀 유저 모델에 존재하는 사용자 id를 전달해야 한다.
    '''
    # 이 뷰에 인증된(로그인한) 사용자만 접근 가능하도록 (요청을 통해 해당 뷰에 접근하기 전 사용자가 인증된 상태인지를 확인한다.)
    # 사용자가 인증되지 않으면 403(Forbidden) 에러를 반환한다.
    permission_classes = [IsAuthenticated] 

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
        # request.user를 시리얼라이저에서 사용할 수 있도록 context에 담아 전달
        serializer = PostSerializer(data=request.data, context={'request': request})
        
        # 입력데이터의 유효성이 검증되면, (raise_exception=True : 만약 유효하지 않으면 drf가 알아서 상태코드 400(Bad request)와 함께 에러나는 이유를 내려준다.)
        if serializer.is_valid(raise_exception=True):
            # ⭐️ save 메서드는 JSON 상태 그대로 DB 에 저장하는 것이 아니라, '역직렬화' 과정을 거쳐 우리가 아는 기본적인 형태의 Post 모델의 인스턴스로 저장한다 ⭐️
            # 지금 시리얼라이저에서 create 메서드를 오버라이드 했으니 save 메서드를 호출할 때 그리로 넘어간다.
            serializer.save()
            # 💊 디버깅 코드
            print(f"\n\nSaved Post ID: {serializer.instance.id}\n\n")  # 저장된 포스트 ID 출력(시리얼라이저 객체 자체에는 author 가 없으니 조심해야 한다!)
            # DB에는 역직렬화해서 저장하지만, 응답을 줄 때는 201 상태코드(created)와 함꼐 직렬화된 데이터를 준다. (그래야 프론트엔드가 이 데이터 받아서 다른 작업에 활용함!)
            return Response(serializer.data, status.HTTP_201_CREATED)


class PostDetailAPIView(APIView):
    '''
    posts/<int:post_pk>/ 라는 url로 들어왔을 때 HTTP 메서드에 따라 그에 맞는 get, put, delete 메서드를 호출하여 로직을 처리한다.
    '''
    # 인증된(로그인한) 사용자만 접근 가능하도록
    permission_classes = [IsAuthenticated] 
    
    # 일단 넘어온 pk 값에 해당하는 게시글 가져와
    def get_object(self, post_pk):
        return get_object_or_404(Post, pk=post_pk)
    
    # Read (상세글)
    def get(self, request, post_pk):
        # post 에 해당 모델 인스턴스를 담아주고
        post = self.get_object(post_pk)
        # 직렬화해서
        serializer = PostSerializer(post)
        # 직렬화 객체 안에 data 속성으로 저장된 JSON 데이터를 응답으로 넘겨줌
        return Response(serializer.data)
    
    # Update (상세글 수정)
    def put(self, request, post_pk):
        post = self.get_object(post_pk)
        # 클라이언트가 어떻게 수정하겠다고 JSON 데이터를 put 요청으로 넘겨줬음
        # ⭐️ 기존 객체(post)와 클라이언트가 수정용으로 보낸 데이터를 결합하여 다시 바인딩? 시리얼라이저 객체를 생성 
        serializer = PostSerializer(post, data=request.data, partial=True)
        # 입력한 데이터가 유효할 때
        if serializer.is_valid(raise_exception=True):
            # 이제 save()를 호출하면, 역직렬화된 데이터로 DB의 기존 인스턴스가 업데이트된다.
            serializer.save()
            # 업데이트된 데이터를 JSON 응답으로 줘
            return Response(serializer.data)


    # Delete (상세글 삭제)
    def delete(self, request, post_pk):
        # 해당 Post 인스턴스 들고와서
        post = self.get_object(post_pk)
        # DB에서 삭제
        post.delete()
        # JSON 응답으로 만들 거 딕셔너리로 만들어놓기. 
        # 💡 Python의 딕셔너리는 JSON 구조와 유사하여 딕셔너리를 JSON으로 변환하거나, JSON 데이터를 딕셔너리로 변환할 수 있다.
        data = {"pk": f"{post_pk} is deleted."}
        # 💡 drf에서 Response 객체에 딕셔너리를 전달하면, '내부적으로 자동으로 JSON 형식으로 변환'하여 클라이언트에 반환한다.
        # JSON 응답을 상태코드 200(ok)와 함께 반환한다.
        return Response(data, status=status.HTTP_200_OK)
    
    
# 댓글
class CommentAPIView(APIView):
    """
    posts/<int:post_pk>/comments/ 로 들어오거나
    posts/<int:post_pk>/comments/<int:comment_pk>/ 로 들어올 예정
    뷰에 해당 변수를 받을 매개변수 자리를 만들어놔야겠지!
    
    특정 게시글의 댓글 목록 조회 및 댓글 생성 (GET, POST)
    특정 댓글 조회, 수정, 삭제 (GET, PUT, DELETE)
    """
    
    # 코드 중복 방지
    def get_post(self, post_pk):
        # post_pk에 해당하는 게시글 가져오기
        return get_object_or_404(Post, pk=post_pk)

    def get_comment(self, post, comment_pk):
        # post에 속한 특정 comment 가져오기
        return get_object_or_404(Comment, post=post, pk=comment_pk)


    # Read
    # 특정 댓글의 아이디 comment_pk 값은 전달 안 왔으면 디폴트값 None으로 지정
    def get(self, request, post_pk, comment_pk=None):
        # 일단 해당 게시글(post_pk)의 모든 댓글 가져오기
        post = self.get_post(post_pk)
        
        # 댓글의 pk 값이 넘어왔으면 posts/<int:post_pk>/comments/<int:comment_pk>/ 로 들어왔다는 거니까
        # 특정 게시글의 특정 댓글 조회
        if comment_pk:
            comment = self.get_comment(post, comment_pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        
        # 댓글의 pk 값이 안 넘어왔으면 그냥 posts/<int:post_pk>/comments/ 로 들어왔다는 거니까
        # 특정 게시글의 전체 댓글 조회
        else :
            comments = post.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

    
    # Create
    # 특정 게시글에 댓글 생성
    def post(self, request, post_pk):
        post = self.get_post(post_pk)
        # 시리얼라이저에서 작성자 자동으로 설정해주기 위해 request 객체 넘겨줌 (시리얼라이저에서 request.user를 통해 로그인한 사용자를 자동으로 댓글의 author 필드에 설정)
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            # 댓글의 작성자(author)는 시리얼라이저에서 request.user를 통해 자동으로 설정됐기 때문에
            # save 할 때는 게시글만 지정해주면 됨.
            serializer.save(post=post)  # 게시글(post) 정보를 설정
            return Response(serializer.data, status=status.HTTP_201_CREATED)


    # Upadate
    # 특정 게시글의 특정 댓글 수정
    def put(self, request, post_pk, comment_pk):
        post = self.get_post(post_pk)
        comment = self.get_comment(post, comment_pk)
        
        serializer = CommentSerializer(comment, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            # author와 post는 시리얼라이저에서 자동 처리되므로 굳이 재설정할 필요 없음
            serializer.save()
            return Response(serializer.data)
    
    
    # Delete
    # 특정 게시글의 특정 댓글 삭제
    def delete(self, request, post_pk, comment_pk):
        post = self.get_post(post_pk)
        comment = self.get_comment(post, comment_pk)
        comment.delete()
        return Response({"message": f"Comment {comment_pk} deleted."}, status=status.HTTP_204_NO_CONTENT)
    
    
# 좋아요
class LikePostAPIView(APIView):
    '''
    posts/<int:post_pk>/like/ 로 요청을 보내면 각각의 HTTP 메서드에 따라 좋아요 로직을 수행한다.
    '''
    # 로그인한 사용자만 접근 가능
    permission_classes = [IsAuthenticated] 
    
    # 코드 중복 방지
    def get_post(self, post_pk):
        # post_pk에 해당하는 게시글 가져오기
        return get_object_or_404(Post, pk=post_pk)
    
    # ✅ 해당 게시글에 달린 좋아요 개수는 게시글 상세 API에서 조회 가능하다.
    
    # 상세 게시글에 좋아요 누른 회원목록 조회
    def get(self, request, post_pk):
        # 일단 해당 게시글 갖고와
        post = self.get_post(post_pk)
        # 게시글 좋아요 누른 회원목록 직렬화해서
        serializer = LikedUsersSerializer(post)
        # 응답으로 넘겨주기
        return Response(serializer.data)
        
    
    # 좋아요 생성 
    def post(self, request, post_pk):
        # 일단 해당 게시글 갖고와
        post = self.get_post(post_pk)

        # 해당 게시글의 likes 필드에 이미 현재 유저가 존재하는 상황이라면 (이미 해당 게시글에 좋아요를 누른 상황)
        if post.likes.filter(id=request.user.id).exists():
            # 이미 좋아요를 눌렀는데 또 좋아요 생성하겠다고 이 url 패턴으로 POST 요청을 보내면 안되세요 🙏
            return Response({"detail": "해당 유저는 이미 이 게시글에 좋아요를 눌렀습니다."}, status=status.HTTP_400_BAD_REQUEST)
        # 해당 게시글의 likes 필드에 현재 유저가 존재하지 않는다면 (해당 게시글에 좋아요를 누르지 않은 상황)
        else:
            # likes 필드에 현재 유저 추가해주기
            # add()는 ManyToManyField에서 중간 테이블에 새로운 관계를 추가하는 작업을 수행한다.
            post.likes.add(request.user)
            return Response({"detail": "좋아요가 추가되었습니다."}, status=status.HTTP_200_OK)

    # 좋아요 삭제
    def delete(self, request, post_pk):
        # 일단 해당 게시글 갖고와
        post = self.get_post(post_pk)

        # 해당 게시글의 likes 필드에 현재 유저가 존재하지 않는 상황이라면 (if not False > if True 로 되어 조건문 실행)
        if not post.likes.filter(id=request.user.id).exists():
            # 좋아요를 누르지도 않았는데 이 url 패턴으로 DELETE 요청을 보내면 안되세요 🙏
            return Response({"detail": "헌재 유저는 이 게시글에 좋아요를 누르지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
        # 해당 게시글의 likes 필드에 현재 유저가 존재하는 상황이라면 (if not True > if False 로 되어 else 문으로 넘어옴)
        else:
            # likes 필드에서 현재 유저 삭제해주기
            # remove()는 ManyToManyField에서 중간 테이블의 관계를 삭제하는 작업을 한다.
            post.likes.remove(request.user)
            return Response({"detail": "좋아요가 취소되었습니다."}, status=status.HTTP_200_OK)