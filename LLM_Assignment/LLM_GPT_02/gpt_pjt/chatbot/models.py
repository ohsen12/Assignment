from django.db import models
from django.conf import settings


# 사용자의 입력값과 그에 대한 gpt모델의 응답을 저장할 모델(테이블)
class Message(models.Model):
    # 사용자 입력값
    user_input = models.TextField(max_length=200)
    # gpt의 응답
    gpt_response = models.TextField()
    # 대화가 생성된 시간
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 어떤 유저가 나눈 대화인가
    # CASCADE 옵션은 ForeignKey 관계가 설정된 모델에서 참조하는 객체가 삭제되면, 그 객체와 연관된 모든 데이터가 함께 삭제되는 옵션이다.
    # 따라서 CASCADE 옵션이 있기 때문에, 해당 유저가 탈퇴하여 DB에서 제거되면, 그 유저와 연결된 모든 데이터가 함께 삭제된다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat")
    
    def __str__(self):
        return f"User: {self.user_input} | GPT: {self.gpt_response}"