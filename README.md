- **숫자 맞추기 게임**
    
    ## 1. 숫자 맞추기 게임
    
    ### **과제 내용**
    
    1. 플레이어와 컴퓨터가 참여하는 숫자 맞추기 게임을 만드세요.
    2. 프로그램은 다음과 같은 기능을 포함해야 합니다.
    - 컴퓨터는 1부터 10 사이의 랜덤한 숫자를 생성합니다.
    - 플레이어는 숫자를 입력하고, 입력한 숫자가 큰지 작은지 힌트를 얻습니다.
    - 플레이어가 숫자를 맞힐 때까지 위 과정을 반복합니다.
    
    ### **입출력 예시**
    
    ```python
    1과 10 사이의 숫자를 하나 정했습니다.
    이 숫자는 무엇일까요?
    예상 숫자: 5
    너무 큽니다. 다시 입력하세요.
    예상 숫자: 4
    너무 큽니다. 다시 입력하세요.
    예상 숫자: 3
    정답입니다!
    ```
    
    ### **추가 도전 과제**
    
    1. 플레이어가 입력한 숫자가 범위를 벗어날 경우, 적절한 안내 메시지를 출력하여 유효한 범위 내의 숫자를 입력하도록 유도하세요.
    2. 플레이어가 게임을 반복하고 싶을 경우, 게임 재시작 여부를 묻고 그에 따라 게임을 초기화하거나 종료하는 기능을 추가하세요.
- **클래스와 함수 사용하기**
    
    # 2.  클래스와 함수 사용하기
    
    ### **과제 내용**
    
    이름, 성별, 나이를 입력받고, 이를 출력하는 프로그램을 작성해주세요.
    
    ### **처리 조건**
    
    - **클래스 정의**
        - `Person`이라는 이름의 클래스를 정의한다.
    - **멤버 변수**
        - `name`, `gender`, `age`라는 멤버 변수를 설정한다.
        - 각 변수는 객체가 생성될 때 초기화된다.
            - `name`: 이름을 저장하는 변수 (문자열)
            - `gender`: 성별을 저장하는 변수 (문자열, "male" 또는 "female")
            - `age`: 나이를 저장하는 변수 (정수형)
    - **생성자**
        - 생성자 `__init__`를 통해 객체 생성 시 이름, 성별, 나이를 초기화한다.
        - 매개변수로 이름(`name`), 성별(`gender`), 나이(`age`)를 받는다.
    - **정보를 출력하는 함수 `display()`**
        - `name`, `gender`, `age` 값을 출력하는 기능을 구현한다.
        - 이름과 성별은 같은 행에 출력하고, 나이는 다음 행에 출력한다.
    - **입력 및 출력**
        - 사용자로부터 나이, 이름, 성별을 각각 입력받는다.
        - 입력된 값을 바탕으로 `Person` 객체를 생성하고, `display()` 함수를 통해 객체의 정보를 출력한다.
    
    **예시 입출력**
    
    **사용자 입력 예시**
    
    ```python
    나이: 28
    이름: 페이커
    성별: male
    ```
    
    **출력 예시**
    
    ```python
    이름: 페이커, 성별: male
    나이: 28
    ```
    
    ### **추가 도전 과제**
    
    1. `Person` 클래스 생성자에서 사용자의 성별 입력값에 대한 유효성 검사를 추가해주세요.
    - **참고**
        - `gender` 값이 `male` 또는 `female`로만 입력될 수 있도록 제한하는 로직을 넣으면 됩니다.
        - 잘못된 입력이 들어오면 오류 메시지를 출력하고, 올바른 성별을 입력받을 때까지 반복해서 입력을 받도록 구현할 수 있습니다.
        
        ```python
        나이: 28
        이름: 페이커
        성별: 남성
        잘못된 성별을 입력하셨습니다. 'male' 또는 'female'을 입력하세요.
        성별:
        
        ```
        
    2. `Person` 클래스에 나잇대에 맞는 인사 메시지를 출력할 수 있도록 `greet()` 함수를 추가해주
    - **참고**
        - *`greet() 함수`*는 `age` 값에 따라 다음과 같은 메시지를 출력합니다.
        
        ```python
        나이: 28
        이름: 페이커
        성별: male
        이름: 페이커, 성별: male
        나이: 28
        안녕하세요, 페이커! 성인이시군요!
        
        ```
        
- **Python 라이브러리로 데이터 분석하기**
    
    ## 3. Python 라이브러리로 데이터 분석하기
    
    ### **과제 내용**
    
    - Python 라이브러리를 활용하여 주어진 데이터(.xlxs)를 분석 Quiz를 수행해주세요.
    
    ### **과제 수행을 위한 데이터 다운로드**
    
    [관서별 5대범죄 발생 및 검거.xlsx](https://prod-files-secure.s3.us-west-2.amazonaws.com/d6409e25-bd68-47fe-a3e5-94c8b0e29283/e96cdcc2-884b-4a2b-9722-222b99f6deeb/%EA%B4%80%EC%84%9C%EB%B3%84_5%EB%8C%80%EB%B2%94%EC%A3%84_%EB%B0%9C%EC%83%9D_%EB%B0%8F_%EA%B2%80%EA%B1%B0.xlsx)
    
    [pop_kor.csv](https://prod-files-secure.s3.us-west-2.amazonaws.com/d6409e25-bd68-47fe-a3e5-94c8b0e29283/6202f3a7-1bcf-4e66-913f-c6030d3eccd7/pop_kor.csv)
    
    - 인구자료 데이터⤴️
    
    ### 과제 수행 방법
    
    1. 다운로드 한 데이터 파일(.xlxs)을 열고 어떤 데이터인지 먼저 파악합니다.
    2. 과제 수행에 필요한 Python 라이브러리를 불러옵니다.
    3. Quiz를 수행합니다.
    
    ### **Quiz**
    
    1. Python 라이브러리 함수를 사용하여 엑셀 파일을 불러오고, DataFrame을 출력해주세요.
    - **참고**
        - DataFrame을 출력하면 아래와 같이 나와야합니다.
        
        ```python
            관서명   살인 발생   살인 검거   강도 발생   강도 검거   강간 발생   강간 검거   절도 발생   절도 검거   폭력 발생   폭력 검거
        0   서울     10         10        20         19         30         28         40         35         50         48
        1   부산     8          8         15         14         25         23         35         30         45         43
        ...
        
        ```
        
    
    2. 각 경찰서(`관서명`)를 해당 구 이름으로 매핑하여 '구별'이라는 새로운 column을 생성하고, DataFrame을 출력해주세요.
        - 매칭되지 않는 경찰서명에 대해서는 기본값 `'구 없음'`을 할당합니다.
    - **참고**
        - 서울시 경찰청 소속 구
        
        ```
        '서대문서': '서대문구', '수서서': '강남구', '강서서': '강서구', '서초서': '서초구',
        '서부서': '은평구', '중부서': '중구', '종로서': '종로구', '남대문서': '중구',
        '혜화서': '종로구', '용산서': '용산구', '성북서': '성북구', '동대문서': '동대문구',
        '마포서': '마포구', '영등포서': '영등포구', '성동서': '성동구', '동작서': '동작구',
        '광진서': '광진구', '강북서': '강북구', '금천서': '금천구', '중랑서': '중랑구',
        '강남서': '강남구', '관악서': '관악구', '강동서': '강동구', '종암서': '성북구',
        '구로서': '구로구', '양천서': '양천구', '송파서': '송파구', '노원서': '노원구',
        '방배서': '서초구', '은평서': '은평구', '도봉서': '도봉구'
        
        ```
        
        - DataFrame 출력 예시
        
        ```python
        관서명	소계(발생)	소계(검거)	살인(발생)	살인(검거)	강도(발생)	강도(검거)	강간(발생)	강간(검거)	절도(발생)	절도(검거)	폭력(발생)	폭력(검거)	구별
        0	계	126401	82680	163	156	276	257	5449	5069	55307	21842	65206	55356	구 없음
        1	중부서	2860	1716	2	2	3	2	105	65	1395	477	1355	1170	중구
        2	종로서	2472	1589	3	3	6	5	115	98	1070	413	1278	1070	종로구
        ...
        
        ```
        
    
    3. `pivot_table` 을 사용하여 관서별 데이터를 구별 데이터로 변경하고, 같은 구의 경우에는 sum을 적용하여 더해주세요. (index : 관서명 -> 구별)
    - **참고**
        - DataFrame 출력 예시
        
        ```python
        	강간(검거)	강간(발생)	강도(검거)	강도(발생)	살인(검거)	살인(발생)	소계(검거)	소계(발생)	절도(검거)	절도(발생)	폭력(검거)	폭력(발생)
        구별
        강남구	349	449	18	21	10	13	5732	8617	1650	3850	3705	4284
        강동구	123	156	8	6	3	4	3171	5244	789	2366	2248	2712
        강북구	126	153	13	14	8	7	3113	4257	618	1434	2348	2649
        강서구	191	262	13	13	8	7	4190	5585	1260	2096	2718	3207
        관악구	221	320	14	12	8	9	3712	6345	827	2706	2642	3298
        
        ```
        
    
    4. `구 없음` 행은 `drop` 을 활용하여 삭제해주세요.
    - **참고**
        
        ```python
        데이터프레임명.drop([row])
        
        ```
        
    
    5. 각 범죄 별로 검거율을 계산하고, 각 검거율 데이터 column을 DataFrame에 추가해주세요.
    - 추가해야할 column
        
        ```
        강간검거율,
        강도검거율,
        살인검거율,
        절도검거율,
        폭력검거율,
        검거율
        
        ```
        
    - **참고**
        - DataFrame 출력 예시
        
        ```python
        	강간(검거)	강간(발생)	강도(검거)	강도(발생)	살인(검거)	살인(발생)	소계(검거)	소계(발생)	절도(검거)	절도(발생)	폭력(검거)	폭력(발생)	강간검거율	강도검거율	살인검거율	절도검거율	폭력검거율	검거율
        구별
        강남구	349	449	18	21	10	13	5732	8617	1650	3850	3705	4284	77.728285	85.714286	76.923077	42.857143	86.484594	66.519670
        강동구	123	156	8	6	3	4	3171	5244	789	2366	2248	2712	78.846154	133.333333	75.000000	33.347422	82.890855	60.469108
        강북구	126	153	13	14	8	7	3113	4257	618	1434	2348	2649	82.352941	92.857143	114.285714	43.096234	88.637222	73.126615
        
        ```
        
    
    6. 필요없는 column을 `del` 을 사용하여 삭제해주세요.
    - 삭제해야할 column
        
        ```
        강간(검거),
        강도(검거),
        살인(검거),
        절도(검거),
        폭력(검거),
        소계(발생),
        소계(검거)
        
        ```
        
    - **참고**
        
        ```python
        del 데이터프레임명.['column 명']
        
        ```
        
        - DataFrame 출력 예시
            
            ```python
            강간(발생)	강도(발생)	살인(발생)	절도(발생)	폭력(발생)	강간검거율	강도검거율	살인검거율	절도검거율	폭력검거율	검거율
            구별
            강남구	449	21	13	3850	4284	77.728285	85.714286	76.923077	42.857143	86.484594	66.519670
            강동구	156	6	4	2366	2712	78.846154	133.333333	75.000000	33.347422	82.890855	60.469108
            강북구	153	14	7	1434	2649	82.352941	92.857143	114.285714	43.096234	88.637222	73.126615
            
            ```
            
        
    7. DataFrame의 컬럼명을 `rename` 을 사용하여 변경해주세요.
        - 변경해야할 column
        
        ```
        '강간(발생)':'강간',
        '강도(발생)':'강도',
        '살인(발생)':'살인',
        '절도(발생)':'절도',
        '폭력(발생)':'폭력'
        
        ```
        
    - **참고**
        - DataFrame 출력 예시
        
        ```python
        	강간	강도	살인	절도	폭력	강간검거율	강도검거율	살인검거율	절도검거율	폭력검거율	검거율
        구별
        강남구	449	21	13	3850	4284	77.728285	85.714286	76.923077	42.857143	86.484594	66.519670
        강동구	156	6	4	2366	2712	78.846154	100.000000	75.000000	33.347422	82.890855	60.469108
        
        ```
        
    
    ### 추가 도전 과제
    
    1. Python 라이브러리 함수를 사용하여 인구 데이터(pop_kor.csv) 파일을 불러오고, DataFrame을 출력해주세요.
        - Quiz에서 수행한 DataFrame의 구별 index를 기준으로 merge를 할 것이므로, index를 셋팅해서 불러와 주세요.
    - **참고**
        
        ```python
        index_col='구별'
        
        ```
        
    2. `join` 을 사용하여 Quiz에서 수행한 DataFrame과 인구 데이터 DataFrame을 merge하고, DataFrame을 출력해주세요.
    - **참고**
        - `join` : Quiz에서 수행한 DataFrame의 index를 기준으로 인구 데이터 DataFrame index 중 매칭되는 값을 매김.
    3. 새롭게 merge 된 DataFrame에서 `검거율` 기준으로 오름차순 정렬 후, DataFrame을 출력해주세요.
    - **참고**
        
        ```python
         ascending=True # 오름차순
        
        ```