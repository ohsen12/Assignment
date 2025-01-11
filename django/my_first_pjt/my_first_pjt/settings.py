# settings.py 파일은 Django 프로젝트의 설정과 구성을 관리하는 중심 파일입니다. 이 파일을 통해 다양한 프로젝트 설정을 정의할 수 있어요.
# 'django-admin startproject <프로젝트 이름> <생성 디렉토리>' 해서 프로젝트를 생성하고,'python manage.py startapp <앱 이름>'으로 '앱을 설정'하면, 해당 앱을 settings.py의 INSTALLED_APPS에 '앱을 등록'해줘야 합니다. (리스트 끝에 '앱이름' 추가해주고 뒤에 트레일링 콤마 붙이기)

"""
Django settings for my_first_pjt project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-_na@bx&xcu=!-dti-@a9a-9*quosjb5l)q_5)x(g_g+(fwvn+i"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions", # django_extensions 설치하면 앱 등록해줘야 함
    # 사용자 설정 앱 목록(사용자가 직접 앱 생성했으면 여기에 앱 등록해줘야 함)
    "articles",
    "users",
    "accounts",
    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "my_first_pjt.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # 장고가 템플릿을 참조하는 위치는 여기서 결정된다.
        # DIRS에 Django가 추가적으로 템플릿을 참조할 위치를 추가할 수 있음. 
        "DIRS": [BASE_DIR/'templates'], # 최상단인 베이스 디렉토리에 있는 템플릿에서도 찾아봐라.
        "APP_DIRS": True, # 파일을 찾을 때 앱 안쪽 경로까지 찾아보라는 옵션
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "my_first_pjt.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# 커스텀유저모델은 직접 accounts 앱에 등록해 놓은 유저 모델로 사용하겠음.
AUTH_USER_MODEL = 'accounts.User'


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/" # 이거는 실제 디렉토리 경로가 아님 주의!
# 기본적으로 베이스 디렉토리의 static을 뒤져라
STATICFILES_DIRS = [BASE_DIR / "static"]
STAEIC_ROOT = BASE_DIR / "staticfiles"  # 이거는 배포할 때 사용하는 부분

# Media Files 
# 유저가 업로드하면 베이스 디렉토리에 미디어라는 파일이 생기고 이제 그 아래쪽에 다 업로드 될 것임
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
