# 숙제 - 78
# 문자열에서 모음의 개수를 세어 반환하는 함수

def aeiou(str):
    count = 0
    for i in str:
        if i in 'aeiou':
            count+=1
    return count

print(aeiou('aeiok'))