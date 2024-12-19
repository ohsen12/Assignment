# 숙제 - 89
# 1부터 n까지의 합을 계산하는 재귀함수

# 재귀 함수를 사용할 때는 꼭 기본 사례(Base Case)가 있어야 한다. 
# 기본 사례는 재귀 호출을 멈추는 조건으로, 무한 루프에 빠지는 것을 방지한다. 
# 기본 사례가 없으면 함수가 끝없이 자기 자신을 호출하게 된다.

def recursive_add(n):
    # 기본 사례: n이 1이 되면 1을 반환. (여기서부터 타고 올라간다.)
    if n==1:
        return 1
    # 재귀 사례: n이 1보다 클 때 n과 add(n-1)의 합을 반환
    else:
        return n + recursive_add(n-1)
    
print(recursive_add(3))

'''
recursive_add(3) = 3 + recursive_add(2)  # 3+3 -> 최종 6을 반환
recursive_add(2) = 2 + recursive_add(1)  # 2+1 -> 3
recursive_add(1) = n이 1이 되어 1을 반환함.  # 1 -> 1
'''