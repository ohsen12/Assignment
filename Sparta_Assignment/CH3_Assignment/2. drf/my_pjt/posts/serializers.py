from rest_framework import serializers
from .models import Post,Comment
from django.contrib.auth import get_user_model


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username"]  # 작성자 ID와 이름만 직렬화하여 제공 (Post 모델과 연결하는데는 이거면 충분)


# 댓글 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
    '''
    클라이언트가 댓글을 생성할 때 다음과 같이 요청을 보낼 수 있다.
    {
        "post": 1,
        "content": "This is a sample comment."
    }
    id 1번 포스트에 댓글을 달겠다는 뜻이다.
    
    댓글 생성 후 응답 JSON은 다음과 같다.
    {
        "id": 10,
        "post": {
            "id": 1,
            "title": "Sample Post"
        },
        "author": {
            "id": 3,
            "username": "example_user"
        },
        "content": "This is a sample comment.",
        "created_at": "2025-01-22T12:00:00Z",
        "updated_at": "2025-01-22T12:30:00Z"
    }
    1번 포스트에 달린, 작성자의 id가 3인, id 10번 댓글이라는 뜻이다.
    '''
    
    # ❗️ 이미 Comment 모델에 존재하는 필드를 관련 시리얼라이저를 사용하여 내용을 바꿔주는 것.
    
    # 작성자 정보를 AuthorSerializer를 통해 표현
    author = AuthorSerializer(read_only=True)
    # 댓글이 달린 게시글 정보를 PostSerializer에서 필요한 부분만 직렬화
    # SerializerMethodField는 특정 필드를 계산하거나 커스터마이즈된 형식으로 반환할 때 사용한다.(여기서는 get_post 메서드에서 계산된 값을 반환)
    post = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        exclude = ['created_at', 'updated_at']  # 제외할 필드를 설정
    
    # 게시글 정보에서는 게시글 id와 title 필드만 반환하도록 설정 (댓글에서 게시글 정보에 특정 필드만 반환하도록 설정)
    # 아, 그렇구나 ~
    def get_post(self, obj):
        '''
        get_post 메서드는 DRF의 SerializerMethodField와 함께 사용되는 메서드로,
        특정 필드의 값을 동적으로 생성하거나 원하는 방식으로 커스터마이즈할 때 활용한다.
        이 메서드에서 post 필드의 값을 반환할 방식을 정의한다.
        
        왜 사용?
        기본적으로 외래 키(ForeignKey) 필드는 참조하는 객체의 id만 반환한다.
        그렇기에, 이 메서드를 사용하여 post 객체의 id 외의 정보까지 포함해줄 수 있다.
        
        self: 현재 CommentSerializer 객체.
        obj: 직렬화하려는 댓글 인스턴스.
        '''
        # 이 반환값은 최종 직렬화 데이터에 포함된다.
        return {"id": obj.post.id, "title": obj.post.title}
    
    # ⭐️ 댓글 생성 시 author를 자동으로 설정
    def create(self, validated_data):
        user = self.context['request'].user  # 요청의 사용자 정보
        validated_data['author'] = user  # 작성자를 현재 요청의 사용자로 설정
        return super().create(validated_data)


# 게시글 시리얼라이저
# PostSerializer는 Post 모델의 데이터를 JSON으로 변환하거나(직렬화), JSON 데이터를 Post 모델 인스턴스로 변환하는(역직렬화) 역할을 한다.
class PostSerializer(serializers.ModelSerializer):
    '''
    Post 모델에 이미 존재하는 author 필드를(외래키로 연결해놓은 사용자 객체) AuthorSerializer를 사용하면, 
    작성자 정보를 보다 구체적이고 커스터마이즈된 형식으로 반환할 수 있게된다.
    AuthorSerializer를 통해 author 필드의 데이터를 어떻게 변환할지 정의한다.
    
    게시글 API에서 author 필드는 다음과 같은 형태로 포함된다.
    {
        "id": 1,
        "title": "Sample Post",
        "content": "This is a sample post.",
        "author": {
            "id": 42,
            "username": "example_user"
        },
        "created_at": "2025-01-21T12:00:00Z",
        "updated_at": "2025-01-21T12:30:00Z"
    }

    Post 모델의 author 필드를 별도로 정의하지 않으면, 기본적으로 작성자의 ID만 반환된다. 
    (그냥 Post 인스턴스만 직렬화해도 이미 외래키로 연결시켜놨으니까 작성자가 누구인지도 직렬화되긴 되네.. 
    근데 author 의 pk값만 담기니까, username 과 같이 좀 더 구체적인 정보를 담아주고 싶어서 사용하는 거군)
    '''
    # ⭐️ 이미 Post 모델에 존재하는 필드(외래키 필드가 있으면 역참조 필드가 자동으로 생성되지 ~)를 관련 시리얼라이저를 사용하여 내용을 덮어씌우는 것. (여기서는 작성자와 댓글에 대해서 구체적인 정보를 포함하도록 하고 싶어서.)
    # read_only=True는 작성자 정보가 클라이언트에서 수정되지 않도록 설정해주는 역할
    author = AuthorSerializer(read_only=True)
    # 게시글에 달린 댓글들을 직렬화하여 포함
    comments = CommentSerializer(many=True, read_only=True)
    
    
    # 설정 정보를 정의하기 위한 내부 클래스
    class Meta:
        # 게시글 모델을 시리얼라이즈(직렬화)하겠다.
        model = Post
        # 모델 중에서 어떤 필드를 직렬화할 건데?
        # comments 필드 추가
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'comments']
    
    # ⭐️ 클라이언트에서 author 필드를 보내지 않아도 로그인한 사용자가 자동으로 작성자로 설정되기 위한 오버라이딩
    # 뷰에서 처리하는 방법도 있는데, 그냥 한번에 시리얼라이저에서 해결하는 것이 더 좋은 코드라고 한다.
    def create(self, validated_data):
        # 글을 생성할 때 request.user를 자동으로 author로 설정
        user = self.context['request'].user
        # author는 로그인한 사용자로 설정
        validated_data['author'] = user  
        # 부모 클래스인 ModelSerializer의 create 메서드를 호출하여, validated_data를 직접 Post 모델 인스턴스로 변환하고, 이를 DB에 저장
        return super().create(validated_data)
    

