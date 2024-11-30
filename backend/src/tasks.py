from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import dramatiq_abort
from .models import Task
from .database import db
from .runner import calculate_prime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    if not data or 'n' not in data:
        return jsonify({'error': 'Missing n parameter'}), 400
        
    n = data['n']
    if not isinstance(n, int) or n < 1 or n > 1000000:
        return jsonify({'error': 'N must be an integer between 1 and 1000000'}), 400
    
    task = Task(
        n=n,
        status='waiting',
        user_id=user_id,
        progress=0
    )
    
    db.session.add(task)
    db.session.commit()
    
    # Enqueue the Dramatiq task
    message = calculate_prime.send(task.id)
    task.dramatiq_id = message.message_id
    db.session.commit()
    
    return jsonify({
        'id': task.id,
        'n': task.n,
        'status': task.status,
        'created_at': task.created_at.isoformat(),
    }), 201

@tasks_bp.route('', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
    
    return jsonify([{
        'id': task.id,
        'n': task.n,
        'status': task.status,
        'result': task.result,
        'error': task.error,
        'progress': task.progress,
        'created_at': task.created_at.isoformat(),
        'completed_at': task.completed_at.isoformat() if task.completed_at else None
    } for task in tasks]), 200

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify({
        'id': task.id,
        'n': task.n,
        'status': task.status,
        'result': task.result,
        'error': task.error,
        'progress': task.progress,
        'created_at': task.created_at.isoformat(),
        'completed_at': task.completed_at.isoformat() if task.completed_at else None
    }), 200

@tasks_bp.route('/<int:task_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
        
    if task.status not in ['waiting', 'running']:
        return jsonify({'error': 'Can only cancel waiting or running tasks'}), 400

    if not task.dramatiq_id:
        return jsonify({'error': 'Task has no Dramatiq ID'}), 400
    
    dramatiq_abort.abort(task.dramatiq_id)

    task.status = "cancelled"
    task.completed_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Task cancellation requested'}), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
        
    if task.status in ['waiting', 'running']:
        return jsonify({'error': 'Cannot delete active tasks'}), 400
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Task deleted successfully'}), 200 