from django.db import models

# Create your models here.


class product(models.Model):
    # ⭐️ 카테고리 필드의 선택지
    # 앞이 DB에 저장되는 거, 뒤가 유저에게 보여지는 거
    CATEGORY_CHOICES = (
        ("F", "Fruit"),
        ("V", "Vegetable"),
        ("M", "Meat"),
        ("O", "Other"),
    )
    name = models.CharField(max_length=30)
    # 그냥 인티저 필드 하면 음수도 들어갈 수 있으니 양수 필드로 만들어줌
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    
    # admin 사이트에서 보여질 이름
    def __str__(self):
        return self.name
    
    