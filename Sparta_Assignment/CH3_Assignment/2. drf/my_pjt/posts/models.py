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
    
    # ⭐️ 좋아요 필드 (좋아요를 누른 사용자들을 Many-to-Many 관계로 관리)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    
    # 해당 게시글의 좋아요 수를 반환하는 메서드
    def get_likes_count(self):
        '''
        self는 현재 Post 모델의 인스턴스(특정 게시글)를 가리킨다.
        self.likes는 이 Post 인스턴스와 연결된 User 객체들의 QuerySet을 반환한다.
        
        예를 들어, 
        post = Post.objects.get(id=1)
        post.likes.all() 는 해당 게시글에 좋아요를 누른 사용자들의 리스트를 반환한다.
        
        count()는 Django ORM에서 쿼리셋의 행 개수를 반환하는 메서드이다.
        따라서, post.likes.count()는 현재 게시글에 좋아요를 누른 사용자의 수를 반환한다.
        
        get_likes_count는 단순히 likes.count()의 결과를 반환한다.
        '''
        return self.likes.count()
    

class Comment(models.Model):
    # ⭐️ 어떤 게시글에 달린 댓글인지 연결해주기 위해 게시글 모델을 참조하는 외래키 사용
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    # ⭐️ 댓글을 누가 작성한 것인지 연결해주기 위해 유저 모델을 참조하는 외래키 사용
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    
    # 댓글 내용
    content = models.CharField(max_length=255)
    # 생성일
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정일
    updated_at = models.DateTimeField(auto_now=True)