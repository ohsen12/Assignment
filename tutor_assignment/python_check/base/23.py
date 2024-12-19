#숙제23 (슬랙에선 21이라고 적힘)
#사용자에게 3개의 숫자를 받아, 오름차순 정렬하여 출력

def sort(*args):
    print(''.join(sorted(map(str,args))))
    
sort(5,3,1)
    