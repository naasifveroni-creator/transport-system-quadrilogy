import sqlite3
from datetime import datetime, time

class TimeSlotManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_slot_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enabled BOOLEAN DEFAULT 0,
                start_time TIME DEFAULT '18:00:00',
                end_time TIME DEFAULT '06:00:00',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaign_time_slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_name VARCHAR(100) NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                days_of_week VARCHAR(50) DEFAULT '1,2,3,4,5,6,7',
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('SELECT COUNT(*) FROM time_slot_settings')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO time_slot_settings (enabled, start_time, end_time)
                VALUES (0, '18:00:00', '06:00:00')
            ''')
        
        conn.commit()
        conn.close()

    def get_global_settings(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM time_slot_settings ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'enabled': bool(result[1]),
                'start_time': result[2],
                'end_time': result[3]
            }
        return None

    def update_global_settings(self, enabled, start_time, end_time):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO time_slot_settings (enabled, start_time, end_time)
            VALUES (?, ?, ?)
        ''', (enabled, start_time, end_time))
        conn.commit()
        conn.close()
        return True

    def create_campaign_slot(self, campaign_name, start_time, end_time, days_of_week):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO campaign_time_slots (campaign_name, start_time, end_time, days_of_week)
            VALUES (?, ?, ?, ?)
        ''', (campaign_name, start_time, end_time, days_of_week))
        conn.commit()
        conn.close()
        return True

    def get_campaign_slots(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM campaign_time_slots ORDER BY created_at DESC')
        results = cursor.fetchall()
        conn.close()
        
        campaigns = []
        for result in results:
            campaigns.append({
                'id': result[0],
                'campaign_name': result[1],
                'start_time': result[2],
                'end_time': result[3],
                'days_of_week': result[4],
                'active': bool(result[5]),
                'created_at': result[6]
            })
        return campaigns

    def validate_booking_time(self, booking_time_str):
        try:
            booking_time = datetime.strptime(booking_time_str, '%H:%M').time()
            settings = self.get_global_settings()
            
            if settings and settings['enabled']:
                start_time = datetime.strptime(settings['start_time'], '%H:%M:%S').time()
                end_time = datetime.strptime(settings['end_time'], '%H:%M:%S').time()
                
                if start_time > end_time:
                    if not (booking_time >= start_time or booking_time <= end_time):
                        return False, f"Booking outside allowed time slot ({settings['start_time']} - {settings['end_time']})"
                else:
                    if not (start_time <= booking_time <= end_time):
                        return False, f"Booking outside allowed time slot ({settings['start_time']} - {settings['end_time']})"
            
            return True, "Valid booking time"
        except Exception as e:
            return False, f"Time validation error: {str(e)}"
