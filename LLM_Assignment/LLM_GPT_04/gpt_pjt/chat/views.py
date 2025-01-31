import openai
import os
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ChatSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Chat


# .env 파일을 로드해서 환경 변수로 설정하면서 .env 파일 로드
load_dotenv()

# API key 설정 (내 운영체제에 있는 OPEN_API_KEY 라는 이름의 환경변수를 가지고 와서 API의 키로 설정해)
openai.api_key = os.getenv("OPENAI_API_KEY")

# 💊 디버깅용
api_key = os.getenv("OPENAI_API_KEY")

# API 키가 로드되지 않았을 경우 예외 처리
if not api_key:
    raise ValueError("API key is missing. Please check your .env file.")
else:
    print("\nAPI key successfully loaded.\n")


# GPT와 대화하기
class Chat_With_GPTAPIView(APIView):
    
    # 로그인한 회원만 가능
    permission_classes = [IsAuthenticated]
     
    def post(self, request):
        
        # POST 요청으로 받은 메시지를 들고 오는데, 디폴트 값은 빈 문자열(사용자가 요청에 message라는 키의 value로 보낸 메시지가 없으면 그냥 빈문자열로 반환. KeyError 방지)
        user_input = request.data.get("message", "")

        # 사용자 입력 메시지가 없다면
        if not user_input:
            return Response({"error": "메시지를 입력하세요."}, status=400)
        
        # 사용자 입력 메시지가 있다면
        else:
            # 사용자의 입력 메시지에 대한 모델의 응답 생성
            try:
                # 현재 사용자 ID 가져오기
                user = request.user

                # ⏰ 해당 사용자의 최근 대화 기록 불러오기(최대 5개만 가져와 불필요한 데이터 누적 방지, 최신순 정렬)
                # ⭐️ 대화의 흐름을 기억하도록 하려면, 사용자의 이전 대화를 DB에서 불러와서 messages 리스트에 포함해야 한다.
                previous_chats = Chat.objects.filter(user=user).order_by('-created_at')[:5]

                messages = [{"role": "system", "content": "You are a helpful assistant."}]
                
                # ⏰ 대화 기록을 messages 리스트에 추가
                # DB에서 불러온 대화 기록을 messages 매개변수에 추가(messages 매개변수는 리스트 안에 여러 개의 딕셔너리가 있는 구조이다.)
                for chat in reversed(previous_chats):  # 오래된 기록부터 추가해야 흐름 유지됨
                    messages.append({"role": "user", "content": chat.user_input})
                    messages.append({"role": "assistant", "content": chat.gpt_response})

                # 현재 사용자 입력 추가
                messages.append({"role": "user", "content": user_input})
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                # 응답 추출
                gpt_response = response["choices"][0]["message"]["content"]
                
                # ChatSerializer를 통한 DB 저장을 위한 서식 준비
                chat_data = {
                    "user_input": user_input,
                    "gpt_response": gpt_response,
                    "user": user.id
                }
                
                # 바인딩 시리얼라이저 생성
                serializer = ChatSerializer(data=chat_data)
                # 유효성 검사
                if serializer.is_valid(raise_exception=True):
                    # 유효하면 DB에 저장
                    serializer.save()
                
                return Response({"user":request.user.username, "message": user_input, "response": gpt_response})
            
            # 응답 생성 시도 과정 중 오류가 나면 에러 메시지 출력
            except Exception as e:
                return Response({"error": str(e)}, status=500)
            

# 회원의 대화 기록 삭제
class Chat_DeleteAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        # 해당 회원의 대화 객체를 전부 들고와서
        chat = Chat.objects.filter(user=request.user)
        # 만약 이전 대화기록이 없다면
        if not chat:
            return Response({"message": f"There is no history for '{request.user.username}'."})
        # 이전 대화기록이 있다면
        else:
            # DB에서 삭제
            chat.delete()
            # 삭제됐다고 알려주기
            return Response({"message": f"All chat history for '{request.user.username}' has been deleted."})
