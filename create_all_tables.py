import sqlite3
from werkzeug.security import generate_password_hash

def create_all_tables():
    conn = sqlite3.connect('transport.db')
    cursor = conn.cursor()
    
    print("Creating ALL database tables...")
    
    # Users table (MISSING!)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password VARCHAR(120) NOT NULL,
            role VARCHAR(20) DEFAULT 'user',
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Other tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            vehicle_type VARCHAR(50),
            vehicle_number VARCHAR(20),
            phone VARCHAR(20),
            status VARCHAR(20) DEFAULT 'available'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            driver_id INTEGER,
            pickup_location TEXT,
            dropoff_location TEXT,
            pickup_time TIME,
            status VARCHAR(20) DEFAULT 'confirmed',
            amount DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER,
            amount DECIMAL(10,2),
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Plugin tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_slot_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enabled BOOLEAN DEFAULT 0,
            start_time TIME DEFAULT '18:00:00',
            end_time TIME DEFAULT '06:00:00'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaign_time_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_name VARCHAR(100),
            start_time TIME,
            end_time TIME,
            days_of_week VARCHAR(50)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            description TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bulk_imports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER,
            filename VARCHAR(255),
            total_users INTEGER,
            successful_imports INTEGER,
            status VARCHAR(50)
        )
    ''')
    
    # Add admin user
    hashed_password = generate_password_hash('admin123')
    cursor.execute(
        'INSERT OR IGNORE INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
        ('admin', 'admin@transport.com', hashed_password, 'admin')
    )
    
    # Add sample data for analytics
    cursor.execute('INSERT OR IGNORE INTO bookings (user_id, driver_id, pickup_location, dropoff_location, status, amount) VALUES (1, 1, "City A", "City B", "completed", 50.00)')
    cursor.execute('INSERT OR IGNORE INTO payments (booking_id, amount, status) VALUES (1, 50.00, "completed")')
    cursor.execute('INSERT OR IGNORE INTO drivers (name, vehicle_type, status) VALUES ("John Driver", "Sedan", "available")')
    
    # Add default time slot settings
    cursor.execute('INSERT OR IGNORE INTO time_slot_settings (enabled) VALUES (0)')
    
    conn.commit()
    conn.close()
    print("✅ ALL TABLES CREATED!")
    print("📊 Created: users, drivers, bookings, payments, time_slot_settings, campaign_time_slots, campaigns, bulk_imports")
    print("👤 Admin user: admin / admin123")

if __name__ == "__main__":
    create_all_tables()
