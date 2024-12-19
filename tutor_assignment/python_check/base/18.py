#숙제18 (슬랙에선 16이라고 적힘)
#사용자에게 요일을 받고, 그 요일이 주말이면 주말입니다로 출력

def weekend(str):
    if str in '토일':
        print('주말입니다')
    elif str in '월화수목금':
            print('평일입니다')
        
weekend('토')