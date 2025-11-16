import sqlite3
import csv
import io
from datetime import datetime

class CampaignManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
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
        
        conn.commit()
        conn.close()

    def create_campaign(self, name, description):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO campaigns (name, description)
            VALUES (?, ?)
        ''', (name, description))
        campaign_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return campaign_id

    def get_campaigns(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, COUNT(bi.id) as import_count 
            FROM campaigns c 
            LEFT JOIN bulk_imports bi ON c.id = bi.campaign_id 
            GROUP BY c.id 
            ORDER BY c.created_at DESC
        ''')
        campaigns = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': camp[0],
                'name': camp[1],
                'description': camp[2],
                'created_at': camp[3],
                'import_count': camp[4]
            }
            for camp in campaigns
        ]

    def process_csv_import(self, campaign_id, csv_file):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Read CSV file
            stream = io.StringIO(csv_file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.DictReader(stream)
            
            total_users = 0
            successful_imports = 0
            
            # Record the import
            cursor.execute('''
                INSERT INTO bulk_imports (campaign_id, filename, total_users, status)
                VALUES (?, ?, ?, ?)
            ''', (campaign_id, csv_file.filename, 0, 'processing'))
            import_id = cursor.lastrowid
            
            # Process each row
            for row in csv_reader:
                total_users += 1
                try:
                    username = row.get('username', '').strip()
                    email = row.get('email', '').strip()
                    password = row.get('password', 'default123')  # Default password
                    
                    if username and email:
                        # Check if user already exists
                        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
                        existing_user = cursor.fetchone()
                        
                        if not existing_user:
                            # Insert new user
                            cursor.execute('''
                                INSERT INTO users (username, email, password, role, status)
                                VALUES (?, ?, ?, 'user', 'active')
                            ''', (username, email, password))
                            successful_imports += 1
                        
                except Exception as e:
                    print(f"Error processing user {row}: {e}")
                    continue
            
            # Update import record
            cursor.execute('''
                UPDATE bulk_imports 
                SET total_users = ?, successful_imports = ?, status = 'completed'
                WHERE id = ?
            ''', (total_users, successful_imports, import_id))
            
            conn.commit()
            return True, f"Successfully imported {successful_imports} out of {total_users} users"
            
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            conn.close()

    def get_import_history(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT bi.*, c.name as campaign_name
            FROM bulk_imports bi
            LEFT JOIN campaigns c ON bi.campaign_id = c.id
            ORDER BY bi.created_at DESC
            LIMIT 10
        ''')
        imports = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': imp[0],
                'campaign_id': imp[1],
                'campaign_name': imp[8],
                'filename': imp[2],
                'total_users': imp[3],
                'successful_imports': imp[4],
                'status': imp[5],
                'created_at': imp[6]
            }
            for imp in imports
        ]
