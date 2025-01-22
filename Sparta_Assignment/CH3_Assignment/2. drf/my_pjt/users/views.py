from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, UserCreationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



# 회원가입
class UserSignupView(APIView):
    # 회원가입 로직이니까 이 뷰에 누구나 접근 가능하도록
    permission_classes = [AllowAny]

    def post(self, request):
        # 클라이언트가 넘겨준 회원가입을 위한 데이터를 사용하여 바인딩 시리얼라이저 만들어 주기 (직렬화 해주기)
        # 이제 이 데이터가 UserCreationSerializer의 data 매개변수로 전달됨. data=request.data 이렇게 적어놓은 거 보이지 !!
        # 이 시점부터 시리얼라이저는 data를 기반으로 검증을 진행하거나, 나중에 save() 메서드를 호출해서 해당 데이터를 이용해 모델 인스턴스를 생성할 준비를 하게 됨!
        # 물론 이 코드 자체만으로는 유효성 검사를 진행하는 게 아님! 단지 바인딩 시리얼라이저만 만들어놨을 뿐.
        # request.data는 일반 텍스트 데이터를 처리하고, request.FILES는 파일 업로드 데이터를 처리한다. 회원가입 시 이미지 파일도 포함되므로 request.FILES를 함께 넘겨줘야 한다.
        serializer = UserCreationSerializer(data=request.data, files=request.FILES)
        # 유효성 검사
        # ⭐️ is_valid 메서드 호출 시, 먼저 시리얼라이저 자체에서 필드 별 검증 로직을 수행하고, 시리얼라이저의 추가 검증로직인 validate 메서드가 실행됨 ⭐️ validate()는 전체 데이터를 추가적으로 검증하는, DRF가 특정 이름으로 호출하도록 설계된 메서드 ❗️ 일개 메서드가 아님. (이 메서드들이 DRF의 유효성 검사 프로세스에서 호출되는 시점은 이미 프레임워크 내부적으로 정해져 있기 때문에, 우리가 따로 호출하지 않아도 작동함.)
        # validate 메서드에서 password와 password2가 같은지 확인하고 실패하면 오류메세지를 반환한다.
        # ⭐️ validate 메서드까지 거치면 serializer.validated_data에 검증된 데이터가 저장됨!
        if serializer.is_valid(raise_exception=True):
            # 유효성 검사를 통과하면, create() 메서드가 호출되어 유저 객체가 생성됨
            serializer.save()  # 여기서 create() 메서드가 호출됨 (원래 직접 정의해놓지 않았으면 알아서 내부적으로 create() 메서드를 호출해서 저장하는데, 내가 직접 시리얼라이저에 create 메서드를 정의해놓았으니까, 거기서 지정해놓은 로직을 따라감. 이거는 퓨어 장고랑 다르게 그냥 일반 모델시리얼라이저로 만든거라, create 메서드를 직접 정의해서 암호를 해시화해서 저장하는 등의 추가로직을 거쳐줘야 했음.)
            # 원래 serializer.data 응답하려고 했는데, 이러면 회원가입할 때 입력한 비밀번호 등의 정보가 다 나오는 거니까 그냥 성공했으면 성공했다는 메세지만 띄우자
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        

# 로그인
class UserLoginView(APIView):
    # 로그인하려는 로직이니까 이 뷰에 누구나 접근 가능하도록
    permission_classes = [AllowAny]

    def post(self, request):
        # 로그인이니까 클라이언트가 사용자의 username 과 password 를 POST 요청에 담아 보내줬을 것. (회원가입 폼 기억나지?)
        # 그거 꺼내와서 변수에 할당
        username = request.data.get('username')
        password = request.data.get('password')

        # 사용자 인증
        user = authenticate(username=username, password=password)
        
        if user:
            # 토큰 생성
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)