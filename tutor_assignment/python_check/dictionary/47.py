# 숙제 - 47
# {'a': 1, 'b': 2}와 {'c': 3, 'd': 4}를 합치시오,

# 딕셔너리는 | 연산자로 합칠 수 있다. 여기서 주의할 점은 동일한 키가 있을 경우 두 번째 딕셔너리의 값이 우선한다. 
# value는 중복될 수 있으나 key는 유일해야 하기 때문에 중복되는 앞 딕셔너리의 키의 값은 사라진다는 거.

dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}

print(dict1|dict2)