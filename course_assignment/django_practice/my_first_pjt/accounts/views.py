from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import login as auth_login # 사용자정의 함수랑 이름이 같아서 변경해주겠음
from django.contrib.auth import logout as auth_logout # 사용자정의 함수랑 이름이 같아서 변경해주겠음
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required


# Create your views here.

# 참고로 세션에 대한 작업은 모두 장고 내부에서 처리하므로 신경쓰지 않아도 됨

@require_http_methods(["GET","POST"]) # 이 두 방식으로 들어왔을 때만 로직 처리
def login(request):
    # 로그인 페이지에서 정보입력하고 submit(로그인) 버튼 눌러서 POST 방식으로 데이터 전송했다는 거
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST) # 사용자가 입력한 로그인 정보 폼으로부터
        if form.is_valid(): # 입력이 유효하다면
            # 로그인 처리해주기 (실제로는 엄청 복잡한 로그인 과정이 auth_login 함수하나로 다 처리됨!!)
            auth_login(request, form.get_user()) # 유저 테이블에서 get_user 메서드를 이용하여 해당 유저를 가져옴 
            next_path = request.GET.get("next") or "articles:index"
            return redirect("articles:index")
    
    # 로그인 링크타고 GET요청으로 들어왔다는 거.
    else:    
        form = AuthenticationForm() # 로그인(회원인증)폼 만들어서 context에 담아 템플릿에서 활용 (이거는 커스텀 폼 아님)
    context = {"form":form}
    return render(request, 'accounts/login.html',context)


# 로그아웃은 서버의 세션 데이터를 지우는 것. 현재 request에서 가져온 세션을 사용하여 DB에서 삭제하고, 클라이언트 쿠키에서도 삭제하는 과정.
# 역시나 장고가 해준다.
@require_POST # POST 요청이 들어왔을 때만 실행하게 해주는 데코레이터
def logout(request):
    if request.user.is_authenticated:
        # 로그아웃 함수는 세션을 종료하고 사용자가 인증된 상태를 해제한다. (실제로는 엄청 복잡한 로그아웃 과정이 auth_logout 함수하나로 다 처리됨!!)
        # 얘가 알아서 요청까서 쿠키에 세션아이디 들어있으면 세션 테이블 열어서 이거 지워주고 쿠키에서 세션아이디 지워주는 것까지 다 해준다.
        auth_logout(request)
        return redirect("articles:index")
    

# 회원가입
@require_http_methods(["GET","POST"])
def signup(request):
    if request.method == "POST": # 사용자가 회원가입 정보입력하고 submit 버튼 누른 거면
        form = CustomUserCreationForm(request.POST) # 바인딩 폼 만들어주기
        if form.is_valid(): # 입력 데이터가 유효한 형식이라면
            user = form.save() # 해당 폼 데이터 DB에 저장해주고 + 얘는 save 하는 순간 자기가 세이브한 인스턴스를 돌려줌.
            auth_login(request, user) # 회원가입과 동시에 바로 로그인 시켜주기
            return redirect("articles:index")
    else:  # 그냥 회원가입하겠다고 바로 들어온 거면      
        form = CustomUserCreationForm() # 커스텀 회원가입폼 가져와서 context에 담아 템플릿에 넘겨주기
    context = {"form":form}
    return render(request, "accounts/signup.html",context)


# 회원탈퇴
@require_POST
def delete(request):
    if request.user.is_authenticated:
        # 데이터베이스에서 해당 유저 삭제 (이미 사용자는 로그인 되어있는 유저니까 그냥 delete 했을 때 바로 삭제 되는 건가..?)
        request.user.delete()
        # 삭제하고 바로 로그아웃(해당 유저 세션 지우기. 반드시 탈퇴하고, 세션 지우고 순서여야 함!)
        auth_logout(request) 
    return redirect("articles:index")


# 회원정보 수정
@require_http_methods(["GET","POST"])
def update(request): # 사용자가 수정한 데이터 담아서 다시 온 거
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("articles:index")
    
    else: # 수정하러 링크타고 바로 들어온 거
        form = CustomUserChangeForm(instance=request.user) # 커스텀 회원정보 수정폼 들고와서 템플릿에 넘겨주기
    context = {"form":form}
    return render(request, 'accounts/update.html',context)


# 비밀번호 변경
@login_required
@require_http_methods(["GET","POST"])
def change_password(request):
    # 비밀번호 변경하려고 데이터 입력 해서 제출했으면
    if request.method == "POST":
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save() # 비밀번호 변경완료. 근데 이러면 기존 세션 인증 정보랑 다르기 때문에 로그인이 풀리게 된다.
            # ✅ 비밀번호 변경하고도 로그인 안 풀리게 해주는 거 ( 아,그렇구나 ~)
            update_session_auth_hash(request,form.user) 
            return redirect("articles:index")
    
    # 비밀번호 변경 링크 누르고 들어왔으면
    else:
        form = PasswordChangeForm(request.user) # 이거 커스텀 폼 아님 장고에서 들고 온 거임
    context = {"form":form}
    return render(request, "accounts/change_password.html",context)

    