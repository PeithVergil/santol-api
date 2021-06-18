import os

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

DEBUG = True

# DATABASE CONFIGURATIONS
# --------------------------------------------------------------
# See: http://docs.sqlalchemy.org/en/latest/core/engines.html#mysql
DATABASE_HOST = os.getenv('SANTOL_DATABASE_HOST', 'dagnet_db')
DATABASE_NAME = os.getenv('SANTOL_DATABASE_NAME', 'santol')
DATABASE_PORT = os.getenv('SANTOL_DATABASE_PORT', '3306')

DATABASE_USERNAME = os.getenv('SANTOL_DATABASE_USERNAME', 'santol')
DATABASE_PASSWORD = os.getenv('SANTOL_DATABASE_PASSWORD', 'abcdef123456')

DATABASES = {
    'default': f'mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}',
    'testing': f'mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}_test',
    
    # 'default': f'sqlite:///{ROOT}/{DATABASE_NAME}.db',
    # 'testing': f'sqlite:///{ROOT}/{DATABASE_NAME}_test.db',
}
DATABASE = DATABASES[os.getenv('SANTOL_DATABASE', 'default')]

HASH_FUNC = 'sha256'
HASH_ITER = 100000
