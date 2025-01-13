# manage.py는 Django 프로젝트에서 다양한 명령어를 실행하는 역할을 합니다. 이 명령어들을 통해 서버를 실행하거나, 데이터베이스를 관리하거나, 새로운 앱을 생성하는 등의 작업을 할 수 있어요.

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_first_pjt.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
