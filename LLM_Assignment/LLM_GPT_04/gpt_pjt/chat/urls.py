from django.urls import path
from . import views

app_name="chat"

urlpatterns = [
    path("chat_start/", views.Chat_With_GPTAPIView.as_view(), name="chat_start"),
    path("chat_delete/", views.Chat_DeleteAPIView.as_view(), name="chat_delete"),
]
