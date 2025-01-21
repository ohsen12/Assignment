from django.urls import path
from . import views

urlpatterns = [
    # Create
    path("post_create/", views.post_create, name="post_create"),
]
