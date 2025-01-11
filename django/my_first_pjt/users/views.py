from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

# Create your views here.

# '사용자를 위한 페이지입니다' 라는 문구와 사용자 페이지 목록을 보여주기 위한 뷰
def users(request):  
    users = get_user_model().objects.all() # 모든 유저 데이터 가져오기. 현재 커스텀 유저 모델을 사용하고 있으니, get_user_model()을 사용해준다.
    context = {
        "users" : users
    }
    return render(request,'users/users.html',context)


# 사용자 프로필을 보여주기 위한 뷰
# 일단 얘는 지금 사용자 링크타고 들어가는 GET 방식 밖에 없음.
def profile(request, username): # users/ 뒤에 들어온 무언가를 username() 이라는 변수에 담아서 profile 뷰로 보내졌음
    # 지금, 로그인되어 있는 사람이, 유저네임 타고 누군가의 프로필로 들어온 상황.
    # 지금 맴버 객체는 해당 프로필의 유저를 들고 온 거. 그거 context에 담아서 템플릿으로 보내주기.
    member = get_object_or_404(get_user_model(), username=username)
    context= {
        "member": member,
    }
    return render(request,'users/profile.html',context) # context에 담긴 username을 이제 profile 템플릿에서 사용할 수 있게 된다.


# 팔로우 로직
@require_POST
# 지금 팔로우or언팔로우 버튼 누르고 프로필 유저 pk랑 같이 뷰로 넘어왔음.
def follow(request, user_pk):
    # 현재 사용자가 로그인돼있다면
    if request.user.is_authenticated:
        # 맴버 객체에 프로필 유저 담기
        member = get_object_or_404(get_user_model(), pk=user_pk)
        # 내가 나를 팔로우하게 되는 상황이 아닐 때만
        if request.user != member:
            # 현재 사용자가 프로필 유저의 팔로워 목록에 있다면(이건 언팔 버튼 누른 거니까)
            if request.user in member.followers.all():
                # 프로필 유저의 팔로워 목록에서 현재 사용자 없애주기
                member.followers.remove(request.user)
            # 현재 사용자가 프로필 유저의 팔로워 목록에 없다면(이건 팔로우 버튼 누른 거니까)
            else:
                # 프로필 유저의 팔로워 목록에 현재 사용자 추가해주기
                member.followers.add(request.user)
        # 그리고 다시 프로필 유저의 프로필로 돌아가기
        return redirect("users:profile", member.username)
    # 로그인 안돼있으면 하고 와야 팔로우 기능 사용할 수 있어요~
    return redirect("accounts:login")