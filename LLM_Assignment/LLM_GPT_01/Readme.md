# 🤖 Transformer 모델

### 개요
```
Transformer 모델은 자연어 처리(NLP)와 컴퓨터 비전(Computer Vision) 등 다양한 분야에서 혁신을 이룬 딥러닝 모델이다. 
2017년 논문 "Attention is All You Need"(Vaswani et al.)에서 처음 소개되었으며, 특히 자연어 처리 작업에서 기존의 순환 신경망(RNN)이나 LSTM(Long Short-Term Memory)을 대체하는 데 성공하였다.
Transformer는 Self-Attention 메커니즘과 병렬 처리를 통해 빠르고 효율적으로 대규모 데이터를 학습할 수 있는 구조를 제공한다.
```

### 주요 구성 요소

1. 인코더-디코더 구조

Transformer는 일반적으로 인코더와 디코더로 구성된 구조를 가진다.

- 인코더(Encoder): 입력 시퀀스를 처리하고 고차원 표현 벡터로 변환한다.

- 디코더(Decoder): 인코더 출력과 디코더의 이전 출력을 기반으로 다음 단어를 생성한다.

특정 작업에 따라 인코더만 사용하는 BERT나 디코더만 사용하는 GPT와 같은 변형된 구조도 존재한다.

2. Self-Attention 메커니즘

Self-Attention은 입력 데이터의 각 단어가 문맥적으로 다른 단어와 어떤 관계를 가지는지를 계산하는 핵심 메커니즘이다. 이를 통해, 문장의 중요한 단어들 간의 상호작용을 효율적으로 학습할 수 있다.

<details>
    <summary>
       Self-Attention 계산 과정
    </summary>

- Query(Q), Key(K), Value(V): 입력 데이터로부터 생성된 행렬이다.

- Attention 점수: Query와 Key 간의 내적(dot product)을 통해 유사도 점수를 계산한다.

- Softmax: 유사도 점수를 확률 분포로 변환한다.

- Weighted Sum: 확률 분포를 Value에 가중합하여 최종 출력을 생성한다.
  
</details>

###

3. Positional Encoding

Transformer는 RNN처럼 순차적으로 데이터를 처리하지 않기 때문에 위치 정보를 학습하기 위해 Positional Encoding을 추가한다. 이 값은 단어의 위치 정보를 벡터로 변환해 입력에 더해준다.

### ⭐️ 장점
1. 병렬 처리: RNN 계열 모델과 달리 시퀀스를 병렬로 처리하므로 학습 속도가 빠르다.

2. 효율적인 문맥 학습: Self-Attention 메커니즘을 통해 긴 문맥도 효과적으로 학습 가능하다.

3. 확장성: BERT, GPT, T5 등 다양한 변형 모델이 발전하여 여러 작업에 적합한 아키텍처로 확장되었다.

### 단점

1. 메모리 소모: Attention 연산의 복잡도가 O(n^2)이므로 긴 시퀀스 처리 시 메모리 요구량이 크다.

2. 데이터 요구량: 모델 성능을 극대화하려면 대규모 데이터와 컴퓨팅 자원이 필요하다.

### Transformer 기반 주요 모델

1. BERT (Bidirectional Encoder Representations from Transformers)

- 인코더 구조만 사용한다.

- 문맥의 양방향 정보를 학습한다.

- 주로 문장 분류, 개체명 인식, 질의응답 작업에 사용된다.

2. ⭐️ GPT ⭐️(Generative Pre-trained Transformer)

- 디코더 구조만 사용한다.

- 문맥의 한 방향(왼쪽에서 오른쪽) 정보를 학습한다.

- 주로 텍스트 생성 작업에 사용된다.

3. T5 (Text-to-Text Transfer Transformer)

- 인코더-디코더 구조를 모두 사용한다.

- 텍스트 입력과 출력 모두를 텍스트 형태로 처리한다.

- 번역, 요약, 문장 완성 등에 사용된다.

4. Vision Transformer (ViT)

- Transformer를 이미지 처리에 적용한 모델이다.

- 이미지를 패치(patch) 단위로 분할하고, 이를 입력 시퀀스로 변환해 학습한다.

### Transformer의 응용 분야

1. 자연어 처리: 기계 번역, 텍스트 생성, 요약, 질의응답 등.

2. 컴퓨터 비전: 이미지 분류, 객체 탐지 등.

3. 음성 처리: 음성 인식 및 합성.

4. 추천 시스템: 사용자 행동 예측 및 추천.

<hr>

# 🏙️ OpenAI

OpenAI는 GPT(Generative Pre-trained Transformer) 모델을 포함한 다양한 트랜스포머 기반의 모델을 사용하여 서비스를 제공하는 기업이다. 
GPT 모델은 대규모 언어 모델로, 텍스트 생성, 번역, 요약 등 다양한 자연어 처리 작업을 수행할 수 있다. 
이 모델은 대량의 텍스트 데이터를 학습하여 언어의 패턴과 구조를 이해하고, 주어진 텍스트에 기반해 자연스러운 응답을 생성하는 방식으로 작동한다.

➡️ OpenAI는 API를 통해 자사의 GPT 모델을 비롯한 여러 모델을 외부 애플리케이션에서 사용할 수 있도록 제공하고 있다.
➡️ 우리는 OpenAI 의 API를 사용하여 자신의 프로그램에서 자연어 처리 기능을 통합하거나, 텍스트 생성, 질문 답변, 번역, 요약 등 다양한 AI 서비스를 손쉽게 활용할 수 있다.

### OpenAI의 API를 어떻게 사용하는데?

전반적인 과정은 다음과 같다.

먼저 OpenAI의 계정을 만들고 API 키를 발급받아야 한다. 
그 후, 이를 자신의 코드에서 호출하여 원하는 기능을 구현할 수 있다. 
API는 HTTP 요청을 통해 쉽게 연동할 수 있으며, 다양한 언어에서 사용할 수 있는 클라이언트 라이브러리도 제공된다.

### 그전에, API가 뭐에요?

다음의 링크를 확인하자.

⚙️ [API(Application Programming Interface)](https://tpsdms12.tistory.com/148)