"""
Django settings for Orchestrator project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from pymongo import MongoClient
from slack import WebClient
from slack.errors import SlackApiError
import redminelib
import requests
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

#Common variables por the security baseline
email_config = settings['EMAIL']
burp_config = settings['BURP']
wordlist = settings['WORDLIST']

# Enviroment variables
os.environ['C_FORCE_ROOT'] = settings['C_FORCE_ROOT']
# Connections
WAPPALIZE_KEY = settings['WAPPALIZE_KEY']

# Mongo connection
try:
    client = MongoClient(settings['MONGO_CLIENT'])
except Exception as e:
    print(str(e))

# Slack connection
try:
    slack_web_client = WebClient(settings['SLACK_KEY'])
    slack_channel_name = settings['SLACK_CHANNEL']
    response = slack_web_client.chat_postMessage(channel=slack_channel_name, text=str('test'))
except SlackApiError as e:
    slack_web_client = None

REDMINE_URL = settings['REDMINE_URL']
REDMINE_USER = settings['REDMINE_USER']
REDMINE_PASSWORD = settings['REDMINE_PASSWORD']

# Redmine connection
try:
    redmine_client = redminelib.Redmine(str(REDMINE_URL), username=str(REDMINE_USER), password=str(REDMINE_PASSWORD),
                  requests={'verify': False,'timeout': None})
    projects = redmine_client.project.all()
except requests.exceptions.MissingSchema:
    redmine_client = None
except redminelib.exceptions.AuthError:
    redmine_client = None
except Exception:
    redmine_client = None

nessus_info = settings['NESSUS']
nessus = False

response = requests.post(nessus_info['URL']+'/session',data={'username':nessus_info['USER'],'password':nessus_info['PASSWORD']},verify=False)
json_resp = json.loads(response.text)
try:
    if json_resp['token']:
        nessus = True
    if not nessus:
        raise Exception('Couldn\'t connect to the nessus server, check the credentials in the settings file')
except KeyError:
    raise Exception('Couldn\'t connect to the nessus server, check the credentials in the settings file')
    pass
except Exception:
    print('Nessus connection failed, check the settings file or the VPN connection')
    pass

acunetix_info = settings['ACUNETIX']
acunetix = False
try:
    login_url = acunetix_info['URL']+'/api/v1/me/login'
    login_json = {
        'email':acunetix_info['USER'],
        'password':acunetix_info['PASSWORD_HASH'],
        'remember_me':acunetix_info['REMEMBER_ME'],
        'logout_previous':acunetix_info['LOGOUT_PREVIOUS']
    }
    response = requests.post(login_url,json=login_json,verify=False)
    if response.status_code == 204:
        acunetix = True
    else:
        raise Exception('Couldn\'t connect to the acunetix server, check the credentials in the settings file')
except Exception:
    print('ACUNETIX connection failed, check the settings file or the VPN connection')
    pass