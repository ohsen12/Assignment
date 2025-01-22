from django.db import models
from django.conf import settings

# 게시글 모델(테이블)
class Post(models.Model):
    # ⭐️ 게시글을 누가 작성한 것인지 연결해주기 위해 외래키 사용
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    
    # 제목
    title = models.CharField(max_length=50)
    # 내용
    content = models.TextField()
    # auto_now_add=True : 새로운 행(레코드)가 '생성될 때'의 날짜와 시간을 자동으로 설정한다.
    created_at = models.DateTimeField(auto_now_add=True) 
    # auto_now=True : 행(레코드)이 생성되거나 '저장될 때마다' 해당 필드에 현재 날짜와 시간이 자동으로 설정됨. 즉, 레코드가 변경될 때마다 이 필드는 업데이트된다.
    updated_at = models.DateTimeField(auto_now=True)
    

class Comment(models.Model):
    # ⭐️ 어떤 게시글에 달린 댓글인지 연결해주기 위해 게시글 모델을 참조하는 외래키 사용
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    # ⭐️ 댓글을 누가 작성한 것인지 연결해주기 위해 유저 모델을 참조하는 외래키 사용
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    
    content = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)