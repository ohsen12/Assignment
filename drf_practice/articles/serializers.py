from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        # 아티클 모델에 있는 데이터를 갖고 와서 serialize 할 거고
        model = Article
        # 필드는 다 사용해
        fields = "__all__"
