# 숙제 - 84
# 리스트를 받아 중복된 요소가 있는지 확인하는 함수

def duplicate(list):
    return len(list) != len(set(list))

print(duplicate([1,1,2,3])) #중복요소 있으므로 True
print(duplicate([1,2,3])) #중복요소 없으므로 False