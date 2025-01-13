# asgi.py 파일은 Django 프로젝트에서 비동기 서버 게이트웨이 인터페이스(ASGI)를 설정하는 파일입니다. 
# ASGI는 Django가 비동기 웹 서버 및 애플리케이션과 통신할 수 있도록 하는 표준 인터페이스입니다.

"""
ASGI config for my_first_pjt project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_first_pjt.settings")

application = get_asgi_application()
