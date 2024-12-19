# 숙제 - 45
# {'apple': 111, 'banana': 222, 'cherry': 'babo'} 에서 apple 삭제 후 출력

dict = {'apple': 111, 'banana': 222, 'cherry': 'babo'}

# 딕셔너리에서 어떤 키 값을 지울 때는 del 딕셔너리[해당 키] 해주면 된다.
# del은 한 번에 하나의 키 밖에 못 지움.

del dict['apple'] 

print(dict)

