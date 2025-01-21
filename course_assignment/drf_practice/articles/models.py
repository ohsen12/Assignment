from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Comment(models.Model):
    # 하나의 아티클(1)은 여러 개의 댓글을 가짐(N) > 댓글 모델에 외래키 설정
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    # 댓글 모델(테이블) 필드 설정
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)