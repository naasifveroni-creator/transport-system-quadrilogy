import sqlite3
from datetime import datetime

class LiveTracking:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicle_locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id VARCHAR(50) NOT NULL,
                driver_name VARCHAR(100) NOT NULL,
                latitude DECIMAL(10,6),
                longitude DECIMAL(10,6),
                speed DECIMAL(5,2),
                status VARCHAR(20) DEFAULT 'active',
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add sample vehicles
        cursor.execute('SELECT COUNT(*) FROM vehicle_locations')
        if cursor.fetchone()[0] == 0:
            sample_vehicles = [
                ('VH001', 'John Driver', 40.7128, -74.0060, 45.5, 'active'),
                ('VH002', 'Sarah Wilson', 34.0522, -118.2437, 38.2, 'active'),
                ('VH003', 'Mike Johnson', 41.8781, -87.6298, 0, 'idle')
            ]
            cursor.executemany(
                'INSERT INTO vehicle_locations (vehicle_id, driver_name, latitude, longitude, speed, status) VALUES (?, ?, ?, ?, ?, ?)',
                sample_vehicles
            )
        
        conn.commit()
        conn.close()

    def get_live_overview(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM vehicle_locations')
        total_vehicles = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM vehicle_locations WHERE status = "active"')
        active_vehicles = cursor.fetchone()[0]
        
        cursor.execute('SELECT * FROM vehicle_locations ORDER BY last_updated DESC LIMIT 10')
        vehicle_locations = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_vehicles': total_vehicles,
            'active_vehicles': active_vehicles,
            'vehicle_locations': [
                {
                    'id': vehicle[0],
                    'vehicle_id': vehicle[1],
                    'driver_name': vehicle[2],
                    'latitude': float(vehicle[3]),
                    'longitude': float(vehicle[4]),
                    'speed': float(vehicle[5]),
                    'status': vehicle[6],
                    'last_updated': vehicle[7]
                }
                for vehicle in vehicle_locations
            ]
        }

    def update_vehicle_location(self, vehicle_id, latitude, longitude, speed, status='active'):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO vehicle_locations 
            (vehicle_id, driver_name, latitude, longitude, speed, status, last_updated)
            VALUES (?, (SELECT driver_name FROM vehicle_locations WHERE vehicle_id = ?), ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (vehicle_id, vehicle_id, latitude, longitude, speed, status))
        
        conn.commit()
        conn.close()
        return True
