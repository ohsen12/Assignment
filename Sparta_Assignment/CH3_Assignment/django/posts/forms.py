from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        # Post 모델과 연결
        model = Post
        # fields 항목에 내가 form으로 만들고 싶은 항목들을 지정 (__all__은 모델의 모든 필드를 입력하게 하겠다.)
        fields = "__all__"
        exclude = ("author")