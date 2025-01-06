# 반복되는 작업과 코드를 줄일 수 있는 Django Form

from django import forms
from articles.models import Article

# 모델을 보고 
class ArticleForm(forms.ModelForm):
    # ModelForm이 사용할 데이터를 Meta 클래스에 명시
    class Meta:
        # Aricle 모델을 사용해서 form을 만들거임
        model = Article 
        # fields 항목에 내가 form으로 만들고 싶은 항목들을 지정 (__all__은 모델의 모든 필드를 입력하게 하겠다.)
        fields = "__all__"
        # exclude = ["굳이 입력 안 받아도 되는 컬럼"]

    
    