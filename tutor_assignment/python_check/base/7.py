#숙제7
#사용자가 입력한 숫자의 구구단을 출력 (input)
#예시)
#입력값 : 3
#아래는 출력 값
#3 * 1 = 3
#3 * 2 = 6
#3 * 3 = 9
#...

def gugu(n:int):
    for i in range(1,10):
        print(f'{n} * {i} = {n*i}')
        
gugu(3)