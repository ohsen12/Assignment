# 숙제 - 92
# 숫자를 입력 받아 재귀적으로 정렬하는 함수

def recursive_sort(list):
    # 기본 사례: 리스트가 비어있거나 요소가 하나만 있을 때
    if len(list) <= 1:
        return list
    
    # 리스트에서 최솟값을 찾기
    min_value = min(list)
    list.remove(min_value) #list에서 해당 최솟값을 제거해줌
    
    # 최솟값을 맨 앞에 붙이고 나머지 리스트를 재귀적으로 정렬 (리스트끼리 + 하면 이어붙여진다.)
    return [min_value] + recursive_sort(list)

# 사용자 입력 받기
numbers = list(map(int,input("숫자를 스페이스로 구분지어 입력하세요 : ").split()))

# 재귀적으로 정렬하고 출력
print(recursive_sort(numbers))

'''
만약 사용자가 입력을 1 2 3 이라고 입력했다면,
1. recursive_sort([1, 2, 3]) : return [1] + recursive_sort([2, 3])   # [1] + [2,3] -> 최종 [1,2,3] 반환
2. recursive_sort([2, 3]) : return [2] + recursive_sort([3])         # [2] + [3] -> [2,3]
3. recursive_sort([3]) : 리스트가 요소 하나만 있으므로 그대로 반환 return [3]  # [3]에서부터 타고 올라간다.
'''