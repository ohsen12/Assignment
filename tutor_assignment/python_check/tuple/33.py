# 숙제 - 33
# a = 11
# b = 22
# 위의 변수를 선언 후 a의 값을 22, b의 값을 11로 교환

a = 11
b = 22

a,b = b,a #오른쪽의 b,a는 (b,a)라는 튜플로 평가된다. 왼쪽의 a,b에 튜플의 각각의 값이 할당된다.

print(a,b)
