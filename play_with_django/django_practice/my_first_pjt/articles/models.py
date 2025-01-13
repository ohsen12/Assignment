# DB 관련 데이터 정의 파일(데이터 구조를 적는 곳)

from django.db import models
from django.conf import settings

# ❗️ 모델 파일에서 변경사항이 있으면 꼭 메이크마이그레이션 해야된다는 것 잊지 말기 ❗️

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
    # 이미지 업로드도 가능 (업로드 안해서 비워둬도 ㄱㅊ)
    image = models.ImageField(upload_to="images/", blank = True) # blank=True면 폼에서 해당 값을 입력하지 않아도 된다. 이 경우 이미지 파일을 업로드하지 않으면 이미지 컬럼이 빈문자열로 처리됨
    
    # 장고 설정에서 유저 모델(테이블)을 참조해라. 게시글이 어떤 유저랑 연결되어 있는지를 나타낸다.
    # 게시글이 어느 사용자가 작성했는지를 나타내는 컬럼.(화면에 표시되는 필드는 아님)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles")
    
    # ❗️다대다(M:N) 관계 설정시 사용하는 모델 필드. 중계 테이블은 내가 커스텀해서 만든 모델로 해줄거임. 이렇게 하면 장고가 만들어주는 그 테이블이 생성되지 않음. (❗️ 이거는 article 테이블에 존재하는 컬럼이 아님! 장고가 자동으로 생성한 중간 테이블에서 관리됨!!)
    # 어 그럼 글을 막써서 게시글에 좋아요가 존재하지 않는 초기상태에 중계 테이블은 어떻게 존재하는 거지?
    # >> 중간 테이블은 연결이 없는 경우 데이터를 저장하지 않으므로, 비어 있는 상태로 유지된다. 연결이 생기면 이제 테이블에 추가되는겨.
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_articles")

    def __str__(self): # 클래스를 문자열 취급했을 때 어떻게 보여줄 지 결정하는 매직메서드
        return self.title
    

# 댓글을 작성하기 위한 모델(comment라는 데이터베이스의 테이블과 연결됨.)
# 각 댓글이 어떤 게시글에 달려있는지 알아야 하기 때문에 외래키를 이용해 Article 모델(테이블)을 참조함. 
class Comment(models.Model):
    # 얘는 화면에 직접 표시되는 필드가 아니라, 데이터베이스에서 댓글(Comment)과 게시글(Article) 간의 관계를 정의하는 컬럼이다.
    # 댓글 모델의 외래키 필드는 댓글이 어떤 게시글에 속해 있는지를 나타내는 컬럼이다.
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments") # related_name은 아티클에서 댓글을 역참조 할 때 사용하는 매니저이다.
    
    # 댓글의 작성자가 누구인지 유저 테이블을 참조
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    
    # 화면에 표시될 필드 정의
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
    

# 좋아요 모델(좋아요를 어떤 글에 누가 눌렀는지 보여주는 테이블) - 중계 테이블
class ArticleLike(models.Model):
    # 어떤 아티클인지 참조하는 외래키 (아티클 모델과의 관계 정의)
    # CASCADE:참조된 게시글이 삭제되면 해당 게시글과 관련된 좋아요도 함꼐 삭제된다.
    # realated_name: Article 모델에서 역참조할 때 사용하는 매니저 이름. 예를 들어, 특정 게시글에 달린 모든 '좋아요'를 가져오려면 article.likes.all()을 사용할 수 있다.
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="likes")
    # 어떤 사용자인지 참조하는 외래키. Django 설정에서 정의된 사용자 모델을 참조한다.
    # 특정 사용자가 눌렀던 모든 '좋아요'를 가져오려면 user.likes.all()을 사용할 수 있다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")