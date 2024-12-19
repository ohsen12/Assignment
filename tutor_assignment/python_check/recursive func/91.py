# 숙제 - 91
# 숫자 리스트를 받아 재귀적으로 최대 값을 찾는 함수

# 파이썬에서 리스트 슬라이싱은 인덱스 범위를 벗어나더라도 오류를 발생시키지 않는다. 대신, 빈 리스트를 반환한다.
# 대신 인덱스에러는 리스트에서 유효하지 않은 인덱스에 접근하려 할 때 발생한다.

def recursive_max(list):
    # 기본 사례 : 리스트가 비어있으면 0을 반환
    if not(list):
        return 0
    # 재귀 사례: 첫 번째 요소와 나머지 요소들 중 최대값을 반환
    else:
        return max(list[0],recursive_max(list[1:]))
    
print(recursive_max([1,2,3]))

'''
1. recursive_max([1,2,3]) : 1, recursive_max([2,3])   1,3 -> 최종 3 반환
2. recursive_max([2,3]) : 2, recursive_max([3])       2,3 -> 3
3. recursive_max([3]) : 3, recursive_max([])          3,0 -> 3
4. recursive_max([]) : 리스트가 비어있으므로 0을 반환. 여기서부터 타고 올라간다.
'''