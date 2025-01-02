# 요청을 처리하고 처리한 결과를 반환하는 파일

from django.shortcuts import render



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

def users(request):
    return render(request,'users.html')

def hello(request):
    name = '세은'
    tags = ['python','장고','html']
    books = ['채식주의자','이상한 편의점']
    
    context = {
        'name' : name,
        'tags' : tags,
        'books' : books,
    }   
    return render(request,'hello.html',context)

def data_throw(request):
    return render(request,'data_throw.html')

def data_catch(request):
    return render(request,'data_catch.html')