#숙제8
#피보나치 수열에서 14개만 출력
#a, b = 1, 1
#for문
#출력 

# 피보나치 수열은 각 항이 그 앞의 두 항의 합으로 정의된다.

def p_array(p_tuple):
    a,b = p_tuple
    p_list = [a,b]
    while len(p_list) < 14:
        p_list.append(a+b)
        a,b = b,a+b
    return p_list
    
print(p_array((1,1)))
    