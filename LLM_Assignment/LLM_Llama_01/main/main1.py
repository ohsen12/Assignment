'''
기존의 RNN 방식은 이름에서 알 수 있듯이 반드시 각 단계들을 순차적으로 진행했어야 했다.
하지만 Transformer 모델은 단순히 Attention(어떤 토큰에 더 가중치를 적용할 지 계산하는 기법) 만 하기 때문에 과정이 훨씬 짧아졌고 그로인해 학습시간이 단축되었다.

이 코드의 실행 결과는 입력된 프롬프트를 기반으로 Llama 2 모델이 텍스트를 생성하는 결과물을 출력한다.

📝 전체 실행 흐름
- 프롬프트 템플릿과 사용자 질문을 합쳐서 입력 텍스트를 만든다.
- 이 텍스트를 토큰화하여 모델에 입력할 준비를 한다.
- 모델이 텍스트를 생성하여 답변을 출력한다.
- 그 후, 실행 시간을 측정하여 얼마나 걸렸는지 출력한다.
'''

import logging # 파이썬에서 로그를 출력할 때 사용되는 표준 라이브러리
import time
import os
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM
import sqlite3  # SQLite 사용

# 로그의 기본 설정을 DEBUG 수준(DEBUG는 가장 낮은 수준의 상세한 정보를 기록한다.)으로 설정 (이렇게 하면 DEBUG 이상의 수준의 로그 메시지가 출력된다.)
logging.basicConfig(level=logging.DEBUG)

# 💊 모델 로딩 전에 디버깅 로그 추가
logging.debug("모델 로딩 시작")

# .env 파일을 불러오기
load_dotenv()

# 환경 변수에서 토큰 가져오기 (Hugging Face에서 인증을 요구하는 기능을 사용할 때 필요하다.)
# ❗️ 해당 파일의 meta-llama/Llama-2-7b-chat-hf 모델 같은 경우는 일반적으로 인증 없이 다운로드할 수 있기 때문에, 토큰 없이도 코드가 동작하긴 한다! (나중을 위한 예시 코드)
hf_token = os.getenv('HUGGINGFACE_TOKEN')

# 토크나이저 로드 (Llama-2 7B 모델의 토크나이저를 로드)
# AutoTokenizer는 텍스트를 모델이 이해할 수 있는 형식인 토큰으로 변환하는 역할을 한다.
# from_pretrained("meta-llama/Llama-2-7b-chat-hf")는 Llama 2 모델에 맞는 토크나이저를 불러오는 코드다. 이는 주어진 텍스트를 토큰화하여 모델에 전달할 수 있도록 한다.
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

# 모델 로드와 CPU 메모리 최적화를 위한 옵션들
# AutoModelForCausalLM: 텍스트 생성을 위한 언어 모델을 로드하는 클래스
model = AutoModelForCausalLM.from_pretrained(
    # Llama-2 7B 모델을 Hugging Face에서 가져온다.
    "meta-llama/Llama-2-7b-chat-hf",
    # Mac M1 환경에 따라 안정성을 위해 CPU를 사용하도록 강제한다.
    device_map="cpu", 
    # 모델이 너무 커서 메모리 부족이 우려되므로, 일부 데이터를 디스크에 저장하도록 지정한다.
    offload_folder="offload",
    # 모델의 상태(dict)를 디스크로 오프로드하여 메모리 사용을 최적화한다.
    offload_state_dict=True
)

# 💊 모델 로딩 완료 로그
logging.debug("모델 로딩 완료")


# 📦 SQLite DB 연결 및 테이블 생성 함수
def create_db():
    '''
    이 함수는 SQLite 데이터베이스를 생성하고, conversations라는 테이블을 만든다.
    대화 내용을 저장할 테이블이 존재하지 않으면 새로 생성하며, 존재하면 기존 테이블을 그대로 사용한다.
    
    테이블은 conversation_id (PRIMARY KEY로 지정되어, 각 대화는 고유한 ID를 가지게 된다.), 
    speaker (주체자. "user" 또는 "computer"), message (대화 내용) 컬럼을 가진다.
    
    sqlite3.connect()를 호출하여 SQLite 데이터베이스 파일인 chat_db.sqlite에 연결한다. 
    만약 chat_db.sqlite 파일이 존재하지 않으면, 이 명령으로 파일이 자동으로 생성된다.
    
    커서(cursor)는 SQL 명령을 데이터베이스에 실행하기 위한 객체다. 
    conn.cursor()로 데이터베이스 작업을 할 수 있는 커서를 만든다.
    
    cursor.execute()로 SQL 쿼리를 실행하여 conversations 테이블을 만든다.
    commit()은 커서로 실행한 SQL 명령을 데이터베이스에 실제로 적용하는 명령이다.
    모든 작업이 끝난 후, conn.close()로 데이터베이스 연결을 종료한다.
    '''
    # SQLite 데이터베이스 연결 (파일이 없으면 자동으로 생성됨)
    conn = sqlite3.connect('chat_db.sqlite')
    cursor = conn.cursor()
    
    # 대화 내용 저장을 위한 테이블 생성 (💡 IF NOT EXISTS: 테이블이 이미 존재하면 새로 만들지 않도록 하며, 테이블이 없으면 새로 생성)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            speaker TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# 📦 대화 내용을 DB에 저장하는 함수
def save_conversation_to_db(speaker, message):
    '''
    대화의 주체자와 내용을 받아서, 이를 conversations 테이블에 저장한다.
    speaker는 "user" 또는 "computer"로 구분되며, message는 실제로 주고 받은 대화 내용을 의미한다.
    
    sqlite3.connect('chat_db.sqlite')로 chat_db.sqlite 데이터베이스에 연결한다. 
    이 파일이 없다면, 자동으로 생성된다. 
    
    conn.cursor()로 커서 객체를 만든다. 커서는 SQL 명령을 실행할 때 필요한 객체로, 데이터베이스와의 상호작용을 담당한다.
    
    cursor.execute()로 SQL 명령을 실행한다.
    INSERT INTO: conversations 테이블에 새로운 레코드를 추가하는 SQL 명령이다.
    ?는 파라미터 바인딩을 위한 자리 표시자이다. 이 자리에 실제 값인 speaker와 message가 들어간다.
    즉, INSERT INTO conversations (speaker, message) VALUES (?, ?)는 **speaker**와 **message**를 테이블의 각 컬럼에 삽입하는 명령이다.
    
    commit()은 데이터베이스에 변경 사항을 반영하는 명령이다. 이 단계에서 INSERT된 대화 내용이 실제로 데이터베이스에 저장된다.
    
    모든 작업이 끝나면, conn.close()를 호출하여 데이터베이스 연결을 종료한다. 이를 통해 연결된 리소스가 해제된다.
    '''
    
    # DB에 연결
    conn = sqlite3.connect('chat_db.sqlite')
    cursor = conn.cursor()
    
    # 대화 내용 INSERT (cursor.execute()로 SQL 명령을 실행)
    cursor.execute('''
        INSERT INTO conversations (speaker, message) 
        VALUES (?, ?)
    ''', (speaker, message))
    
    conn.commit()
    conn.close()


# 프롬프트 템플릿 (모델이 주어진 질문에 대해 답변을 생성하는 형식을 정의한 템플릿)
# {question} 자리에 사용자가 입력한 질문을 넣을 수 있다.
prompt_template = """
You are an employee at a café that specializes in traditional Korean drinks. 
Your role is to provide detailed information about these drinks and their cultural significance. 
For each drink, you should describe its ingredients, preparation method, and why it holds significance in Korean culture. 
You should also be able to answer any questions about the history, variations, and modern adaptations of these drinks. 
Please describe one of the traditional Korean drinks in detail.

Question: {question}

Provide a detailed answer:

"""


# 프롬프트 템플릿의 {question} 자리에 들어갈 사용자 입력 데이터 (질문)
input_data = {
    "question": "Do you have any drinks you would recommend at this café?"
}

# 템플릿에 사용자 질문 삽입
# .format() 메서드를 사용해 input_data의 "question" 값을 prompt_template에 삽입하고 그걸 prompt 변수에 넣어준다.
prompt = prompt_template.format(**input_data)

# 실행(텍스트 생성) 시작 시간 기록
start_time = time.time()

# 입력을 토크나이저로 처리하여 모델에 입력할 수 있는 형태로 변환
# ⭐️ tokenizer를 사용하여 완성된 prompt를 '토큰화'한다. ⭐️ 모델은 텍스트를 그대로 처리할 수 없으므로, 이를 숫자 형태로 변환해야 한다.
# return_tensors="pt"는 PyTorch 텐서를 반환하도록 지정한다. 이렇게 하면 텐서 형식으로 입력을 모델에 전달할 수 있다.
inputs = tokenizer(prompt, return_tensors="pt")

# 모델을 통한 텍스트 생성
# model.generate(): 모델이 입력된 토큰들을 기반으로 텍스트를 생성하는 함수이다.
# tokenizer의 출력은 input_ids를 포함한 여러 키를 가지기 때문에, 명시적으로 input_ids의 값을 추출해야 한다.
outputs = model.generate(input_ids=inputs["input_ids"], max_length=150)

# 출력된 텍스트 디코딩(생성된 텍스트를 디코딩하여 사람이 읽을 수 있는 형식으로 변환)
# outputs[0]: 모델이 생성한 첫 번째 텍스트 시퀀스
# ⭐️ tokenizer.decode(): '숫자로 된 토큰'을 다시 '사람이 읽을 수 있는 텍스트로' 변환한다.
# skip_special_tokens=True: 생성된 텍스트에서 특수 토큰(예: [PAD], [UNK] 등)을 제외하고 출력한다.
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

# 대화 내용 DB에 저장
save_conversation_to_db("user", input_data["question"]) # 사용자 질문 저장
save_conversation_to_db("computer", generated_text) # 모델의 응답 저장

# 대화 출력
print(generated_text)

# 종료 시간 기록
end_time = time.time()

# 코드 실행 전후 시간을 기록하여, 최종 실행 시간을 계산한다. (보통 일반 컴퓨터에서는 20분 이상 걸림)
execution_time = end_time - start_time
# 최종 실행 시간 출력 (.2f는 소수점 이하 2자리까지 표시하도록 하는 포맷 지정자)
print(f'\n실행 시간 : {execution_time:.2f}초\n')