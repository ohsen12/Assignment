from django import forms
from .models import Message


class ChatForm(forms.ModelForm):
    '''
    이 폼을 context로 사용자 입력 페이지로 넘겨줘서 사용자에게 보여주고, 
    사용자가 거기에 입력해서 submit 버튼 누르고 POST 방식으로 제출하면 뷰에서 모델을 사용하여 처리한 다음에
    응답과 함께 응답 페이지로 redirect.
    
    이 폼은 Message 모델과 연동되어, 사용자가 입력한 user_input 값을 모델에 자동으로 저장할 수 있다.
    사용자는 Message 모델 필드인 user_input, gpt_response, created_at 중에 user_input 만 템플릿의 폼에서 보여주고 입력받도록 한다. (당연. 사용자 입력만 필요함.)
    '''
    class Meta:
        model = Message  # Message 모델과 연동
        fields = ['user_input']  # 사용자의 입력만 폼에 표시
        # 폼의 입력요소를 커스터마이즈 (TextArea를 사용하여 사용자가 입력할 수 있는 영역을 크게 설정)
        widgets = {
            'user_input': forms.Textarea(attrs={'placeholder': '이곳에 대화를 입력하세요. ', 'rows': 2}),
        }