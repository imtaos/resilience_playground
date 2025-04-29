import os

class Config:
    # ProxySQL Configuration
    DB_USER = os.getenv('DB_USER', 'proxyuser')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'proxyuser_password')
    DB_HOST = os.getenv('DB_HOST', 'proxysql')
    DB_PORT = os.getenv('DB_PORT', '6033')
    DB_NAME = os.getenv('DB_NAME', 'blogdb')

    # SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20
    SQLALCHEMY_POOL_TIMEOUT = 30
