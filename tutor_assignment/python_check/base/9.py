#숙제9
#numbers = [11, 22, 33, 44, 55]
#target = 44 
#found = False
#44를 찾을 시 찾았다라고 print로 출력

numbers = [11, 22, 33, 44, 55]

def find(n_list):
    for i in n_list:
        if i==44:
            print('찾았다')

find(numbers)