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
            return redirect("posts:post_detail", post.pk)
    # 게시글 작성하려고 링크타고 들어왔으면
    else:    
        form = PostForm()
        context = {"form":form}
        return render(request, "posts/post_create.html", context)


# 게시글 목록
@login_required
@require_http_methods(["GET"])
def post_list(request):
    # 장고 ORM의 매니저 이름은 object's' 이다.
    posts = Post.objects.all()
    context = {"posts":posts}
    return render(request, "posts/post_list.html", context)


# 게시글 상세
@login_required
@require_http_methods(["GET"])
def post_detail(request,pk):
    # 해당 pk값 포스트 객체 담아서 context로 템플릿에 넘겨주기
    post = get_object_or_404(Post, pk=pk)
    context = {"post":post}
    return render(request, "posts/post_detail.html", context)


# ⭐️ 게시글 수정
@login_required
@require_http_methods(["GET","POST"])
def post_update(request,pk):
    # 일단 해당 게시글 객체 조회하고
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # 바인딩 폼 만들어 주고 인스턴스는 원래 객체라고 알려주기
        form = PostForm(request.POST, instance=post)
        post = form.save()
        return redirect("posts:post_detail", pk=post.pk)
    # 글 수정하려고 링크 타고 들어왔으면
    else:
        form = PostForm(instance=post)
        # ⭐️ 글을 수정하고 저장할 때는, 해당 게시글 객체(뭔지 알아야 되니까!)랑 작성 폼 둘 다 필요하다!
        context = {
            "post":post,
            "form":form,
        }
        return render(request,"posts/post_update.html", context)
    

# 게시글 삭제
@login_required
@require_POST
def post_delete(request, pk):
    # 로그인 된 사람이 삭제 버튼을 눌러야 (이미 템플릿에서 본인이 작성한 글인지는 검증했음)
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect("posts:post_list")


