#숙제22 (슬랙에선 20이라고 적힘)
#id = admin
#password = 1234
#로그인 성공 시, 로그인 성공 출력
#로그인 실패 시, 로그인 실패 출력

def login(id:str,password:int):
    if id == 'admin' and password == 1234:
        print('로그인 성공')
    else:
        print('로그인 실패')

login('admin',1234)