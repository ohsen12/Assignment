# 숙제 - 49
# {'apple': 111, 'banana': 222, 'cherry': 'babo'} 키 'cherry'의 '값'을 출력 하시오
# 없을 경우 None이라고 출력

dict = {'apple': 111, 'banana': 222, 'cherry': 'babo'}

# dict[키이름] 의 방법은 해당 키가 없을 경우 오류가 나지만 dict.get(키이름)의 경우 해당 키가 없으면 none 을 반환한다.

print(dict.get('cherry'))