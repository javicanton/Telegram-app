from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime
from models import db, User
from functools import wraps
import os

auth_bp = Blueprint('auth', __name__)
mail = Mail()
serializer = URLSafeTimedSerializer(os.environ.get('SECRET_KEY', 'your-secret-key'))

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = User.query.get(get_jwt_identity())
        if not current_user or current_user.role != 'admin':
            return jsonify({'error': 'Admin privileges required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['email', 'password', 'name']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        user = User(
            email=data['email'],
            password=data['password'],
            name=data['name']
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Generar token de verificación
        token = serializer.dumps(user.email, salt='email-verification')
        verification_url = f"http://localhost:3000/verify-email/{token}"
        
        # Enviar email de verificación (comentado por ahora)
        # msg = Message(
        #     'Verifica tu email',
        #     recipients=[user.email]
        # )
        # msg.body = f'Por favor, verifica tu email haciendo clic en el siguiente enlace: {verification_url}'
        # mail.send(msg)
        
        return jsonify({'message': 'User registered successfully. Please verify your email.'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

@auth_bp.route('/verify-email/<token>')
def verify_email(token):
    try:
        email = serializer.loads(token, salt='email-verification', max_age=3600)
        user = User.query.filter_by(email=email).first()
        
        if user:
            user.email_verified = True
            user.is_active = True
            db.session.commit()
            return jsonify({'message': 'Email verified successfully'}), 200
    except:
        return jsonify({'error': 'Invalid or expired token'}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['email', 'password']):
            return jsonify({'error': 'Missing email or password'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.email_verified:
            return jsonify({'error': 'Please verify your email first'}), 401
        
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user:
        token = serializer.dumps(user.email, salt='password-reset')
        reset_url = f"http://localhost:3000/reset-password/{token}"
        
        msg = Message(
            'Recuperación de contraseña',
            recipients=[user.email]
        )
        msg.body = f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {reset_url}'
        mail.send(msg)
    
    return jsonify({'message': 'If an account exists with this email, you will receive a password reset link'}), 200

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset', max_age=3600)
        user = User.query.filter_by(email=email).first()
        
        if user:
            data = request.get_json()
            user.password = user.hash_password(data['new_password'])
            db.session.commit()
            return jsonify({'message': 'Password reset successfully'}), 200
    except:
        return jsonify({'error': 'Invalid or expired token'}), 400

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user = User.query.get(get_jwt_identity())
    return jsonify(user.to_dict()), 200 