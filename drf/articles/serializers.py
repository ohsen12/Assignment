from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        # 아티클 모델을 기반으로 시리얼라이즈(직렬화)하겠다.
        model = Article
        # 모델 중에서 어떤 필드를 직렬화할 건데?
        # 모든 필드를.
        fields = "__all__"
