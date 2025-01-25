import openai
# 내 운영체제
import os
# 환경변수 관리해주는 모듈
from dotenv import load_dotenv

# .env 파일을 로드해서 환경 변수로 설정하면서 .env 파일 로드
load_dotenv()

# API key 설정 (내 운영체제에 있는 OPEN_API_KEY 라는 이름의 환경변수를 가지고 와서 API의 키로 설정해)
# ⭐️ simpletest.py 에서 키를 코드에 직접 노출했던 것과 달리, 실제로는 이런 식으로 가져와서 사용해야 한다!
openai.api_key = os.getenv("OPENAI_API_KEY")


# 💊 디버깅용
api_key = os.getenv("OPENAI_API_KEY")

# API 키가 로드되지 않았을 경우 예외 처리
if not api_key:
    raise ValueError("API key is missing. Please check your .env file.")
else:
    print("\nAPI key successfully loaded.\n")

# 프롬프트 명령 변수에 담아주기 
prompt = "너의 이름은 '김춘식'이다. 너는 사용자의 '자존감을 끌어올리는 자존감 지킴이'이다. 모든 문장에 느낌표와 이모지를 적극 활용하며 사용자에게 칭찬과 격려의 말을 해야 한다. 사용자의 말에 공감의 말을 해야 한다. 해결책이 있을 경우 제시해라."

# 초기 대화 설정
messages = [{"role":"system", "content":prompt}]

# 📝 대화 기록 파일 설정
# 코드에서 이 변수를 통해  현재 디렉터리에 있는 gpt_conversation_log.txt 파일을 가리키게 된다.
log_file_path = "gpt_conversation_log.txt"

# 📝 대화 기록 함수
def log_conversation(user_input, assistant_reply):
    '''
    사용자의 입력값과 그에 대한 모델의 응답을 매개변수로 받아, 
    텍스트 파일에 추가해주는 대화 기록 함수.
    
    open: 파일을 여는 함수
    log_file_path: 기록할 파일의 경로를 나타내는 변수(기록할 파일의 위치와 이름을 지정하는 변수)
    "a"는 "append" 모드로 파일을 연다. 기존 파일 내용은 유지하고, 새 내용을 파일의 끝에 추가한다. 만약 파일이 존재하지 않으면 새로 생성한다!
    💡 현재 루프가 돌아갈 때마다 기존 파일에 새로운 응답을 추가해야 되니까 쓰기 모드 W(기존 파일 내용을 모두 지우고 새로 작성)를 사용하면 안된다.
    encoding="utf-8": 파일을 UTF-8로 인코딩하여 저장한다. (한글뿐만 아니라 이모지까지 깨지지 않게 저장해줌!)
    with 문: 파일을 열고 닫는 작업을 자동으로 처리 (파일 작업이 끝나면 자동으로 파일을 닫아 자원을 해제하여 메모리 누수나 오류 방지)
    write(): 파일 객체의 메서드로, 문자열 데이터를 파일에 작성(저장)할 때 사용된다.
    '''
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"User: {user_input}\n")
        log_file.write(f"GPT: {assistant_reply}\n\n")

# exit가 입력되기 전까지의 대화 루프
while True:
    # 사용자 입력 받기
    user_input = input("User: ")
    
    # "exit" 입력 시 대화 종료
    if user_input.lower() == "exit":
        print("exit를 눌러 대화를 종료합니다.")
        break
    
    # 1. 응답을 생성하기 위한 messages 구조 완성을 위한 코드 (ChatCompletion.create 메서드를 사용하기 위한 messages라는 매개변수의 구조를 사용자에게 입력 받은 내용을 사용해 완성하기 위함. 위에 messages 보면 아직 모델의 역할을 정해준 부분밖에 없어 미완성 상태였음.)
    # 2. 그 이후부터는 대화의 흐름을 기억시키기 위한 코드 (💡 GPT는 messages에 대화 내용을 누적해서 전달해줌으로써 이전 대화 내용을 문맥으로 삼아 응답을 생성한다.)
    # 매번 messages에 이전 대화 내용을 계속 추가(append)함으로써 GPT가 대화의 흐름을, 즉 문맥을 고려하며 이해할 수 있다.
    # OpenAI 모델은 messages 리스트의 가장 마지막 항목을 "가장 최신"으로 인식하기 때문에 어쨌든 리스트의 끝에 있는 발화(가장 최신 사용자의 입력값)가 현재 대화의 문맥을 형성하는 핵심이다. (이전 메시지도 참고하지만, 최신 메시지가 가장 강력한 지침 역할을 한다.)
    messages.append({"role":"user", "content": user_input})

    # 완성된 messages 로 응답 생성하기 (이를 사용해 만들어진 응답은 response에 담긴다.)
    try:
        response = openai.ChatCompletion.create(
            # GPT3.5로 설정
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        # GPT의 응답을 변수에 담음
        assistant_reply = response['choices'][0]['message']['content']
        
        # 응답 출력
        print(f"GPT: {assistant_reply}\n")
        
        # 📝 이번 루프의 사용자의 입력값과 모델의 응답을 대화 기록 파일에 저장
        log_conversation(user_input, assistant_reply)
        
        # GPT 응답값을 대화 목록에 추가 (GPT의 응답도 messages에 누적하기 위한 코드)
        # 이렇게 하면 GPT가 자신의 이전 응답까지 포함해 문맥을 이해하며 더 일관된 대화를 이어갈 수 있다.
        messages.append({"role":"assistant", "content": assistant_reply})
    
    # 권한 오류가 난다면
    except openai.error.AuthenticationError:
        print("Authentication error: API key is invalid or missing.")
        break
    
    # 그 밖의 오류가 난다면 해당 오류의 내용을 출력해주기
    except Exception as e:
        print(f"An error occurred: {e}")
        break
