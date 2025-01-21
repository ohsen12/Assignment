from rest_framework import serializers
from .models import Article,Comment

'''
직렬화 (Serialization) : 모델 인스턴스를 JSON 데이터로 변환한다.
역직렬화 (Deserialization) : JSON 데이터를 Python 객체로 변환하고, 유효성 검증 후 모델 인스턴스로 저장한다.

ModelSerializer는 마치 모델 폼처럼 기능하다.

Serializer는 기존 필드를 override 하거나 추가적인 필드를 구성할 수 있으며
이때 모델 사이에 참조 관계가 있다면 해당 필드를 포함하거나 중첩할 수 있다.

'''

# ModelSerializer는 DRF에서 제공하는 직렬화 클래스이며, 특정 모델(Comment)과 자동으로 연결되고, 모델의 필드를 기반으로 직렬화 및 역직렬화를 자동으로 처리한다.


# 댓글 시리얼라이저
# CommentSerializer는 Comment 모델의 데이터를 JSON으로 변환하거나, JSON 데이터를 Comment 모델 인스턴스로 변환하는 역할을 한다.
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        # 댓글 모델을 시리얼라이즈(직렬화)하겠다.
        model = Comment
        # 모델의 어떤 필드를 직렬화할 건데?
        # 모든 필드를.
        fields = "__all__"
        # 넘겨받은 데이터에 article 정보가 없기 때문에 어, 아티클 필드도 직렬화해야 되는데? 하고 serializer.is_valid를 통과하지 못한다.
        # 이를 방지하기 위해, article 필드를 직렬화 로직에 포함하지 않고 반환 값에만 필드를 포함하도록 한다.
        # 즉, 특정 필드를 읽기 전용으로 설정하는 옵션 (요청 시 직렬화에는 무시되고, 응답 시 직렬화에는 포함된다.)
        # 외래키(article)처럼 중요한 데이터가 클라이언트에 의해 수정되지 않도록 방지한다.
        read_only_fields = ("article",)
    
    # '직렬화 이후 보여지는 결과에 대해 자동으로 내부적으로 불리는' 함수.
    # 이 메서드를 오버라이드 하여 커스텀 형식으로 사용
    def to_representation(self, instance):
        # 직렬화된 댓글 객체가 보여지는 거
        ret = super().to_representation(instance)
        # 그거 맨 마지막에 어떤 아티클이랑 연결되어 있는지도 보여주는데, 그거 pop 시키겠음
        ret.pop("article")
        # 그리고 반환하겠음. 결국 최종적으로 이것만 응답으로 반환되겠지.
        return ret
        
        
# 게시글 시리얼라이저
# ArticleSerializer는 Article 모델의 데이터를 JSON으로 변환하거나, JSON 데이터를 Article 모델 인스턴스로 변환하는 역할을 한다.
class ArticleSerializer(serializers.ModelSerializer):
    # 설정 정보를 정의하기 위한 내부 클래스
    class Meta:
        # 게시글 모델을 시리얼라이즈(직렬화)하겠다.
        model = Article
        # 모델 중에서 어떤 필드를 직렬화할 건데?
        # 모든 필드를.
        fields = "__all__"
        
        

# 위의 아티클 시리얼라이즈의 필드 + 해당 게시글과 연결되어 있는 댓글도 필드로 만들어 직렬화 해주기
# 그리고 이 시리얼라이저는 게시글을 상세 조회할 때 사용하자. 상세 조회할 때 해당 게시글에 연결되어 있는 댓글 객체도 볼 수 있도록.
class ArticleDetailSerializer(ArticleSerializer):
    # 게시글에서 댓글을 역참조 매니저 comments (댓글 시리얼라이저를 먼저 정의하고 게시글 시리얼라이저에서 사용하면 된다.)
    # comments 라는 기존에 존재하는 매니저 이름으로 된 필드를 다시 override 
    # 댓글은 여러 개일 수 있으니 mant=True 옵션을 주고 그냥 게시글 조회할 때 댓글도 조회하려고 하는 거라 읽기 모드 옵션을 준다.
    comments = CommentSerializer(many=True, read_only=True)
    # comments 의 경우 Django가 자동으로 추가해주는 매니저이기에 바로 사용할 수 있었으나 comments_count 는 직접 필드를 추가해주는 것이 필요하다.
    # source 속성을 이용하여 데이터 값을 전달하는 것이 가능함.
    # 여기서 "comments.count" 는 장고 ORM 사용한 거임. 댓글 역참조 해서 개수를 세어라.
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

