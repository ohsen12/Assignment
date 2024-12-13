# 숙제 - 77
# 문자열의 첫 문자가 대문자인지 확인하는 함수

def upper(str):
    return str[0].isupper()

print(upper('Apple')) #True
print(upper('apple')) #False