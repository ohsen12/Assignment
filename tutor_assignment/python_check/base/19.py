#숙제19 (슬랙에서 17이라고 적힘)
#0부터 100사이의 점수를 받아 학점 출력
#90이상 A
#80이상 B
#70이상 C
#60이상 D
#60미만 F

def grade(n):
    if n>=90: print('A')
    elif n>=80: print('B')
    elif n>=70: print('C')
    elif n>=60: print('D')
    else: print('F')
    
grade(0)