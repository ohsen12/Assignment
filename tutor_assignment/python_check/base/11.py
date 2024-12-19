#숙제11
#numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#홀수만 새로운 리스트에 추가

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
l = []
for i in numbers:
    if i%2:
        l.append(i)

print(l)