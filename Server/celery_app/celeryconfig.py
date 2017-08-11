BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_IMPORTS = ('celery_app.Execution')
