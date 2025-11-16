def add_db_init():
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    # Find the imports section and add init_db function
    for i, line in enumerate(lines):
        if 'from werkzeug.security import generate_password_hash, check_password_hash' in line:
            # Add init_db function after imports
            db_init_code = '''
def init_db():
    conn = sqlite3.connect('transport.db')
    cursor = conn.cursor()
    
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
    
    # Add default admin user if not exists
    cursor.execute('SELECT COUNT(*) FROM users WHERE role = "admin"')
    if cursor.fetchone()[0] == 0:
        hashed_password = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO users (username, email, password, role) 
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin@transport.com', hashed_password, 'admin'))
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()
'''
            lines.insert(i + 1, db_init_code)
            break
    
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    print("✅ Added database initialization!")

if __name__ == "__main__":
    add_db_init()
