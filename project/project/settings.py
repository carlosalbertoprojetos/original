import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
# import pdb

# pdb.set_trace()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-#_m3ld$+yr7kp_&h*idcmhw)*jhtyong1&e#8*apgplpod4)tu"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
ALLOWED_HOSTS = [os.environ.get("ALLOWED_HOSTS")]
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # necessário para o django-allauth:
    "django.contrib.sites",
    # apps terceiros
    "django_select2",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "crispy_forms",
    "widget_tweaks",
    "django.contrib.humanize",
    "import_export",
    "django_cpf_cnpj",
    # apps
    "cliente",
    "compra",
    "despesa",
    "receita",
    "estoque",
    "expedicao",
    "financeiro",
    "fornecedor",
    "funcionario",
    "garantia",
    "materiaprima",
    "notafiscal",
    "producao",
    "produto",
    "venda",
    "transportadora",
    "empresa",
    "mercadolivre",
    "suporte",
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

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
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

# WSGI_APPLICATION = "project.wsgi.application"
WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DJANGO_DB_NAME"),
        "USER": os.environ.get("DJANGO_DB_USERNAME"),
        "PASSWORD": os.environ.get("DJANGO_DB_PASSWORD"),
        "HOST": os.environ.get("DJANGO_DB_HOST"),
        "PORT": "5432",
    }
}

# DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": str(os.path.join(BASE_DIR / "db.sqlite3")),
#    }
# }


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_AUTHENTICATION_METHOD = "username_email"

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

SITE_ID = 1


LOGIN_URL = "/"
LOGIN_REDIRECT_URL = "index"
LOGOUT_URL = "/"
LOGOUT_REDIRECT_URL = "/"


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True

USE_TZ = True

THOUSAND_SEPARATOR = (".",)
DECIMAL_SEPARATOR = ","
USE_THOUSAND_SEPARATOR = True

DATE_FORMAT = ["%d/%m/%Y"]
DATE_INPUT_FORMATS = ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_URL = "static/"

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")

STATICFILES_DIRS = (os.path.join(BASE_DIR, "project/static"),)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# django-crispy-forms.
CRISPY_TEMPLATE_PACK = "bootstrap4"
X_FRAME_OPTIONS = "SAMEORIGIN"


# # configuração para disparo de email address
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# DEFAULT_FROM_EMAIL = 'Nome <email@gmail.com>'
# # EMAIL_HOST = 'smtp.mailtrap.io'
# # EMAIL_HOST_USER = '4cbde76bf57cd9'
# # EMAIL_HOST_PASSWORD = 'f0f092992ce056'
# # EMAIL_PORT = '2525'


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.mailtrap.io"
EMAIL_HOST_USER = "4cbde76bf57cd9"
EMAIL_HOST_PASSWORD = "f0f092992ce056"
EMAIL_PORT = "2525"

EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "seu email do outlook"
SERVER_EMAIL = DEFAULT_FROM_EMAIL
