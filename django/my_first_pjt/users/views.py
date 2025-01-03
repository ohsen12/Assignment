from django.shortcuts import render

# Create your views here.


def users(request):
    return render(request,'users.html')

def profile(request, username): # users/ 뒤에 들어온 무언가를 username 이라는 변수에 담아서 profile 뷰로 보내버려
    context= {
        "username" : username
    }
    return render(request,'profile.html',context) # context에 담긴 username 을 이제 profile 템플릿에서 사용할 수 있게 된다.