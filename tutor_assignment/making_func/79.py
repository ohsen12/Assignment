# 숙제 - 79
# 숫자 리스트에서 짝수만 합을 계산하는 함수 

def even(num_list):
    return sum(i for i in num_list if i%2 == 0)

print(even([1,2,3,4])) #6