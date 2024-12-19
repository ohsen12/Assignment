# 숙제 - 48
# {'apple': 111, 'banana': 222, 'cherry': 'babo'}에서 모든 키와 모든 값을 순회하여 출력

dict = {'apple': 111, 'banana': 222, 'cherry': 'babo'}

keys = dict.keys()
values = dict.values()

for i in keys:
    print(i,end=' ')
for i in values:
    print(i,end=' ')