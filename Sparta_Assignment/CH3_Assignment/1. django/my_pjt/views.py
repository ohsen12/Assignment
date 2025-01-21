from django.shortcuts import render


# 홈페이지
def index(request):
    return render(request, "index.html")


