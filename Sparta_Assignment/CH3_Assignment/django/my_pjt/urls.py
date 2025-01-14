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
from my_pjt import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 홈페이지
    path("", views.index),
    # 앱
    path("users/", include("users.urls")),
    path("posts/", include("posts.urls")),
]

# 개발모드일 때만 미디어 파일을 서빙(제공)하게 한다.
# Django에서는 미디어 파일(예: 사용자 업로드 파일)을 MEDIA_URL과 MEDIA_ROOT 설정을 통해 관리한다.
# 이 코드가 하는 일은, 개발 환경에서 미디어 파일을 요청할 때 Django가 이를 직접 제공하도록 하는 것이다.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
