from django.urls import path
from . import views

app_name = "chatbot"

urlpatterns = [
    # OpednAI의 API를 사용하여 챗 지피티 기능 이용하기
    
    path("chat_view/",views.chat_view, name="chat_view"), # 대화 입력 화면
    path("chat_history/", views.chat_history, name="chat_history"),  # 대화 기록 화면
    path("chat_delete/", views.chat_delete, name="chat_delete"),  # 대화 기록 삭제 로직

]   
