"""
Django settings for Orchestrator project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import os,json
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
settings = json.loads(open(BASE_DIR+'/settings.json').read())
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = settings['DEBUG']

ALLOWED_HOSTS = settings['ALLOWED_HOSTS']
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'OrchestratorApp.apps.OrchestratorappConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Orchestrator.urls'

TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates",
                    "DIRS": [],
                    "APP_DIRS": True,
                    "OPTIONS": {"context_processors": ["django.template.context_processors.debug",
                                "django.template.context_processors.request","django.contrib.auth.context_processors.auth",
                                "django.contrib.messages.context_processors.messages"]
            		}
    		}]

WSGI_APPLICATION = 'Orchestrator.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [{"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    				    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        				{"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        				{"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
        				}]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

BROKER_URL = settings['BROKER_URL']
CELERY_BROKER_URL = BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

### EMAIL SETTINGS ###
EMAIL_BACKEND = settings['EMAIL']['BACKEND']
EMAIL_USE_TLS = settings['EMAIL']['USE_TLS']
EMAIL_HOST = settings['EMAIL']['HOST']
EMAIL_HOST_USER = settings['EMAIL']['HOST_USER']
EMAIL_HOST_PASSWORD = settings['EMAIL']['HOST_PASSWORD']
EMAIL_PORT = settings['EMAIL']['PORT']