from django.contrib import admin
from .models import CustomUser

# Register your models here.

# admin 사이트에서 CustomUser 테이블을 관리하기 위해 여기에 등록한다. 안하면 사이트에 안보임.
admin.site.register(CustomUser)