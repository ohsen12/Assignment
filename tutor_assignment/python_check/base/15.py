#숙제15 (슬랙에선 13이라고 적힘)
#회문(palindrome)일 경우 회문입니다 출력, 아닐 경우 아님 출력
#회문 예: 토마토, 구로구, ....등등
#hint: 인덱싱?????

# str[::-1]는 문자열 str을 뒤집는 표현식이다.

def palindrome(str):
    if str == str[::-1]:
        print('회문입니다')
    else:
        print('아님')
        
palindrome('토마토')