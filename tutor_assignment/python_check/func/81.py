# 숙제 - 81
# 두 개의 문자열을 받아 공통으로 포함된 문자를 반환하는 함수를 만드세요

def common(str1,str2):
    list = (i for i in str1 if i in str2)
    return ','.join(list)

print(common('abc','bcd')) #b,c