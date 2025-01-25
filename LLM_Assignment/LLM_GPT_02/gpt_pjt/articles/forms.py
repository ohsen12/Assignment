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
        # Comment 모델을 사용해서 form을 만들거임 ❗️코멘트 폼으로 save하면 코멘트 테이블(모델)에 저장된다는 거
        model = Comment
        # 모델에서 보여줄 필드 정의
        fields = "__all__"
        # 댓글 작성할 때 게시글은 사용자가 고르는 게 아니라 그냥 해당 아티클에 다는 거니까 아티클 필드는 보여주지 마. user도 같은 맥락에서 보여주지 마.
        exclude = ("article","user")