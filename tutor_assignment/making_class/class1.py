class Student:
    student_total_count = 0
    scholarship_score = 100


    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade
        Student.student_total_count += 1    #클레스 변수. 객체가 하나 생성되어 초기화될 때마다 1이 늘어난다. 즉, 해당 클래스로 만들어진 객체의 수를 보여준다.   
        Student.scholarship_score += 5      #클래스 변수. 객체가 하나 생성되어 초기화될 때마다 기본 100에서 5가 늘어난다.

    def current_situation(self):
        return f'클래스로 만들어진 객체 수: {Student.student_total_count}\n총 장학금: {Student.scholarship_score}만원'
    
    
    def get_info(self):
        return f'name > {self.name}\nage > {self.age}\ngrade > {self.grade}'
    
    

# 객체 생성
s1 = Student('몽룡',19,3)
s2 = Student('춘향',18,2)

print(s1.current_situation())
print()
print(s1.get_info())
print()
print(s2.get_info())