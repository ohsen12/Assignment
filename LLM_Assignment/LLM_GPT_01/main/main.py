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

# exit가 입력되기 전까지 계속 대화할게
while True:
    # 사용자 입력 받기
    user_input = input("User: ")
    
    # "exit" 입력 시 대화 종료
    if user_input.lower() == "exit":
        print("exit를 눌러 대화를 종료합니다.")
        break
    
    # ⭐️ 사용자 입력 값을 대화 목록에 추가 (대화의 흐름을 기억시키기 위해)
    # simpletest.py 에서는 계속 처음 대화하는 거였음.
    messages.append({"role":"user", "content": user_input})

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
        # GPT 출력값을 대화 목록에 추가
        messages.append({"role":"assistant", "content": assistant_reply})
    
    # 권한 오류가 난다면
    except openai.error.AuthenticationError:
        print("Authentication error: API key is invalid or missing.")
        break
    # 그 밖의 오류가 난다면 해당 오류의 내용을 출력해주기
    except Exception as e:
        print(f"An error occurred: {e}")
        break
