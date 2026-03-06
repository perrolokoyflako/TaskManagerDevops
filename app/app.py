from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    done = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(10), default='medium')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done,
            'priority': self.priority
        }

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    done_filter = request.args.get('done')
    priority_filter = request.args.get('priority')
    query = Task.query
    if done_filter is not None:
        query = query.filter_by(done=done_filter.lower() == 'true')
    if priority_filter:
        query = query.filter_by(priority=priority_filter)
    tasks = query.all()
    return jsonify([t.to_dict() for t in tasks]), 200

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = db.get_or_404(Task, task_id)
    return jsonify(task.to_dict()), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'title is required'}), 400
    priority = data.get('priority', 'medium')
    if priority not in ('low', 'medium', 'high'):
        return jsonify({'error': 'priority must be low, medium or high'}), 400
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        priority=priority
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    task = db.get_or_404(Task, task_id)
    data = request.get_json()
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'done' in data:
        task.done = bool(data['done'])
    if 'priority' in data:
        if data['priority'] not in ('low', 'medium', 'high'):
            return jsonify({'error': 'priority must be low, medium or high'}), 400
        task.priority = data['priority']
    db.session.commit()
    return jsonify(task.to_dict()), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': f'Task {task_id} deleted'}), 200

@app.route('/stats', methods=['GET'])
def stats():
    total = Task.query.count()
    done = Task.query.filter_by(done=True).count()
    pending = total - done
    high = Task.query.filter_by(priority='high', done=False).count()
    return jsonify({
        'total': total,
        'done': done,
        'pending': pending,
        'high_priority_pending': high
    }), 200

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
