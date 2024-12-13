# 숙제 - 85
# 두개의 리스트를 받아 공통 요소만 반환하는 함수

#join은 모든 요소값이 문자열인 이터러블에 사용가능

def duplicate_list(list1,list2):
    return ','.join(str(i) for i in list1 if i in list2) 

print(duplicate_list([1,2,3],[2,3,4]))
print(duplicate_list(['일','이','삼'],['이','삼','사']))