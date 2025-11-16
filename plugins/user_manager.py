import sqlite3
import csv
import io

class UserManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_all_users(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, email, role, status, created_at 
            FROM users 
            ORDER BY created_at DESC
        ''')
        users = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'role': user[3],
                'status': user[4],
                'created_at': user[5]
            }
            for user in users
        ]

    def bulk_update_users(self, user_ids, action):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            if action == 'activate':
                cursor.execute('UPDATE users SET status = "active" WHERE id IN ({})'.format(
                    ','.join('?' * len(user_ids))
                ), user_ids)
            elif action == 'deactivate':
                cursor.execute('UPDATE users SET status = "inactive" WHERE id IN ({})'.format(
                    ','.join('?' * len(user_ids))
                ), user_ids)
            elif action == 'delete':
                cursor.execute('DELETE FROM users WHERE id IN ({})'.format(
                    ','.join('?' * len(user_ids))
                ), user_ids)
            
            conn.commit()
            return True, f"Successfully {action}d {len(user_ids)} users"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            conn.close()

    def export_users_csv(self):
        users = self.get_all_users()
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(['ID', 'Username', 'Email', 'Role', 'Status', 'Created At'])
        for user in users:
            writer.writerow([
                user['id'],
                user['username'],
                user['email'],
                user['role'],
                user['status'],
                user['created_at']
            ])
        
        return output.getvalue()

    def search_users(self, query):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, email, role, status, created_at 
            FROM users 
            WHERE username LIKE ? OR email LIKE ? OR role LIKE ?
            ORDER BY created_at DESC
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        
        users = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'role': user[3],
                'status': user[4],
                'created_at': user[5]
            }
            for user in users
        ]
