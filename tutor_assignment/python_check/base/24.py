#숙제24 (슬랙에선 22이라고 적힘)
#숙제21과 동일 but 조건 추가
#5개의 숫자를 받은 뒤 그 평균을 구하고, 그에 따른 등급 출력

def sort(*args):
    mean = sum(args)/len(args) 
    for i in args:
        if i>mean:
            print(f'점수:{i} 등급: A ')
        elif i<mean:
            print(f'점수:{i} 등급: C ')
        else:
            print(f'점수:{i} 등급: B ')
    
    
sort(3,2,1)