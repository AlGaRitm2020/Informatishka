from os import environ
from dotenv import load_dotenv

# Загрузка значений переменных окружения
load_dotenv()

DEPLOY_TOKEN = environ.get('DEPLOY_TOKEN')
DATABASE_URL = environ.get('DATABASE_URL')

print(DEPLOY_TOKEN, DATABASE_URL)