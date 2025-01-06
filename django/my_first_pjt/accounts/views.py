from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login # 사용자정의 함수랑 이름이 같아서 변경해주겠음
from django.contrib.auth import logout as auth_logout # 사용자정의 함수랑 이름이 같아서 변경해주겠음
from django.views.decorators.http import require_POST, require_http_methods

# Create your views here.

# 참고로 세션에 대한 작업은 모두 장고 내부에서 처리하므로 신경쓰지 않아도 됨

@require_http_methods(["GET","POST"]) # 이 두 방식으로 들어왔을 때만 로직 처리
def login(request):
    # 로그인 페이지에서 정보입력하고 submit(로그인) 버튼 눌러서 POST 방식으로 데이터 전송했다는 거
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST) # 사용자가 입력한 로그인 정보 폼으로부터
        if form.is_valid(): # 입력이 유효하다면
            # 로그인 처리해주기
            auth_login(request, form.get_user()) # 유저 테이블에서 get_user 메서드를 이용하여 해당 유저를 가져옴 
            next_path = request.GET.get("next") or "articles:index"
            return redirect("articles:index")
    # 로그인 링크타고 GET요청으로 들어왔다는 거. 로그인 폼 만들어서 context에 담아 템플릿에서 활용
    else:    
        form = AuthenticationForm()
    context = {"form":form}
    return render(request, 'accounts/login.html',context)

# 로그아웃은 서버의 세션 데이터를 지우는 것. 현재 request에서 가져온 세션을 사용하여 DB에서 삭제하고, 클라이언트 쿠키에서도 삭제하는 과정.
# 역시나 장고가 해준다.
@require_POST # POST 요청이 들어왔을 때만 실행하게 해주는 데코레이터
def logout(request):
    if request.user.is_authenticated:
    # 로그아웃 함수는 세션을 종료하고 사용자가 인증된 상태를 해제한다.
        auth_logout(request)
        # 얘가 알아서 요청까서 쿠키에 세션아이디 들어있으면 세션 테이블 열어서 이거 지워주고 쿠키에서 세션아이디 지워주는 것까지 다 해준다.
        return redirect("articles:index")