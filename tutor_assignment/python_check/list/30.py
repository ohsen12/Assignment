# 숙제 - 30
# number = [1, 4, 4, 4, 4, 4, 4, 5]에서 요소 4의 위치(인덱스)를 출력하세요

number = [1, 4, 4, 4, 4, 4, 4, 5]

for i,e in enumerate(number):
    if e==4:
        print(i,end=' ')