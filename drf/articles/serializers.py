from rest_framework import serializers
from .models import Article,Comment

'''
직렬화 (Serialization) : 모델 인스턴스를 JSON 데이터로 변환한다.
역직렬화 (Deserialization) : JSON 데이터를 Python 객체로 변환하고, 유효성 검증 후 모델 인스턴스로 저장한다.
'''

# ModelSerializer는 DRF에서 제공하는 직렬화 클래스이며, 특정 모델(Comment)과 자동으로 연결되고, 모델의 필드를 기반으로 직렬화 및 역직렬화를 자동으로 처리한다.

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

