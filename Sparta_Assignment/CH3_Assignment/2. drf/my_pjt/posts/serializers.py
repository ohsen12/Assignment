from rest_framework import serializers
from .models import Post
from django.contrib.auth import get_user_model


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username"]  # 작성자 ID와 이름만 직렬화하여 제공 (Post 모델과 연결하는데는 이거면 충분)


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
    # ❗️ 이미 Post 모델에 존재하는 필드를 관련 시리얼라이저를 사용하여 내용을 바꿔주는 것. (여기서는 작성자에 대한 더 구체적인 정보를 포함하도록 하고 싶어서.)
    # read_only=True는 작성자 정보가 클라이언트에서 수정되지 않도록 설정해주는 역할
    author = AuthorSerializer(read_only=True)
    
    # 설정 정보를 정의하기 위한 내부 클래스
    class Meta:
        # 게시글 모델을 시리얼라이즈(직렬화)하겠다.
        model = Post
        # 모델 중에서 어떤 필드를 직렬화할 건데?
        # 모든 필드를.
        fields = "__all__"