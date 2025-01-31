from rest_framework import serializers
from .models import Chat



class ChatSerializer(serializers.ModelSerializer):
    # 설정 정보를 정의하기 위한 내부 클래스
    class Meta:
        # 커스텀 유저 모델을 시리얼라이즈(직렬화)하겠다.
        # 현재 프로젝트에서 정의된 User 모델 사용
        model = Chat
        # 모델 중에서 어떤 필드를 직렬화할 건데?
        # 이 시리얼라이즈로 직렬화해서 응답 반환하면 아래 필드의 직렬화된 결과만 나오는 거임
        fields = '__all__'