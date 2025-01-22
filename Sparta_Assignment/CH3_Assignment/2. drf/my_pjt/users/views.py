from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, UserCreationSerializer
from rest_framework_simplejwt.tokens import RefreshToken


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
        

# 인증(로그인)과 엑세스, 리프레시 토큰 발급은 url 에서 TokenObtainPairView 와 TokenRefreshView 클래스 뷰에서 해결한다.

# 로그아웃
class UserLogoutView(APIView):
    '''
    클라이언트는 로그아웃을 요청할 때 리프레시 토큰을 POST 방식으로 서버에 보낸다.
    그럼 UserLogoutView는 사용자가 보낸 리프레시 토큰을 서버에서 무효화하는 작업을 수행한다.
    {
        "refresh_token": "<refresh_token>"
    }
    서버는 이 리프레시 토큰을 받아 해당 토큰을 블랙리스트에 추가하여 더 이상 사용할 수 없게 만든다.
    이를 통해 현재 로그인할 때 사용했던 엑세스 토큰이 만료되는 순간 로그아웃을 완전하게 처리할 수 있다!
    
    ⭐️ 물론, 로그아웃 후 액세스 토큰이 만료되지 않았을 경우, 서버는 액세스 토큰을 계속 유효하다고 인식한다. 
    이 문제는 클라이언트에서 액세스 토큰을 삭제하거나 액세스 토큰의 유효 기간을 짧게 설정하는 방식으로 처리할 수 있다.
    (백엔드에서 로그아웃을 처리하는 것과 별개로, 클라이언트가 리프레시 토큰을 서버로 보내고 나면, 클라이언트 측에서는 해당 액세스 토큰을 삭제하거나 만료된 토큰을 새로 고침하여 사용할 수 있도록 해야 한다.
    그러니까, 클라이언트 측에서 액세스 토큰을 삭제하는 작업은 백엔드에서 할 일이 아니며, 클라이언트 애플리케이션에서 처리해야 한다.
    백엔드에서는 리프레시 토큰을 블랙리스트에 추가해 사용 불가능하게 만드는 방식으로 로그아웃 처리를 하며, 액세스 토큰의 만료나 삭제는 클라이언트에서 담당하는 부분이다.)
    '''
    
    # 로그아웃을 요청하는 사용자가 인증된 사용자여야만 접근할 수 있다는 것을 의미한다. 
    # 즉, 액세스 토큰을 보유한 사용자가 로그아웃을 요청할 수 있다.
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 요청에서 보낸 refresh_token을 꺼낸다.
            refresh_token = request.data.get("refresh_token")
            # 만약 요청에 담겨온 리프레시 토큰이 없다면
            if not refresh_token:
                return Response({"detail": "No refresh token provided"}, status=400)

            # 리프레시 토큰을 받아 RefreshToken 클래스를 사용해 토큰 객체를 만든다.
            token = RefreshToken(refresh_token)
            # token.blacklist()는 이 리프레시 토큰을 블랙리스트(DB의 블랙리스트 테이블에)에 추가하는 메서드이다.
            # 블랙리스트에 추가된 토큰은 더 이상 유효하지 않게 되어, 이 리프레시 토큰으로는 새로운 액세스 토큰을 발급받을 수 없다. 
            # 현재 사용자의 엑세스 토큰이 만료되면 더 이상 로그인 후 사용가능한 서비스가 이용불가하게 된다. 그런 것들은 요청 헤더에 사용자 본인의 유효한 엑세스 토큰을 담아 보내야 사용가능한 거니까.
            token.blacklist()

            # 성공 응답
            return Response({"detail": "Successfully logged out"}, status=200)
        
        # try 블록 내에서 예외가 발생하면 파이썬은 즉시 except 블록을 실행한다.
        # ⭐️ 예외처리(토큰이 유효하지 않거나 블랙리스트에 추가할 때 문제가 생기면)
        # 발생한 예외 객체를 변수 e 에 담아 사용한다.
        except Exception as e:
            return Response({"detail": str(e)}, status=400)