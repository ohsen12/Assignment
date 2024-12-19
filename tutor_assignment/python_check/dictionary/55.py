# 숙제 - 55
# {'apple': 111, 'banana': 222, 'cherry': 'babo'} 에서 값 babo에 해당하는 키를 출력

dict = {'apple': 111, 'banana': 222, 'cherry': 'babo'}

for key, value in dict.items():
    if value == 'babo':
        print(key)