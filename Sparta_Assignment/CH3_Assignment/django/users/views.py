from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
# 장고가 알아서 해주는 폼
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


# 로그인
@require_http_methods(["GET","POST"])
def login(request):
    # 로그인 페이지에서 정보입력하고 submit(로그인) 버튼 눌러서 POST 방식으로 데이터 전송했다는 거
    if request.method == "POST":
        # ❗️data=request.POST 라고 명시해줌으로서 request 객체와 관련된 다른 정보는 자동으로 무시하고, 오직 POST 데이터만 사용
        form = AuthenticationForm(data=request.POST) # 사용자가 입력한 로그인 정보 폼으로부터
        if form.is_valid(): # 입력이 유효하다면
            # 로그인 처리해주기 (실제로는 엄청 복잡한 로그인 과정이 auth_login 함수하나로 다 처리됨!)
            auth_login(request, form.get_user()) # 유저 테이블에서 get_user 메서드를 이용하여 로그인한 해당 유저를 가져옴 
            # 💡
            next_path = request.GET.get("next") or "index"
            return redirect("index")
    # 로그인 링크타고 GET요청으로 들어왔다는 거.
    else:    
        form = AuthenticationForm() # 로그인(회원인증)폼 만들어서 context에 담아 템플릿에서 활용 (이거는 커스텀 폼 아님)
    context = {"form":form}
    return render(request, 'users/login.html',context)
    

# 로그아웃
@require_POST
def logout(request):
    # 요청 보낸자가 로그인 되어있는 상황이 맞다면
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect("index")
        

# 회원가입
@require_http_methods(["GET", "POST"])
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


# 회원탈퇴
@require_POST
def delete(request):
    if request.user.is_authenticated:
        # 데이터베이스에서 해당 유저 삭제 (이미 사용자는 로그인 되어있는 유저니까 그냥 delete 했을 때 바로 삭제 되는 건가..?)
        request.user.delete()
        # 삭제하고 바로 로그아웃(해당 유저 세션 지우기. 반드시 탈퇴하고, 세션 지우고 순서여야 함!)
        auth_logout(request) 
    return redirect("index")


# 회원정보수정
@login_required
@require_http_methods(["GET", "POST"])
def update(request):
    # 수정한 정보 입력하고 submit 버튼 눌렀다면
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            print('유효성 검사 성공')
            user = form.save()
            print('폼 저장 성공')
            return redirect("users:user_profile", username=user.username)
    # 수정하러 링크타고 들어왔다면
    else:
        form = CustomUserChangeForm(instance=request.user) # 커스텀 회원정보 수정폼 들고와서 템플릿에 넘겨주기
    context = {"form":form}
    return render(request, 'users/update.html',context)
    

# ❗️ 현재는 username 변수 직접 url에 쳐줘야 들어갈 수 있음
def user_profile(request, username):
    member = get_object_or_404(get_user_model(), username=username)
    context = {"member":member}
    return render(request, "users/user_profile.html", context)
