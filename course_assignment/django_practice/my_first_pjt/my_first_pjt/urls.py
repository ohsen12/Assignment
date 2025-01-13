# urls.py 파일은 Django 프로젝트에서 URL 라우팅을 관리하는 파일입니다. 이 파일을 통해 특정 URL이 요청되었을 때 어떤 뷰(View) 함수가 호출될지를 결정합니다.
# URL 라우팅(URL Routing)은 웹 애플리케이션에서 요청된 URL을 특정한 코드나 함수로 연결하는 과정을 의미해요. 쉽게 말해, 사용자가 웹 브라우저에 특정 URL을 입력했을 때 그 URL에 해당하는 웹 페이지나 기능을 제공할 수 있도록 하는 작업입니다.

"""
URL configuration for my_first_pjt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# 특정 url 패턴으로 들어왔을 때(주소창), 어떠한 뷰로 보낼지를 결정하는 곳
# /의 유무와 상관없이 오늘 날의 웹에서는 이를 같은 것으로 인식하나, 장고에서는 /를 끝에 붙이는 것을 권장한다.
urlpatterns = [
    path("admin/", admin.site.urls), # admin/ 이라는 url 패턴으로 들어오면 articles 앱의 view 모듈 안에 있는 인덱스 함수(뷰)로 요청을 보내라는 뜻
    
    # include 함수를 사용하면 특정 URL 패턴 하위에 다른 URL 패턴을 포함시킬 수 있다.
    
    # articles.urls 파일에서 정의된 URL 패턴은 articles라는 이름 공간을 가지게 된다.
    path("articles/", include("articles.urls")), # 앞이 articles/랑 일치하면 뒤 나머지는 articles.urls 일로 보내서 처리해
    
    path("users/", include("users.urls")), # 앞이 users/랑 일치하면 뒤 나머지는 users.urls 일로 보내서 처리해
    path("accounts/", include("accounts.urls")),

]

# 디버그 모드(개발 모드일 때만) 정적 파일들을 서빙하는 기능을 더해
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)