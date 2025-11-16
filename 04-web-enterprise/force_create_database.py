import sqlite3
from werkzeug.security import generate_password_hash

def create_database():
    conn = sqlite3.connect('transport.db')
    cursor = conn.cursor()
    
    print("Creating database tables...")
    
    # Users table
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
    
    # Drivers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            vehicle_type VARCHAR(50) NOT NULL,
            vehicle_number VARCHAR(20) UNIQUE NOT NULL,
            phone VARCHAR(20) NOT NULL,
            status VARCHAR(20) DEFAULT 'available',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            driver_id INTEGER NOT NULL,
            pickup_location TEXT NOT NULL,
            dropoff_location TEXT NOT NULL,
            pickup_time TIME NOT NULL,
            status VARCHAR(20) DEFAULT 'confirmed',
            amount DECIMAL(10,2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (driver_id) REFERENCES drivers (id)
        )
    ''')
    
    # Payments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (booking_id) REFERENCES bookings (id)
        )
    ''')
    
    # Time slot tables (for plugins)
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
    
    # Campaign tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bulk_imports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER,
            filename VARCHAR(255),
            total_users INTEGER,
            successful_imports INTEGER,
            status VARCHAR(50) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
        )
    ''')
    
    # Add default admin user
    print("Creating admin user...")
    hashed_password = generate_password_hash('admin123')
    try:
        cursor.execute(
            'INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
            ('admin', 'admin@transport.com', hashed_password, 'admin')
        )
        print("✅ Admin user created: admin / admin123")
    except sqlite3.IntegrityError:
        print("✅ Admin user already exists")
    
    # Add default time slot settings
    cursor.execute('INSERT INTO time_slot_settings (enabled, start_time, end_time) VALUES (0, "18:00:00", "06:00:00")')
    
    conn.commit()
    conn.close()
    print("🎉 DATABASE CREATED SUCCESSFULLY!")
    print("📊 Tables created: users, drivers, bookings, payments, time_slot_settings, campaign_time_slots, campaigns, bulk_imports")

if __name__ == "__main__":
    create_database()
