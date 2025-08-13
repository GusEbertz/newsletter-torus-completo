from flask import Blueprint, request, jsonify
from src.models.subscriber import db, Subscriber
from datetime import datetime, timedelta
import sqlite3
from collections import defaultdict
import time

newsletter_bp = Blueprint('newsletter', __name__)

# Rate limiting simples em memória (para produção, usar Redis)
rate_limit_storage = defaultdict(list)
RATE_LIMIT_REQUESTS = 5  # máximo 5 tentativas
RATE_LIMIT_WINDOW = 300  # em 5 minutos (300 segundos)

def is_rate_limited(ip_address):
    """Verificar se IP está sendo rate limited"""
    now = time.time()
    # Limpar registros antigos
    rate_limit_storage[ip_address] = [
        timestamp for timestamp in rate_limit_storage[ip_address]
        if now - timestamp < RATE_LIMIT_WINDOW
    ]
    
    # Verificar se excedeu o limite
    if len(rate_limit_storage[ip_address]) >= RATE_LIMIT_REQUESTS:
        return True
    
    # Adicionar nova tentativa
    rate_limit_storage[ip_address].append(now)
    return False

@newsletter_bp.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        # Obter IP do cliente
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        if client_ip:
            client_ip = client_ip.split(',')[0].strip()
        
        # Verificar rate limiting
        if is_rate_limited(client_ip):
            return jsonify({
                'error': 'Muitas tentativas. Tente novamente em alguns minutos.'
            }), 429
        
        # Validar dados da requisição
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        email = data.get('email')
        if not email:
            return jsonify({'error': 'Email é obrigatório'}), 400
        
        # Sanitizar email
        email = Subscriber.sanitize_email(email)
        if not email:
            return jsonify({'error': 'Email inválido'}), 400
        
        # Validar formato do email
        if not Subscriber.is_valid_email(email):
            return jsonify({'error': 'Formato de email inválido'}), 400
        
        # Verificar se email já existe
        existing_subscriber = Subscriber.query.filter_by(email=email).first()
        if existing_subscriber:
            if existing_subscriber.is_active:
                return jsonify({'error': 'Este email já está inscrito na newsletter'}), 409
            else:
                # Reativar assinatura existente
                existing_subscriber.is_active = True
                existing_subscriber.subscribed_at = datetime.utcnow()
                existing_subscriber.ip_address = client_ip
                db.session.commit()
                return jsonify({
                    'message': 'Inscrição reativada com sucesso!',
                    'subscriber_id': existing_subscriber.id
                }), 200
        
        # Criar novo assinante
        new_subscriber = Subscriber(
            email=email,
            ip_address=client_ip
        )
        
        db.session.add(new_subscriber)
        db.session.commit()
        
        return jsonify({
            'message': 'Inscrição realizada com sucesso!',
            'subscriber_id': new_subscriber.id
        }), 201
        
    except sqlite3.IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email já cadastrado'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@newsletter_bp.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        email = data.get('email')
        if not email:
            return jsonify({'error': 'Email é obrigatório'}), 400
        
        email = Subscriber.sanitize_email(email)
        if not email or not Subscriber.is_valid_email(email):
            return jsonify({'error': 'Email inválido'}), 400
        
        subscriber = Subscriber.query.filter_by(email=email, is_active=True).first()
        if not subscriber:
            return jsonify({'error': 'Email não encontrado na lista de assinantes'}), 404
        
        subscriber.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'Descadastro realizado com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@newsletter_bp.route('/stats', methods=['GET'])
def get_stats():
    """Endpoint simples para estatísticas (opcional)"""
    try:
        total_subscribers = Subscriber.query.filter_by(is_active=True).count()
        total_all_time = Subscriber.query.count()
        
        return jsonify({
            'active_subscribers': total_subscribers,
            'total_all_time': total_all_time
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro ao obter estatísticas'}), 500

