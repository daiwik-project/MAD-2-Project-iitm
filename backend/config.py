import os
from dotenv import load_dotenv
from celery.schedules import crontab


load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ['SECRET_KEY']

    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    BCRYPT_LOG_ROUNDS = int(os.environ['BCRYPT_LOG_ROUNDS'])

    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = os.environ['REDIS_CACHE_URL']

    # CELERY_BROKER_URL = os.environ['REDIS_CELERY_URL']
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND_URL')
    IMPORTS = ('controllers.jobs.celery_tasks',)
    BEAT_SCHEDULE = {
        # A name for our scheduled task
        'send-email-of-any-new-quiz': {
            'task': 'controllers.jobs.celery_tasks.check_new_created_quiz_24_hrs_ago',  # The function to run (in app.py)
            'schedule': crontab(hour=18, minute=0),
            # 'schedule': 15.0,       # How often to run it, in seconds (20 hours)
        }, 
        'send-email-monthly-report':{
            "task": 'controllers.jobs.celery_tasks.send_email_report',
            "schedule": crontab(day_of_month=1, hour=1, minute=0),
            # 'schedule': 15.0,  
        }
    }
    # CELERY_RESULT_BACKEND = os.environ['REDIS_CELERY_URL']

    CORS_ENABLED = os.environ['CORS_ENABLED']
    CORS_ORIGINS = os.environ['CORS_ORIGINS'].split(',')

    # mail server INFO
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 465))
    # MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() in ['true', '1', 't']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
