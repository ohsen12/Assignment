# 숙제 - 43
# {'apple': 111, 'banana': 222, 'cherry': 'babo'} 에서 모든 값 출력

dict = {'apple': 111, 'banana': 222, 'cherry': 'babo'} 

print(dict.values())
print(','.join(map(str,dict.values()))) # join 함수는 이터러블의 모든 요소가 문자열일 때만 사용할 수 있음!