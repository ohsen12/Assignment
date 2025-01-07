# 관리자용 페이지 관련 설정
# 관리자 페이지에서 사용할 '모델'은 직접 등록해주는것이 필요합니다.
# 각 앱의 admin.py에서 설정 가능합니다.

# articles/admin.py
from django.contrib import admin
from .models import Article

# Register your models here. (admin에서 관리할 모델 등록)
@admin.register(Article) # 이 데코레이터는 Article 모델을 관리자 사이트에 등록하는 역할
class ArticleAdmin(admin.ModelAdmin): # admin.ModelAdmin을 상속받아 관리자 인터페이스에서 Article 모델을 어떻게 표시하고 관리할지 정의.
    # ArticleAdmin 클래스 안에 정의된 속성들을 통해 관리자 인터페이스를 커스터마이징
    # 목록 보기에서 표시할 필드를 지정
    list_display = ("title", "created_at")
    # 검색을 수행할 때 사용할 필드를 지정
    search_fields = ("title", "content")
    # 목록 보기에 필터 사이드바를 추가하여 created_at 필드로 필터링할 수 있도록
    list_filter = ("created_at",)
    # 목록 보기에 날짜 계층 링크를 추가하여 created_at 필드를 기준으로 계층적 탐색을 할 수 있도록
    date_hierarchy = "created_at"
    # 목록 보기를 정렬하는 기준을 설정합니다. 여기서는 created_at 필드를 기준으로 내림차순 정렬
    ordering = ("-created_at",)