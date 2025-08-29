import sqlite3
import json
import time
from pathlib import Path
from contextlib import contextmanager

class Database:
    def __init__(self, db_path="/opt/fermentation-monitor/data/fermentation.db"):
        self.db_path = db_path
        
        # Create data directory if it doesn't exist
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self._init_database()
        
    def _init_database(self):
        """Initialize database tables"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Sensor data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL NOT NULL,
                    temperature REAL,
                    humidity REAL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Image metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS image_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL NOT NULL,
                    volume_change REAL,
                    surface_activity REAL,
                    bubble_count INTEGER,
                    texture_variance REAL,
                    image_path TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Fermentation sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fermentation_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    start_time REAL NOT NULL,
                    end_time REAL,
                    status TEXT DEFAULT 'active',
                    notes TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            
    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        try:
            yield conn
        finally:
            conn.close()
            
    def store_sensor_data(self, data):
        """Store sensor readings"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sensor_data (timestamp, temperature, humidity)
                VALUES (?, ?, ?)
            ''', (data['timestamp'], data['temperature'], data['humidity']))
            conn.commit()
            
    def store_image_metrics(self, metrics):
        """Store image analysis results"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO image_metrics (
                    timestamp, volume_change, surface_activity, 
                    bubble_count, texture_variance
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                metrics['timestamp'],
                metrics['volume_change'],
                metrics['surface_activity'],
                metrics['bubble_count'],
                metrics['texture_variance']
            ))
            conn.commit()
            
    def get_recent_sensor_data(self, hours=24):
        """Get sensor data from the last N hours"""
        cutoff_time = time.time() - (hours * 3600)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM sensor_data 
                WHERE timestamp > ? 
                ORDER BY timestamp DESC
            ''', (cutoff_time,))
            
            return [dict(row) for row in cursor.fetchall()]
            
    def get_recent_image_metrics(self, hours=24):
        """Get image metrics from the last N hours"""
        cutoff_time = time.time() - (hours * 3600)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM image_metrics 
                WHERE timestamp > ? 
                ORDER BY timestamp DESC
            ''', (cutoff_time,))
            
            return [dict(row) for row in cursor.fetchall()]
            
    def create_session(self, name, notes=""):
        """Create a new fermentation session"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO fermentation_sessions (name, start_time, notes)
                VALUES (?, ?, ?)
            ''', (name, time.time(), notes))
            conn.commit()
            return cursor.lastrowid
            
    def get_active_sessions(self):
        """Get all active fermentation sessions"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM fermentation_sessions 
                WHERE status = 'active'
                ORDER BY start_time DESC
            ''')
            
            return [dict(row) for row in cursor.fetchall()]