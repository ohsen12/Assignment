from django.urls import path
from . import views


app_name = "posts"
urlpatterns = [
    # Create
    path("post_create/", views.post_create, name="post_create"),
    # Read
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("post_list/", views.post_list, name="post_list"),
]
