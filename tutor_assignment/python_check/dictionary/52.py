# 숙제 - 52
# {'apple': 111, 'banana': '222', 'cherry': 333} 에 값을 합산하라
# hint 형변환

dict = {'apple': 111, 'banana': '222', 'cherry': 333} 
# 현재 str 이 껴있어서 sum이 안됨
print(sum(map(int,dict.values())))