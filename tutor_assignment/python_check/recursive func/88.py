# 숙제 - 88
# 정수를 받아 그 정수의 팩토리얼을 계산하는 재귀함수

def fact(n):
    # 기본 사례: n이 0이거나 1일 때 1을 반환 (0!은 1임)
    if n == 0 or n == 1:
        return 1
    # 재귀 사례: n이 1보다 클 때 n과 fact(n-1)의 곱을 반환
    else:
        return n * fact(n - 1)
    
print(fact(3))

'''
fact(3) : 3 * fact(2)   # 3*2 -> 최종 6 반환
fact(2) : 2 * fact(1)   # 2*1
fact(1) : 1             # 1
'''