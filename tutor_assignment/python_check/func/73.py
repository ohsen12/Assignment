# 숙제 - 72
# 사용자가 입력한 두 개의 숫자를 받아 더해주는 함수 만드세요

def add_many_num(*args):
    return sum(args)

print(add_many_num(1,2,3)) # 함수 내부에는 args가 (1, 2, 3) 튜플로 묶여서 전달됨