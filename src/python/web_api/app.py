from flask import Flask, render_template, jsonify, request
import json
import time
from pathlib import Path

def create_app(database):
    app = Flask(__name__, 
                template_folder='../../web/templates',
                static_folder='../../web/static')
    
    app.config['SECRET_KEY'] = 'fermentation-monitor-secret-key'
    
    @app.route('/')
    def index():
        return render_template('index.html')
        
    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')
        
    @app.route('/api/sensor-data')
    def get_sensor_data():
        hours = request.args.get('hours', 24, type=int)
        data = database.get_recent_sensor_data(hours)
        return jsonify(data)
        
    @app.route('/api/image-metrics')
    def get_image_metrics():
        hours = request.args.get('hours', 24, type=int)
        data = database.get_recent_image_metrics(hours)
        return jsonify(data)
        
    @app.route('/api/sessions')
    def get_sessions():
        sessions = database.get_active_sessions()
        return jsonify(sessions)
        
    @app.route('/api/sessions', methods=['POST'])
    def create_session():
        data = request.get_json()
        session_id = database.create_session(
            data.get('name', 'New Session'),
            data.get('notes', '')
        )
        return jsonify({'id': session_id, 'status': 'created'})
        
    @app.route('/api/current-status')
    def current_status():
        # Get latest readings
        sensor_data = database.get_recent_sensor_data(1)  # Last hour
        image_data = database.get_recent_image_metrics(1)  # Last hour
        
        latest_sensor = sensor_data[0] if sensor_data else None
        latest_image = image_data[0] if image_data else None
        
        return jsonify({
            'temperature': latest_sensor['temperature'] if latest_sensor else None,
            'humidity': latest_sensor['humidity'] if latest_sensor else None,
            'fermentation_activity': latest_image['surface_activity'] if latest_image else 0,
            'bubble_count': latest_image['bubble_count'] if latest_image else 0,
            'last_update': latest_sensor['timestamp'] if latest_sensor else time.time()
        })
        
    return app