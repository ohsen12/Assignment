from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserCreationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


# 회원가입
class UserSignupView(APIView):
    # 회원가입 로직이니까 이 뷰에 누구나 접근 가능하도록
    permission_classes = [AllowAny]

    def post(self, request):
        # 바인딩 시리얼라이저 만들어주기
        serializer = UserCreationSerializer(data=request.data)
        # 유효성 검사
        # ⭐️ is_valid 메서드 호출 시, 먼저 시리얼라이저 자체에서 필드 별 검증 로직을 수행하고, 시리얼라이저의 추가 검증로직인 validate 메서드가 실행됨 ⭐️ validate()는 전체 데이터를 추가적으로 검증하는, DRF가 특정 이름으로 호출하도록 설계된 메서드 ❗️ 일개 메서드가 아님. (이 메서드들이 DRF의 유효성 검사 프로세스에서 호출되는 시점은 이미 프레임워크 내부적으로 정해져 있기 때문에, 우리가 따로 호출하지 않아도 작동함.)
        # validate 메서드에서 password와 password2가 같은지 확인하고 실패하면 오류메세지를 반환한다.
        # ⭐️ validate 메서드까지 거치면 serializer.validated_data에 검증된 데이터가 저장됨!
        if serializer.is_valid(raise_exception=True):
            # 유효성 검사를 통과하면 DB에 저장. (ModelSerializer를 사용하는 것이기 때문에 해당 시리얼라이저를 통해 데이터를 save하면 현재 유저 모델에 저장된다. 즉, 회원가입 완료!)
            user=serializer.save() 
            # 원래 serializer.data 응답하려고 했는데, 이러면 회원가입할 때 입력한 비밀번호 등의 정보가 다 나오는 거니까 그냥 성공했으면 성공했다는 메세지만 띄우자
            return Response({"id": user.id, "username":user.username}, status=status.HTTP_201_CREATED)


# 💡 인증(로그인)과 함께 진행되어야 할 엑세스, 리프레시 토큰 발급은 url 에서 TokenObtainPairView 클래스 뷰와 연결하여 해결한다.


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
    ❗️ 백엔드에서는 리프레시 토큰을 블랙리스트에 추가해 사용 불가능하게 만드는 방식으로 로그아웃 처리를 하며, 액세스 토큰의 만료나 삭제는 클라이언트에서 담당하는 부분이다.)
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
        

# 회원탈퇴
class UserDeleteView(APIView):
    # 현재 로그인한 사용자만 회원탈퇴 가능함(당연)
    permission_classes = [IsAuthenticated]
    
    # 회원탈퇴(회원을 DB에서 삭제하는 작업)를 위해 DELETE 방법으로 들어오면
    def delete(self, request):
        # 로그인한 사용자를 DB에서 삭제한다.
        request.user.delete()
        # 성공 메세지 반환
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    