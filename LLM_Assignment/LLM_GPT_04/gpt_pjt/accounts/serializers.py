from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    # 설정 정보를 정의하기 위한 내부 클래스
    class Meta:
        # 커스텀 유저 모델을 시리얼라이즈(직렬화)하겠다.
        # 현재 프로젝트에서 정의된 User 모델 사용
        model = get_user_model()
        fields = ['id','username','date_joined']
        
        
# ⭐️ 회원가입 시리얼라이저 
class UserCreationSerializer(serializers.ModelSerializer):
    # 지금 커스텀 유저 모델에는 패스워드를 받는 필드가 없음!
    # 회원가입 시 비밀번호와 비밀번호 확인 필드를 받을 수 있도록 추가. (폼에서 form.CharField 했던 것처럼, 역시나 시리얼라이저도 동일하게 진행한다.)
    # write_only=True: 응답 데이터(JSON)에서는 이 필드가 포함되지 않음. (입력받는 용도로만 사용)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        '''
        클라이언트가 JSON 형식으로 POST 요청을 보내는 예시..는 이미지 필드가 포함될 경우 엄청 복잡하길래 안 넣었음
        어쨌든 대충 'username', 'email', 'password', 'password2', 'profile_image' 얘네를 보낼 거임
        '''
        # 직렬화 대상 모델
        model = get_user_model()
        # 직렬화할 필드. 유저 모델에서 회원가입에 필요한 필드만 지정
        # 💡 fields에 지정하지 않은 필드를 클라이언트가 보내면, DRF는 기본적으로 직렬화 시 해당 필드를 무시한다. 즉, 클라이언트가 요청에 포함시킨 불필요한 필드는 시리얼라이저에서 처리되지 않고, 그 값은 직렬화 과정에서 제외된다.
        # fields에 정의되지 않은 필드는 직렬화 및 유효성 검사 과정에서 제외되며, 따라서 저장(save) 과정에도 포함되지 않는다.
        fields = ['id','username', 'email', 'password', 'password2']
    
    
    # ⭐️ 비밀번호 확인 (⭐️ 이거는 지금 퓨어장고의 UserCreationForm 같은 거를 상속받아서 하는 게 아니라, 그냥 일반 모델 시리얼라이저를 회원가입 시리얼라이저로 만드는 것이기 때문에 비밀번호 확인 로직은 직접 작성해줘야 한다!!)
    def validate(self, data):
        '''
        data는 serializer에 전달된 클라이언트 데이터를 내부적으로 처리한 결과.
        validate 메서드는 이 데이터를 기준으로 추가 검증을 수행.
        
        시리얼라이저가 매개변수로 받은 data에는 처음에는 request.data 가 담겼다가, 시리얼라이저가 필드별로 유효성을 검증한 후의 데이터가 담겨있다. 
        원래 시리얼라이저 자체적으로 필드별 유효성 검사 > validate() 메서드 호출 순서대로 진행된다.
        
        기본검증 로직만 있든, 추가 검증 로직까지 있든, 정의해놓은 유효성 로직을 모두 거치면 serializer.validated_data에 검증된 데이터가 저장됨!
        '''
        # 입력한 비밀번호와 비밀번호 확인이 같지 않으면
        if data['password'] != data['password2']:
            # 오류를 발생시키기
            raise serializers.ValidationError("Passwords do not match.")
        # 유효하다면 데이터를 그대로 반환
        # 💡 이 반환된 데이터는 serializer.validated_data에 저장된다! 이게 이제 바로 밑의 create 에서 사용되는 거임.
        return data


    def create(self, validated_data):
        # password2는 유저 모델에 저장하지 않아야 함 (데이터의 끝에 패스워드2 있을테니까 pop으로 validated_data에서 날려버림)
        validated_data.pop('password2')
        # create_user()를 사용하면, 유저의 비밀번호가 자동으로 해시되어 데이터베이스에 저장된다. 이렇게 해시 처리된 비밀번호는 안전하게 저장되며, 평문 비밀번호는 저장되지 않는다.
        # create() 메서드는 user 객체를 생성한 후, 해당 user 객체를 반환한다.
        user = get_user_model().objects.create_user(**validated_data)
        # create 메서드가 원래 DB에 인스턴스 생성하고 그 새로운 인스턴스를 반환하는 메서드임. 기본 create 메서드 대체하는 거니까 로직 똑같이 만들어주자 ~
        return user