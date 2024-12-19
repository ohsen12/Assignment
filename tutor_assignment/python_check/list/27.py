# 숙제 - 27
# number = [1, 2, 3, 4, 5]에서 3 제거 후 나머지 요소의 평균 값 구해주세요

number = [1, 2, 3, 4, 5]

number.remove(3) # remove 메서드는 원본데이터를 바꿈

print(sum(number)/len(number))
