from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
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


def data_throw(request):
    return render(request,'articles/data_throw.html')


@require_POST
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
    # 포스트 방식으로 넘어온 입력 데이터 꺼내오기
    message = request.POST.get("message") # 서버로 데이터가 message라는 키값으로 전송되니까 딕셔너리의 get 메서드를 사용해서 해당 키의 값을 꺼내오는 것임
    # 아무것도 입력하지 않았는데 제출버튼을 눌렀다면
    if not(message):
        # 오류 메시지 생성. 
        # messages 모듈을 사용하면 장고의 메시지 프레임워크가 자동으로 메시지를 세션에 저장하고, 이를 장고가 자동으로 컨텍스트로 템플릿에 전달한다.
        # 이제 템플릿에서 messages 컨텍스트 변수에 접근하여 저장된 메시지를 화면에 표시할 수 있다.
        messages.error(request, '내용을 입력하세요.')
        return redirect("articles:data-throw")
    else:
        context = {"message": message}
        return render(request,'articles/data_catch.html',context)


# 데이터베이스에서 Article 테이블을 전부 가져와서 화면에 보여주는 로직
def articles(request): 
    # 모든 게시글 들고와
    articles = Article.objects.all().order_by("-id") # id(pk)을 기준으로 내림차순 정렬
    
    # ⭐️ Python에서는 동적으로 객체에 속성을 추가할 수 있다.
    # 비록 Article 모델에 like_count 속성이 기본적으로 정의되어 있지 않지만, 런타임 중에 동적으로 추가할 수 있다.
    # 이렇게 하면 like_count 속성은 데이터베이스에 저장되지 않지만, 뷰에서 템플릿으로 전달되는 객체에서는 사용할 수 있다!!
    for article in articles: 
        article.like_count = article.like_users.count()
    
    context = {
        "articles" : articles,
    }
    return render(request,'articles/articles.html',context)


def article_detail(request, pk): # 뷰 함수의 첫번째 인자는 request, 두번째 인자가 들어올 구멍을 만들어 줘야 함.
    article = get_object_or_404(Article, pk=pk) # id가 넘겨받은 인자랑 같은 레코드 가져오기, 없으면 404에러 내주기
    # 댓글 작성 폼
    comment_form = CommentForm()
    # 해당 아티클에 작성되어있는 댓글을 댓글 매니저 사용해서 댓글 다 들고와서 context에 담아줌 (그럼 얘는 길이가 있는 객체겠지. {{comment|length}} 이런 걸로 댓글 개수 알 수 있겠지 ~)
    comments = article.comments.all()
    context = {
      "article": article,
      "comment_form": comment_form,
      "comments": comments,
    }
    return render(request, "articles/article_detail.html", context)


# 로그인이 되어있지 않은 상태에서 접근하면 settings.py에서 설정된 LOGIN_URL 경로(기본은 로그인 페이지)로 이동시킴
# 기본적으로 LOGIN_URL 설정은 '/accounts/login/'로 되어 있다. 
@login_required
def create(request):
    if request.method == "POST": # 새글 작성하고 저장 누른 거임. 이제 데이터베이스에 전송받은 글 저장해야지.
        form = ArticleForm(request.POST, request.FILES) # form에 request.POST에 있는(전송받은) 데이터 채워
        if form.is_valid(): # form 형식에 맞으면
            article = form.save(commit=False) # 바로 냅다 저장할 수 없어서 commit=False 로 지정. 필요한 속성(컬럼)을 다 채워야 함!
            article.author = request.user # 해당 객체에 author 속성 채워야 되는데, 그거를 지금 요청 보낸 유저로 채워. (현재 로그인한 사람)
            article.save()
            return redirect("articles:article_detail", article.pk) # 저장된 해당 글 상세페이지로 넘어가기
    else: # 새로운 아티클 작성하러 가기 앵커 태그(GET방식) 누르고 새 글 작성하러 온 거임
        form = ArticleForm() # 폼(입력양식) 만들어주고
        context = {"form": form} # 저장 버튼 눌러서 전송받으면 그거 활용해서 creat.html 랜더링 해서 보여줘
    return render(request, "articles/create.html", context) # 이제 해당 페이지에서 submit 버튼 누르면 POST 방식으로 데이터를 담아 다시 이 뷰에 전송함.


@login_required # 로그인이 되어있지 않은 상태에서 접근하면 settings.LOGIN_URL 에 설정된 경로(기본은 로그인 페이지)로 이동시킴
@require_http_methods(["GET", "POST"]) # 요청이 이 방식일 때만 처리
def update(request, pk):
    # 1️⃣ 일단 해당 글 가져와서 객체에 넣어놔
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


# 사용자가 입력한 댓글 폼으로 댓글 테이블에 저장해주는 뷰(해당 게시글에 댓글을 추가하는 역할)
@require_POST
# request 객체와 pk라는 게시글의 기본 키(primary key)를 인자로 받는다.
def comment_create(request, pk):
    # 주어진 기본 키(pk)에 해당하는 Article 객체를 데이터베이스에서 가져온다.
    article = get_object_or_404(Article, pk=pk)
    # 요청으로 전달된 데이터를 이용해 CommentForm 인스턴스를 생성한다. 폼 데이터는 request.POST로 전달된다.
    form = CommentForm(request.POST)
    # 폼 데이터가 유효한지 검증
    if form.is_valid():
        # CommentForm의 데이터를 이용해 Comment 객체를 생성하되, 아직 데이터베이스에 저장하지 않는다. commit=False 옵션을 사용하여 인스턴스만 생성함
        # comment.article과 같이 폼에는 포함되지 않은 데이터를 설정할 필요가 있다. 이렇게 해야 Comment가 특정 Article과 연결된다.
        comment = form.save(commit=False)
        # 새로 생성된 댓글 객체(comment)의 article 속성을 위에서 가져온 Article 객체로 설정한다. 이를 통해 해당 댓글이 어느 게시글에 속하는지를 지정한다!
        comment.article = article
        # 새로 생성된 댓글 객체의 user 속성을 요청을 넘긴(댓글 입력하고 작성버튼을 누른) 유저로 설정한다.
        comment.user = request.user
        # 이제 필요한 모든 컬럼을 채웠으니 댓글 객체를 데이터베이스에 저장한다.
        comment.save()
    return redirect("articles:article_detail", article.pk)


# 댓글 삭제
@require_POST # url에 땅 치고 들어오면 안되니까 submit 버튼 눌렀을 때만 되는 POST 방식 사용해주자
# request 객체와 두 개의 인자 pk (게시글의 기본 키)와 comment_pk (댓글의 기본 키)를 받는다.
def comment_delete(request, pk, comment_pk):
    # 데이터베이스에서 주어진 기본 키(comment_pk)에 해당하는 Comment 객체를 가져온다. (Comment 객체 : 데이터베이스에 저장된 하나의 댓글 데이터를 객체로 표현한 것)
    comment = get_object_or_404(Comment, pk=comment_pk)
    # 가져온 댓글 객체를 데이터베이스에서 삭제
    comment.delete()
    # 해당 게시글로 다시 이동함
    return redirect("articles:article_detail", pk)


@require_POST
# 좋아요(or 좋아요 취소) 버튼 누르고 이 뷰로 넘어왔음
def like(request, pk):
    # 현재 사용자가 로그인되어 있다면
    if request.user.is_authenticated:
        # 해당 게시글 들고오고
        article = get_object_or_404(Article, pk=pk)
        # 해당 게시글에 좋아요 누른 사람 중에 요청 보낸 회원의 pk가 존재한다면 (해당 사용자가 현재 좋아요를 이미 누른 상태라는 거니까. 이 사람은 좋아요 취소 버튼 누르고 온거임)
        if article.like_users.filter(pk=request.user.pk).exists():
            # 해당 게시글 좋아요 누른 사람에서 해당 회원 없애기
            # ❗️ 중계 테이블에서 두 인스턴스 간의 관계가 제거되는 것
            article.like_users.remove(request.user)
        
        # 아직 해당 게시글에 좋아요를 누르지 않은 회원이라면(좋아요 버튼 누르고 온 거니까)
        else:
            # 해당 게시글 좋아요 누른 사람에 해당 회원 추가하기
            # ❗️ 중계 테이블에 두 인스턴스 간의 관계가 추가되는 거임
            article.like_users.add(request.user)
        return redirect("articles:articles")
    # 현재 사용자가 로그인되어 있지 않는데 따봉 버튼을 눌렀다면 로그인 페이지로 보내기 (로그인해야 사용할 수 있는 기능이에요~)
    return redirect("accounts:login")