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
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]