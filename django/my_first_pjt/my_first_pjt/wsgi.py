# wsgi.py 파일은 Django 프로젝트에서 웹 서버 게이트웨이 인터페이스(WSGI)를 설정하는 파일입니다. 
# WSGI는 Django가 동기 웹 서버 및 애플리케이션과 통신할 수 있도록 하는 표준 인터페이스입니다.

"""
WSGI config for my_first_pjt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_first_pjt.settings")

application = get_wsgi_application()
