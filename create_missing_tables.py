import sqlite3

def create_tables():
    conn = sqlite3.connect('transport.db')
    cursor = conn.cursor()
    
    # Create missing tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            driver_id INTEGER,
            pickup_location TEXT,
            dropoff_location TEXT,
            status TEXT,
            amount DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER,
            amount DECIMAL(10,2),
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            vehicle_type TEXT,
            status TEXT
        )
    ''')
    
    # Add some sample data for analytics
    cursor.execute("INSERT OR IGNORE INTO bookings (user_id, driver_id, pickup_location, dropoff_location, status, amount) VALUES (1, 1, 'City A', 'City B', 'completed', 50.00)")
    cursor.execute("INSERT OR IGNORE INTO payments (booking_id, amount, status) VALUES (1, 50.00, 'completed')")
    
    conn.commit()
    conn.close()
    print("✅ Created missing database tables")

if __name__ == "__main__":
    create_tables()
