from os import getenv
from dotenv import load_dotenv

load_dotenv()

MAIL_SETTINGS = {
    'MAIL_SERVER': getenv('MAIL_SERVER', 'smtp.gmail.com'),
    'MAIL_PORT': int(getenv('MAIL_PORT', 465)),
    'MAIL_USE_SSL': bool(getenv('MAIL_USE_SSL', True)),
    'MAIL_USERNAME': getenv('MAIL_USERNAME', 'testowy2.kmprograms@gmail.com'),
    'MAIL_PASSWORD': getenv('MAIL_PASSWORD', 'jjtdkjurrfqdgqxu'),
}

DB_USERNAME = getenv('DB_USERNAME', 'user')
DB_PASSWORD = getenv('DB_PASSWORD', 'user1234')
DB_PORT = getenv('DB_PORT', 3306)
DB_NAME = getenv('DB_NAME', 'db_1')
DB_HOSTNAME = getenv('DB_HOST', 'mysql')
DB_URL = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}'

ACTIVATION_TOKEN_EXPIRATION_TIME_IN_SECONDS = int(getenv('ACTIVATION_TOKEN_EXPIRATION_TIME_IN_SECONDS', '300'))
ACTIVATION_TOKEN_LENGTH = int(getenv('ACTIVATION_TOKEN_LENGTH', '30'))

JWT_ISSUER = getenv(JWT_ISSUER, 'km-programs.pl')
JWT_AUTHTYPE = getenv(JWT_AUTHTYPE, 'HS512')
JWT_SECRET = getenv(JWT_SECRET, '198272918')
JWT_ACCESS_MAX_AGE = getenv(JWT_ACCESS_MAX_AGE, '5')
JWT_REFRESH_MAX_AGE = getenv(JWT_REFRESH_MAX_AGE, '400')
JWT_PREFIX = getenv(JWT_PREFIX, 'Bearer ')