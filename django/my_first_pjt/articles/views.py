# 요청을 처리하고 처리한 결과를 반환하는 파일

from django.shortcuts import render, redirect
from .models import Article

# Create your views here.
# 뷰를 작성하는 방법에는 함수형 뷰와 클래스형 뷰가 있다.
# 클래스형 뷰는 상속 받아서 사용할 수 있으니 조금 더 코드를 단축할 수 있다.

# 함수형 뷰: 첫 번째 인자로 요청을 받는다. 이 요청은 장고가 알아서 넘겨준다.
def index(request): 
    '''
    index/라는 url 패턴으로 요청이 들어오면 이 함수형 뷰랑 연결되어 처리된다.
    이 뷰에서는 render 함수가 index.html이라는 템플릿(화면 관련)을 가져와 렌더링을 거쳐서 그대로 반환한다.
    '''
    return render(request,'index.html')



# 데이터베이스에서 Article 테이블을 전부 가져와서 화면에 보여주는 로직
def articles(request): 
    articles = Article.objects.all().order_by("-id") # id(pk)을 기준으로 내림차순 정렬
    
    context = {
        "articles" : articles
    }
    return render(request,'articles.html',context)

def article_detail(request, pk): # 뷰 함수의 첫번째 인자는 request, 두번째 인자가 들어올 구멍을 만들어 줘야 함.
    article = Article.objects.get(pk=pk) # id가 넘겨받은 인자랑 같은 레코드 가져오기
    context = {
      "article": article,
    }
    return render(request, "article_detail.html", context)
    

def new(request):
    return render(request,'new.html')

def create(request):
    # POST 방식으로 전달된 데이터 꺼내기
    title = request.POST.get("title")
    content = request.POST.get("content")
    
    # 받은 데이터를 Article 모델을 이용해서 데이터베이스에 저장
    article = Article(title=title, content=content)
    article.save()
    # articles url로 이동해라(입력된 내용 데이터베이스에 저장하고 url 이동했으니까 이제 해당 페이지에선 추가된 아티클까지 보이는 거임.)
    return redirect("article_detail", article.id) # 어떤 pk값으로 갈 지도 변수로 넘겨줘야 한다. 저렇게 써주면 알아서 매핑됨(아, 그렇구나~)


def delete(request, pk):
    article = Article.objects.get(pk=pk)
    # 포스트 방식일 때만 해당 pk 데이터 삭제하고
    if request.method == "POST":
        article.delete()
        # 아티클 목록 페이지로 이동
        return redirect("articles")
    # 포스트 방식으로 들어온 거 아니면 삭제 안하고 그냥 해당 pk값 상세페이지 보여줌
    return redirect("article_detail", article.pk)


def edit(request, pk):
    # pk 값에 해당하는 레코드를 가져옴
    article = Article.objects.get(pk=pk)
    # 해당 레코드를 context에 담아 템플릿에서 활용할 수 있게함
    context = { "article" : article, }
    # context를 활용한 템플릿을 렌더링해서 화면에 보여줌
    return render(request, 'edit.html', context)


def update(request, pk):
    # pk 값에 해당하는 레코드를 가져옴
    article = Article.objects.get(pk=pk)
    
    # POST 방식으로 전달된 데이터를 꺼내서 해당 컬럼에 할당해주기(컬럼 데이터 수정)
    article.title = request.POST.get("title")
    article.content = request.POST.get("content")
    
    # 변경된 데이터를 데이터베이스에 저장(수정 완료)
    article.save()
    
    # 다시 해당 상세페이지로 돌아감(수정된 결과가 나옴)
    return redirect("article_detail", article.pk)



def data_throw(request):
    return render(request,'data_throw.html')


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
    return render(request,'data_catch.html',context)
