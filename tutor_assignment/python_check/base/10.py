#숙제10
#1부터 100까지 3과 7의 배수만 출력

for i in range(1,101):
    if i%3==0 and i%7==0:
        print(i, end=' ')
    
    