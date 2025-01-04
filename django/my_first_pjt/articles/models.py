# DB 관련 데이터 정의 파일(데이터 구조를 적는 곳)

from django.db import models

# Create your models here.

# 모델 정의 기본구조. 모든 모델은 models.Model의 서브 클래스로 표현된다. 
# 이 아티클이 하나의 테이블이 된다. 클래스 밑에 이 테이블 안에 들어갈 데이터들을 정의해줘야 한다.
# ⭐️각각의 필드는 테이블의 각각의 컬럼이다.⭐️
# 행(row)는 데이터베이스에서 한 개의 레코드를 나타낸다. 각 행은 테이블 내의 각 열에 해당하는 데이터를 포함하고 있다. 쉽게 말해, 테이블의 한 행은 데이터를 구체적으로 구성하는 한 단위.
class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add=True : 새로운 행(레코드)가 '생성될 때'의 날짜와 시간을 자동으로 설정한다. 이후에 레코드가 업데이트되더라도 이 필드는 변경되지 않고 레코드가 처음 생성된 시점을 나타낸다.
    updated_at = models.DateTimeField(auto_now=True) # 행(레코드)이 생성되거나 '저장될 때마다' 해당 필드에 현재 날짜와 시간이 자동으로 설정됨. 즉, 레코드가 변경될 때마다 이 필드는 업데이트된다.
    
    def __str__(self): # 클래스를 문자열 취급했을 때 어떻게 보여줄 지 결정하는 매직메서드
        return self.title