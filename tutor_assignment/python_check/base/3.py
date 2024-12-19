#숙제3
#1부터 44까지 짝수는 * 4, 홀수 그냥 출력

for i in range(1,45):
    if i%2: #홀수라면
        print(i,end=' ')
    else:
        print(i*4,end=' ')