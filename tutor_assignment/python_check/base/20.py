#숙제20 (슬랙에선 18이라고 적힘)
#숙제19와 동일 but 조건 추가
#만약에 100초과의 점수를 받을 경우, 바보라고 출력

def grade(n):
    if n>100: print('바보')
    elif n>=90: print('A')
    elif n>=80: print('B')
    elif n>=70: print('C')
    elif n>=60: print('D')
    else: print('F')
    
grade(101)