import json
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
import os

cwd = Path().cwd()


CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
ORGANIZATION_ID = os.getenv('ORGANIZATION_ID')
PERSONAL_ACCESS_TOKEN = os.getenv('PERSONAL_ACCESS_TOKEN')
LICENSE_ID = int(os.getenv('LICENSE_ID'))

ROUTE_URL = os.getenv('ROUTE_URL')
POLLING = os.getenv('POLLING')
ADMINS_ID = json.loads(os.getenv('ADMINS_ID'))
BOT_TOKEN = os.getenv('BOT_TOKEN')
is_ssl = os.getenv('SSL')

NOTIFY_USERS = json.loads(os.getenv('NOTIFY_USERS'))

WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = f'{cwd.name}'
WEBHOOK_URL = f"{WEBHOOK_HOST}/{WEBHOOK_PATH}/"

BOT_SERVER = {
    'host': os.getenv('BOT_SERVER_HOST'),
    'port': os.getenv('BOT_SERVER_PORT')
}

REDIS = {
    'db': 2,
    'prefix': cwd.name
}
# sad
MYSQL = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'db': os.getenv('MYSQL_DB_NAME'),
    # 'unix_socket': '/var/run/mysqld/mysqld.sock'
}

