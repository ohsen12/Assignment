# 요청을 처리하고 처리한 결과를 반환하는 파일

from django.shortcuts import render



# Create your views here.
# 뷰를 작성하는 방법에는 함수형 뷰와 클래스형 뷰가 있다.
# 클래스형 뷰는 상속 받아서 사용할 수 있으니 조금 더 코드를 단축할 수 있다.

# 함수형 뷰: 첫 번째 인자로 요청을 받는다. 이 요청은 장고가 알아서 넘겨준다.
def index(request): 
    '''
    index/라는 패턴으로 요청이 들어오면 이 뷰랑 연결되어 처리된다.
    
    render 함수가 어떤 템플릿으로 요청을 처리해서 반환할 건지.
    '''
    return render(request,'index.html')

