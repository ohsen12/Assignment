# 숙제 - 90
# 숫자 리스트를 받아 재귀적으로 요소의 합을 계산하는 함수


def recursive_sum(list):
    # 기본 사례: 입력값으로 빈리스트가 오면 0을 반환(여기서부터 타고 올라간다.)
    if not(list):
        return 0
    # 재귀 사례: 첫 번째 요소와 나머지 요소들의 합을 계산
    else:
        return list[0] + recursive_sum(list[1:])
    
print(recursive_sum([1,2,3]))
    
'''
1. recursive_sum([1, 2, 3]) 호출: 1 + recursive_sum([2, 3])  # 1+5 -> 최종 6을 반환
2. recursive_sum([2, 3]) 호출: 2 + recursive_sum([3])        # 2+3
3. recursive_sum([3]) 호출: 3 + recursive_sum([])            # 3+0
4. recursive_sum([]) 호출: 리스트가 비어 있으므로, 0을 반환.        # 0
'''