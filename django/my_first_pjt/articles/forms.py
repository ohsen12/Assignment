# 반복되는 작업과 코드를 줄일 수 있는 Django Form
# 보통 forms.py 파일에는 기본 폼 클래스를 상속받아 만든 사용자 정의 폼을 넣어 둔다.
# 이를 통해 Django 기본 폼 기능을 확장하거나 커스터마이징할 수 있다.

from django import forms
from articles.models import Article,Comment

# 게시글(Article) 폼 정의
class ArticleForm(forms.ModelForm):
    # ModelForm이 사용할 데이터를 Meta 클래스에 명시
    class Meta:
        # Aricle 모델을 사용해서 form을 만들거임
        model = Article 
        # fields 항목에 내가 form으로 만들고 싶은 항목들을 지정 (__all__은 모델의 모든 필드를 입력하게 하겠다.)
        fields = "__all__"
        exclude = ("author","like_users",)

# 댓글(Comment) 폼 정의
class CommentForm(forms.ModelForm):
    class Meta:
        # Comment 모델을 사용해서 form을 만들거임
        model = Comment
        # 모델에서 보여줄 필드 정의
        fields = "__all__"
        # 댓글 작성할 때 게시글은 사용자가 고르는 게 아니라 그냥 해당 아티클에 다는 거니까 아티클 필드는 보여주지 마. user도 같은 맥락에서 보여주지 마.
        exclude = ("article","user")

    
    