from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm


def login(request):
    pass
    

def logout(request):
    pass


def signup(request):
    # 회원가입 폼에 정보 입력하고 submit 버튼 누른 거면
    if request.method == "POST":
        # 사용자가 입력한 정보로 바인딩 폼 만들어주기
        # 업로드된 이미지가 폼에 반영되려면 request.FILES도 함께 전달해야 한다.
        form = CustomUserCreationForm(request.POST,request.FILES)
        # 그리고 그 입력 데이터가 유효하다면
        if form.is_valid():
            # 해당 폼 데이터 DB에 저장해주고 + 얘는 save 하는 순간 자기가 세이브한 인스턴스(객체)를 돌려줌.
            user = form.save()
            # 제대로된 객체가 맞는지 터미널에서 확인
            print(type(user))
            auth_login(request, user) # 회원가입과 동시에 바로 로그인 시켜주기
            return redirect("users:user_profile", username=user.username )   
    # 회원가입하려고 링크(GET방식) 타고 들어왔으면
    else:
        # 커스텀 폼 context에 담아 템플릿으로 보내주기
        form = CustomUserCreationForm()
        context = {"form":form}
        return render(request, "users/signup.html", context)
    

# ❗️ 현재는 username 변수 직접 url에 쳐줘야 들어갈 수 있음
def user_profile(request, username):
    member = get_object_or_404(get_user_model(), username=username)
    context = {"member":member}
    return render(request, "users/user_profile.html", context)
