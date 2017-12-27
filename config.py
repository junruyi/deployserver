import os
import random
import string

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')


class Config:
    SLAT = ''.join(random.sample(string.ascii_letters + string.digits + "-=#_@!$&^*", 50))
    SECRET_KEY = os.environ.get('SECRET_KEY') or SLAT

    DISPLAY_PRE_PAGE = 25
    SITE_URL = 'http://localhost'

    DOMAIN_NAME = 'jumruyi.cc'
    ALLOWED_HOSTS = ['deployserver.junruyi.cc','127.0.0.1','123.207.14.42']

    DEBUG = True

    LOG_LEVEL = 'DEBUG'

    #DATABASE
    DB_ENGINE = 'mysql'
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_USER = 'test'
    DB_PASSWORD = 'test123'
    DB_NAME = 'deployserver'

    HTTP_BIND_HOST = '0.0.0.0'
    HTTP_LISTEN_PORT = 8080

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = ''
    BROKE_URL = 'redis://%(password)s%(host)s:%(port)s/3' %{
        'password':REDIS_PASSWORD,
        'host':REDIS_HOST,
        'port':REDIS_PORT
    }

    TOKEN_EXPIRATION = 3600

    #cookie  setting
    SESSION_COOKIE_DOMAIN = None
    CSRF_COOKIE_DOMAIN = None
    SESSION_COOKIE_AGE = 60 * 30
    SESSION_SAVE_EVERY_REQUEST = True
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_COOKIE_AGE = 60*30

    CAPTCHA_TEST_MODE = False
    # Email SMTP setting, we only support smtp send mail
    EMAIL_HOST = 'smtp.163.com'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = 'matiejun_yy@163.com'
    EMAIL_HOST_PASSWORD = 'mtj@8316107'
    EMAIL_USE_SSL = True  # If port is 465, set True
    EMAIL_USE_TLS = False  # If port is 587, set True
    EMAIL_SUBJECT_PREFIX = '[deployserver] '

    def __init__(self):
        pass

    def __getattr__(self, item):
        return None
