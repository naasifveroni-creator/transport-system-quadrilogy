import sqlite3
from datetime import datetime, timedelta

class Billing:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number VARCHAR(50) UNIQUE NOT NULL,
                customer_name VARCHAR(100) NOT NULL,
                customer_email VARCHAR(120),
                amount DECIMAL(10,2) NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                due_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments_received (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER,
                amount DECIMAL(10,2) NOT NULL,
                payment_method VARCHAR(50),
                transaction_id VARCHAR(100),
                paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (invoice_id) REFERENCES invoices (id)
            )
        ''')
        
        # Add sample data
        cursor.execute('SELECT COUNT(*) FROM invoices')
        if cursor.fetchone()[0] == 0:
            sample_invoices = [
                ('INV-2024-001', 'ABC Transport Co.', 'abc@transport.com', 1250.00, 'paid', '2024-12-01'),
                ('INV-2024-002', 'XYZ Logistics', 'billing@xyz.com', 890.50, 'pending', '2024-12-15'),
                ('INV-2024-003', 'Global Shipping Ltd', 'accounts@global.com', 2100.75, 'paid', '2024-11-28')
            ]
            cursor.executemany(
                'INSERT INTO invoices (invoice_number, customer_name, customer_email, amount, status, due_date) VALUES (?, ?, ?, ?, ?, ?)',
                sample_invoices
            )
        
        conn.commit()
        conn.close()

    def get_billing_overview(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT SUM(amount) FROM invoices WHERE status = "paid"')
        total_revenue = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT SUM(amount) FROM invoices WHERE status = "pending"')
        pending_amount = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT * FROM invoices ORDER BY created_at DESC LIMIT 10')
        recent_invoices = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_revenue': float(total_revenue),
            'pending_amount': float(pending_amount),
            'recent_invoices': [
                {
                    'id': inv[0],
                    'invoice_number': inv[1],
                    'customer_name': inv[2],
                    'amount': float(inv[4]),
                    'status': inv[5],
                    'due_date': inv[6]
                }
                for inv in recent_invoices
            ]
        }

    def create_invoice(self, invoice_number, customer_name, customer_email, amount, due_date):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO invoices (invoice_number, customer_name, customer_email, amount, due_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (invoice_number, customer_name, customer_email, amount, due_date))
        
        invoice_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return invoice_id
