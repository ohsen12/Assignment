# 요청을 처리하고 처리한 결과를 반환하는 파일

from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST


# Create your views here.
# 뷰를 작성하는 방법에는 함수형 뷰와 클래스형 뷰가 있다.
# 클래스형 뷰는 상속 받아서 사용할 수 있으니 조금 더 코드를 단축할 수 있다.

# 함수형 뷰: 첫 번째 인자로 요청을 받는다. 이 요청은 장고가 알아서 넘겨준다.
def index(request): 
    '''
    index/라는 url 패턴으로 요청이 들어오면 이 함수형 뷰랑 연결되어 처리된다.
    이 뷰에서는 render 함수가 index.html이라는 템플릿(화면 관련)을 가져와 렌더링을 거쳐서 그대로 반환한다.
    '''
    return render(request,'articles/index.html')


# 데이터베이스에서 Article 테이블을 전부 가져와서 화면에 보여주는 로직
def articles(request): 
    articles = Article.objects.all().order_by("-id") # id(pk)을 기준으로 내림차순 정렬
    
    context = {
        "articles" : articles
    }
    return render(request,'articles/articles.html',context)


def article_detail(request, pk): # 뷰 함수의 첫번째 인자는 request, 두번째 인자가 들어올 구멍을 만들어 줘야 함.
    article = get_object_or_404(Article, pk=pk) # id가 넘겨받은 인자랑 같은 레코드 가져오기, 없으면 404에러 내주기
    context = {
      "article": article,
    }
    return render(request, "articles/article_detail.html", context)
    
    
# ⭐️ 이 부분만 제대로 이해하면 돼🥹

# 로그인이 되어있지 않은 상태에서 접근하면 settings.py에서 설정된 LOGIN_URL 경로(기본은 로그인 페이지)로 이동시킴
# 기본적으로 LOGIN_URL 설정은 '/accounts/login/'로 되어 있다. 
@login_required
def create(request):
    if request.method == "POST": # 새글 작성하고 저장 누른 거임. 이제 데이터베이스에 전송받은 글 저장해야지.
        form = ArticleForm(request.POST) # form에 request.POST에 있는(전송받은) 데이터 채워
        if form.is_valid(): # form 형식에 맞으면
            article = form.save() # DB에 저장하고
            return redirect("articles:article_detail", article.id) # 저장된 해당 글 상세페이지로 넘어가기
    else: # 새로운 아티클 작성하러 가기 앵커 태그(GET방식) 누르고 새 글 작성하러 온 거임
        form = ArticleForm() # 폼(입력양식) 만들어주고
        context = {"form": form} # 저장 버튼 눌러서 전송받으면 그거 활용해서 creat.html 랜더링 해서 보여줘
    return render(request, "articles/create.html", context) # 이제 해당 페이지에서 submit 버튼 누르면 POST 방식으로 데이터를 담아 다시 이 뷰에 전송함.


@login_required # # 로그인이 되어있지 않은 상태에서 접근하면 settings.LOGIN_URL 에 설정된 경로(기본은 로그인 페이지)로 이동시킴
@require_http_methods(["GET", "POST"]) # 요청이 이 방식일 때만 처리
def update(request, pk):
    # 일단 해당 글 가져와서 객체에 넣어놔
    article = get_object_or_404(Article, pk=pk)
    
    if request.method == "POST": # 글 수정하고 저장 누른 거임.
        form = ArticleForm(request.POST, instance=article) # 양식이 유효하면 데이터베이스에 다시 저장하고
        if form.is_valid():
            article = form.save()
            return redirect("articles:article_detail", article.pk) # 해당 아티클 상세페이지로 돌아가.

    else: # 글 수정 앵커 태그(GET 방식) 누르고 글 수정하러 온 거임
        # instance : ArticleForm을 생성할 때 article 객체를 기반으로 폼을 생성하도록 하는 매개변수
        form = ArticleForm(instance=article)  # 입력폼에 기존 글 채워서 보여주고
    context = {
        "form": form,
        "article": article,
    }
    # 생성한 입력 폼이랑 해당 객체 context에 담아서 update.html 에서 활용하고 랜더링해서 보여줌
    return render(request, "articles/update.html", context) # 이제 update.html에서 submit 버튼 누르면 POST 방식으로 데이터를 담아 다시 이 뷰에 전송함.


@require_POST # POST 요청일 떄만 처리
def delete(request, pk):
    # 로그인 된 상태에서 삭제 버튼 눌러야만 삭제해줌
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        # 삭제하고 아티클 목록 페이지로 이동
    # 로그인 안된 상태에서 눌렀으면 바로 아티클 목록 페이지로 이동
    return redirect("articles:articles")


def data_throw(request):
    return render(request,'articles/data_throw.html')


def data_catch(request):
    '''
    data-throw 에서 입력한 데이터를 message라는 name(key)으로 값을 전달해줬기 때문에
    뷰에서 message라는 key에 있는 값을 꺼내라는 것이다.
    그럼 그 값을 context에 담아 render 함수의 세 번째 인자로 넘겨준다.
    
    ⭐️ render 함수에서 context는 '템플릿에 전달할 데이터를 포함'하는 역할을 한다. 
    context는 딕셔너리 형태로 작성되며, 템플릿에서 사용될 변수를 키-값 쌍으로 정의한다. 
    이를 통해 템플릿은 동적 데이터를 포함하여 HTML 페이지를 생성할 수 있다.
    
    템플릿에서 contex 딕셔너리에 정의된 변수들을 사용하여 HTML 페이지를 만들 수 있다는 것이다. 
    근데 이때 context를 세 번째 인자로 전달하지 않으면 템플릿에서 변수를 사용할 수 없어서, HTML 출력에 동적 데이터가 포함되지 않게 되니 주의해야 한다!  
    '''
    message = request.GET.get("message") # 서버로 데이터가 message라는 키값으로 전송되니까 딕셔너리의 get 메서드를 사용해서 해당 키의 값을 꺼내오는 것임
    context = {"message": message}
    return render(request,'articles/data_catch.html',context)
