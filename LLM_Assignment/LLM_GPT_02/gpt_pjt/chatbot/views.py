import openai
# 내 운영체제
import os
# 환경변수 관리해주는 모듈
from dotenv import load_dotenv
import requests
from django.shortcuts import render, redirect
from .forms import ChatForm
from .models import Message
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required


# .env 파일을 로드해서 환경 변수로 설정하면서 .env 파일 로드
load_dotenv()

# 사용자 인증을 위한 API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# ⭐️ OpenAI API URL (gpt-3.5-turbo 모델을 사용할 경우 이 엔드포인트 URL을 통해 GPT 모델과 상호작용한다.)
API_URL = "https://api.openai.com/v1/chat/completions"


@login_required
@require_http_methods(["GET","POST"])
def chat_view(request):
    '''
    뷰에서 사용자가 입력한 대화를 GPT 모델에 전달하고, 응답을 받아 DB에 저장한 뒤,
    결과를 보여줄 템플릿(페이지)으로 리디렉션한다.
    
    세션은 해당 유저에게 고유한 데이터로, 장고에서 세션은 각 사용자의 요청에 대해 별도의 데이터를 저장하고 관리할 수 있는 방법을 제공한다.
    따라서, 동일한 사용자에 대해 세션을 사용하면 각 사용자마다 별도의 데이터가 저장되고, 다른 사용자와 세션 데이터가 공유되지 않는다. 
    예를 들어, A 사용자와 B 사용자가 각각 대화하는 경우, A의 대화 흐름과 B의 대화 흐름은 서로 영향을 미치지 않는다.
    
    세션은 사용자가 브라우저를 닫지 않거나 세션이 만료되지 않는 한, 여러 페이지를 이동하면서도 계속 유지된다.
    ⭐️ 하지만, 사용자가 로그아웃하거나 탈퇴할 때는, 로그아웃 함수가 작동하여 세션 정보를 초기화해주기 때문에,
    다시 로그인했을 때 데이터베이스에서 대화기록은 사라지지 않아도, gpt 모델은 사용자를 기억하지 못한다!
    
    물론, 세션과 데이터베이스는 별개의 작업이기 때문에 사용자의 대화 기록을 데이터베이스에서 삭제한다고 하더라도, 해당 사용자의 세션에 저장된 대화 기록에는 영향을 미치지 않는다.
    데이터베이스의 기록을 지우는 것은 단지 그냥 DB에서 '기록'을 지우는 것이고, 세션에는 모델이 이전 대화의 문맥들을 기억하기 위해 이전까지의 대화를 저장해둔 것이다!
    '''
    # 💡 응답 요청하기 전 세션을 이용하여 messages 매개변수 전처리
    
    # 유저의 세션에 메시지 데이터가 없으면 초기화
    if 'messages' not in request.session:
        # 대화의 흐름을 세션에 저장 (세션에 'messages'라는 키에 시스템의 역할을 넣어서 초기화해줌)
        request.session['messages'] = [{"role": "system", "content": "너의 이름은 '김춘식'이다. 모든 문장에 느낌표와 이모지를 적극 활용하여 발랄하고 활기찬 뉘앙스를 사용해라. 사용자의 말에 공감의 말을 하며 대화를 이어가야 한다."}]
    # 이미 대화를 했어서 사용자의 메시지 기록이 세션에 남아있으면
    else:
        # 세션에서 messages(대화 흐름)에 담긴 데이터를 가져와서 messages 매개변수 초기화
        messages = request.session['messages']
    
    
    if request.method == 'POST':
        form = ChatForm(request.POST)
        # 사용자의 입력이 유효하다면
        if form.is_valid():
            # 폼의 검증된 데이터인 cleaned_data (딕셔너리 형태)에서 user_input 필드의 값을 키로 추출하여 변수에 저장
            user_input = form.cleaned_data['user_input']
        
            # OpenAI API 요청 설정
            
            # OpenAI API에 요청을 보낼 때 필요한 HTTP 헤더
            headers = {
                # 요청 본문이 JSON 형식임을 지정
                "Content-Type": "application/json",
                # Bearer 토큰 방식으로 인증
                # 권한의 베리어 토큰에 나의 키 넣음 (drf할 때 요청 헤더에 엑세스 토큰 집어넣어야 했던 거 생각해!)
                "Authorization": f"Bearer {openai.api_key}"
            }

            data = {
                "model": "gpt-3.5-turbo",  # 사용할 모델
                # chat 모델을 사용할 때는 messages라는 리스트로 대화의 흐름을 전달해야 한다.
                # 이전 대화와 함께 사용자 메시지 추가 (리스트끼리 더하면 안의 객체들끼리 쉼표로 연결되지~)
                "messages": messages + [{"role": "user", "content": user_input}],
            }
            
            # GPT 모델의 응답 받기
            # 응답 변수에, POST 방식으로 사용자의 입력값을 담아 GPT-3 모델의 엔드포인트로 보낸 후에 돌려받은 JSOM 응답 데이터 담아주기.
            # requests 라이브러리의 post() 메서드를 사용해, OpenAI API에 POST 요청을 보낸다.
            response = requests.post(API_URL, headers=headers, json=data)
            
            # 모델 응답 초기화 해놓기 (만약 이렇게 기본값을 지정해놓지 않으면 에러로 응답이 오지 않았을 때 이 변수가 초기화되지 않았는데 이후에 사용하려고 해서 에러가 발생한다.)
            gpt_response = "GPT 모델에서 응답을 받을 수 없습니다."
            
            try:
                # API 요청이 성공했으면
                if response.status_code == 200:
                    # JSON 응답에서 GPT 모델의 응답 텍스트를 추출
                    gpt_response = response.json()["choices"][0]["message"]["content"]
                    
                    # 대화 흐름을 기억하기 위해 messages 매개변수에 사용자의 입력값과 모델의 응답을 누적
                    messages.append({"role":"user", "content": user_input})
                    messages.append({"role":"assistant", "content": gpt_response})
                    
                    # 세션에 대화 흐름 업데이트 (결국 세션에는 messages 라는 키의 value 로 프롬프트 명령과 사용자의 입력값, 그리고 모델의 응답이 누적된 딕셔너리 리스트 형태의 데이터가 들어있을 것!)
                    request.session['messages'] = messages
                    
            # API 요청이 실패했으면
            except Exception as e:
                # 터미널에서 왜 실패했는지 해당 에러메세지 출력
                print(f"\nAn error occurred: {e}\n")

            
            # 💡 사용자와 모델 간의 대화를 DB에 저장해주기 
            
            # 폼의 데이터를 저장하되 아직 DB에 반영하지 않음(왜냐? 아직 Message 모델 필드들 중 필수 필드인 get_response와 user가 저장되지 않았기 때문)
            message = form.save(commit=False)
            # 필수 필드들 수동으로 저장해주기
            message.gpt_response = gpt_response
            message.user = request.user
            # 필수 필드를 모두 채운 후 DB에 저장
            message.save()

            # 대화 내용을 보여주는 페이지로 리디렉션 (chat_history url로 요청을 보낸다. 그럼 이제 이 url 패턴에서 chat_history 뷰로 요청을 넘깁)
            return redirect('chatbot:chat_history')
            
    # 대화 입력하려고 링크 타고 GET 요청으로 들어왔으면
    else:
        # 사용자 입력 폼
        form = ChatForm()
        # 템플릿으로 던져주기
        context = {"form":form}
        return render(request, "chatbot/chat_view.html", context)
    

# 대화 기록 url타고 들어오면 이 뷰로 연결돼서 로직이 처리된다.
@login_required
def chat_history(request):
    # DB에 저장된 요청 유저만의 대화 기록을 최신순으로 들고와서 
    messages = Message.objects.filter(user=request.user).order_by('-created_at')
    # context에 담아 템플릿으로 보내주기 (템플릿에서 이를 for 문으로 돌리며 화면에 보여줄 것임)
    context = {"messages":messages}
    return render(request, "chatbot/chat_history.html", context)


# 나의 대화 기록 전체 삭제하기
@login_required
@require_POST
def chat_delete(request):
    chat = Message.objects.filter(user=request.user)
    chat.delete()
    return redirect("chatbot:chat_history")



