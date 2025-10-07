import os
from datetime import timedelta

class Config:
    # Configuración básica de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
    
    # Configuración de la base de datos
    # Para desarrollo local usar SQLite, para producción PostgreSQL
    if os.environ.get('FLASK_ENV') == 'production':
        DB_USER = os.environ.get('DB_USER', 'admin')
        DB_PASSWORD = os.environ.get('DB_PASSWORD')
        DB_HOST = os.environ.get('DB_HOST', 'localhost')
        DB_PORT = os.environ.get('DB_PORT', '5432')
        DB_NAME = os.environ.get('DB_NAME', 'telegram_app')
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        # SQLite para desarrollo local
        SQLALCHEMY_DATABASE_URI = 'sqlite:///telegram_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # Configuración de correo electrónico (usando SES de AWS)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'email-smtp.eu-north-1.amazonaws.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('AWS_SES_ACCESS_KEY')
    MAIL_PASSWORD = os.environ.get('AWS_SES_SECRET_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Configuración de AWS
    AWS_REGION = os.environ.get('AWS_REGION', 'eu-north-1')
    S3_BUCKET = os.environ.get('S3_BUCKET', 'monitoria-data')
    
    # Credenciales de AWS S3
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    # Configuración de CORS
    CORS_HEADERS = 'Content-Type'
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://app.monitoria.org,http://localhost:3000').split(',') 