from django.shortcuts import get_object_or_404, redirect, render
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST


# 게시글 작성
@login_required
@require_http_methods(["GET","POST"])
def post_create(request):
    # 게시글 작성하고 submit 눌렀으면
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # 아직 저장하지 말고,
            post = form.save(commit=False)
            # 필수 필드인 author 까지 채워주고 저장
            post.author = request.user
            post.save()
            # ❗️여기 경로변수 때문에 될지 의문
            return redirect("users:user_profile", username=request.user)
    # 게시글 작성하려고 링크타고 들어왔으면
    else:    
        form = PostForm()
        context = {"form":form}
        return render(request, "posts/post_create.html", context)


# 게시글 상세
def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    context = {"post":post}
    return render(request, "posts/post_detail.html", context)


# 게시글 목록
def post_list(request):
    posts = Post.object.all()
    context = {"posts":posts}
    return render(request, "posts/post_list.html", context)