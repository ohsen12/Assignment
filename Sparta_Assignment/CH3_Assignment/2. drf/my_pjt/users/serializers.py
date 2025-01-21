from rest_framework import serializers
from django.contrib.auth import get_user_model


# 유저 시리얼 라이저
# UserSerializer는 커스텀 유저 모델의 데이터를 JSON으로 변환하거나, JSON 데이터를 커스텀 유저 모델 인스턴스로 변환하는 역할을 한다.
class UserSerializer(serializers.ModelSerializer):
    '''
    현재 커스텀 유저 모델에 이미지 필드도 있는데, 그 필드의 직렬화는 어떻게 이루어지는가?
    ➡️
    ImageField는 이미지 파일 '경로'(실제 파일이 서버에 저장된 위치 : 파일을 업로드하고 서버 측에서 해당 경로를 통해 직접 파일을 처리하는 경우에 사용)를 직렬화한다. 
    만약 이 필드를 포함하여 JSON 응답에서 이미지를 보여주려면 MEDIA_URL을 추가하는 등의 처리가 필요하다. 
    예를 들어, profile_image가 이미지 URL(사용자가 웹 브라우저를 통해 이미지에 접근할 수 있는 링크)로 직렬화되도록 하려면, to_representation 메서드를 오버라이드하여 URL을 반환하는 방법을 사용해야 한다.
    (웹에서 이미지 파일을 클라이언트에게 제공하고 싶다면, 이미지 URL로 직렬화하는 것이 더 적합하다는 점.)
    실무에서는 브라우저가 이미지에 쉽게 접근할 수 있도록 이미지 url 경로를 많이 사용한다.
    (Django는 MEDIA_URL과 MEDIA_ROOT 설정을 통해 파일 서버와 연동하여, 이미지 파일의 경로와 도메인을 합친 완전한 URL을 자동으로 생성해줌)
    '''
    # 설정 정보를 정의하기 위한 내부 클래스
    class Meta:
        # 커스텀 유저 모델을 시리얼라이즈(직렬화)하겠다.
        # 현재 프로젝트에서 정의된 User 모델 사용
        model = get_user_model()
        # 모델 중에서 어떤 필드를 직렬화할 건데?
        # 모든 필드를. (프로필 이미지를 포함한 모든 필드가 직렬화된다.)
        fields = "__all__"
        
        # 이미지 필드를 이미지 url 로 직렬화 처리하기 위한 방법
        # 기본 to_representation 메서드는 모델 인스턴스를 직렬화하여 Python 딕셔너리 형태로 반환
        # 이 메서드의 오버라이드를 통해 직렬화 과정에서 특정 필드를 어떻게 변환할지를 커스터마이징할 수 있다.
        def to_representation(self, instance):
            '''
            to_representation 메서드를 오버라이드하여, 이미지 필드를 파일 경로에서 이미지 URL로 변환하는 처리. 
            이 방법을 통해 이미지 파일 경로가 아닌 클라이언트에서 접근 가능한 URL로 반환되도록 할 수 있다.
            '''
            
            # super()는 부모 클래스인 ModelSerializer의 to_representation 메서드를 호출하는 코드
            # 기본 직렬화된 결과를 가져오는 코드
            representation = super().to_representation(instance)
            
            # profile_image 필드가 비어 있지 않다면
            if instance.profile_image:
                # 'profile_image' 필드를 경로에서 URL로 변환
                # instance.profile_image.url은 이미지 파일의 절대 URL을 반환
                # 이 URL을 직렬화된 결과 딕셔너리 representation에 profile_image 키의 value 값으로 넣어줌. 기존 거 대체.
                representation['profile_image'] = instance.profile_image.url  # 이미지 URL로 변환
            
            # 변환된 URL을 직렬화된 데이터에 반영하여, 클라이언트에게 전달되는 JSON 응답에 이미지 URL이 포함된다.
            return representation