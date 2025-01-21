from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer


# 회원가입
class UserSignupView(APIView):
    # 이 뷰에 누구나 접근 가능하도록
    permission_classes = [AllowAny]

    def post(self, request):
        # 사용자 정보 받아오기
        serializer = UserSerializer(data=request.data)

        # 유효성 검사
        if serializer.is_valid():
            # 새 사용자 저장
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)