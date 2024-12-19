#숙제12 (슬랙에선 10이라고 적힘)
#사용자가 입력한 숫자를 받아, 팩토리얼 계산

# 0의 팩토리얼은 1로 정의된다.

def facto(n):
    result = 1
    if not(n): # n이 0이먄
        return result
    for i in range(1,n+1):
        result *= i
    return result

print(facto(3))