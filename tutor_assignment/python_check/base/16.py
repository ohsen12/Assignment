#숙제16 (슬랙에선 14이라고 적힘)
#사용자의 입력을 숫자를 입력 받아, 0, 양수, 음수 판별

def n_type(n):
    if n<0:
        print('음수')
    elif n>0:
        print('양수')
    else:
        print('0')
        
n_type(1)