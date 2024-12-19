# 숙제 - 86
# 문자열에서 숫자만 추출하는 함수

# 문자열의 isdigit() 메서드는 문자열의 모든 요소가 숫자형으로 구성되어 있다면 True를 반환한다.

def ru_num(str):
    return ''.join(i for i in str if i.isdigit())

print(ru_num('123일이삼'))