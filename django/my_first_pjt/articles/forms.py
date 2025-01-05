# 반복되는 작업과 코드를 줄일 수 있는 Django Form

from django import forms

# 기본 구조 (모델 선언과 비슷!)
class ArticleForm(forms.Form):
    # 내가 이 Form에서 입력받고자 하는 데이터에 대한 명세
    
    # 앞은 데이터베이스에 저장될 값, 뒤는 사용자에게 보여질 값
    GENRE_CHOICES = [
        ("technology", "기술"),
        ("life", "생활"),
        ("hobby", "취미"),
        ("ets", "기타")
    ]
    
    # 제목 입력
    title = forms.CharField(max_length=50) 
    # 내용 입력
    content = forms.CharField(widget=forms.Textarea)
    genre = forms.ChoiceField(choices=GENRE_CHOICES)
    