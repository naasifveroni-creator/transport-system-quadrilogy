import sqlite3
import json
from datetime import datetime

class RouteOptimizer:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS optimized_routes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                route_name VARCHAR(100) NOT NULL,
                start_location VARCHAR(100) NOT NULL,
                end_location VARCHAR(100) NOT NULL,
                waypoints TEXT,
                total_distance DECIMAL(10,2),
                estimated_time DECIMAL(10,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add sample routes
        cursor.execute('SELECT COUNT(*) FROM optimized_routes')
        if cursor.fetchone()[0] == 0:
            sample_routes = [
                ('Morning City Run', 'Downtown', 'Airport', '["City Center", "Business District"]', 25.5, 45.0),
                ('Coastal Delivery', 'Port Authority', 'Beach Resort', '["Harbor", "Coastal Road"]', 18.2, 35.0),
                ('Industrial Zone', 'Factory A', 'Warehouse B', '["Factory B", "Storage Facility"]', 32.7, 55.0)
            ]
            cursor.executemany(
                'INSERT INTO optimized_routes (route_name, start_location, end_location, waypoints, total_distance, estimated_time) VALUES (?, ?, ?, ?, ?, ?)',
                sample_routes
            )
        
        conn.commit()
        conn.close()

    def get_route_overview(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM optimized_routes')
        total_routes = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(total_distance) FROM optimized_routes')
        total_distance = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT * FROM optimized_routes ORDER BY created_at DESC LIMIT 10')
        recent_routes = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_routes': total_routes,
            'total_distance': float(total_distance),
            'recent_routes': [
                {
                    'id': route[0],
                    'route_name': route[1],
                    'start_location': route[2],
                    'end_location': route[3],
                    'waypoints': json.loads(route[4]) if route[4] else [],
                    'total_distance': float(route[5]),
                    'estimated_time': float(route[6])
                }
                for route in recent_routes
            ]
        }

    def optimize_route(self, route_name, start_location, end_location, waypoints=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        waypoints_json = json.dumps(waypoints) if waypoints else '[]'
        
        # Simple distance calculation (mock)
        total_distance = len(start_location + end_location) * 2.5
        estimated_time = total_distance * 1.8
        
        cursor.execute('''
            INSERT INTO optimized_routes (route_name, start_location, end_location, waypoints, total_distance, estimated_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (route_name, start_location, end_location, waypoints_json, total_distance, estimated_time))
        
        route_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return route_id
