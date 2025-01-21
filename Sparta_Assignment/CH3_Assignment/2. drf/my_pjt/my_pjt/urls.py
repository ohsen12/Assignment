"""
URL configuration for my_pjt project.

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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # 관리자 페이지
    path('admin/', admin.site.urls),
    
    # 앱
    path("users/", include("users.urls")),
    path("posts/", include("posts.urls")),
]

# 미디어 파일 URL 처리 추가 (개발 환경에서만 사용)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
'''
시리얼라이저는 이미지 URL을 생성하는 역할을 하고,
static() 설정은 해당 URL로 접근할 때 실제 파일을 제공하는 역할을 한다.

원래 장고는 보안상의 이유로 사용자가 업로드한 미디어 파일을 제공하지 않지만(프로덕션 환경일 때는 웹서버가 미디어 파일을 처리한다.), 개발환경일 때는 테스트를 위해 runserver 명령이 임시로 MEDIA_ROOT 경로의 파일을 제공하도록 설정하는 것이다.
시리얼라이저에서 이미지 url 을 포함한 json 응답을 반환하면, 클라이언트가 접근해야 할 url 경로를 생성해주고, 그걸로 클라이언트가 MEDIA_URL(예: /media/)로 요청을 보내면, Django는 요청을 받아 MEDIA_ROOT에 있는 파일을 반환해준다.

따라서 개발 환경에서 미디어 파일을 제공하려면 static() 설정이 꼭 필요하다.
프로덕션 환경에서는 웹 서버 설정으로 대체한다.
'''