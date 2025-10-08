import os
from datetime import timedelta

class Config:
    # Configuración básica de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
    
    # Configuración de la base de datos
    # Usar SQLite para desarrollo y AWS (sin PostgreSQL)
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