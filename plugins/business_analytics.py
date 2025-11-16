import sqlite3
from datetime import datetime, timedelta

class BusinessAnalytics:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_dashboard_metrics(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total Bookings
        cursor.execute('SELECT COUNT(*) FROM bookings')
        total_bookings = cursor.fetchone()[0] or 0
        
        # Total Revenue
        cursor.execute('SELECT SUM(amount) FROM payments WHERE status = "completed"')
        total_revenue = cursor.fetchone()[0] or 0
        
        # Active Users
        cursor.execute('SELECT COUNT(*) FROM users WHERE status = "active"')
        active_users = cursor.fetchone()[0] or 0
        
        # Popular Routes
        cursor.execute('''
            SELECT pickup_location, dropoff_location, COUNT(*) as booking_count 
            FROM bookings 
            GROUP BY pickup_location, dropoff_location 
            ORDER BY booking_count DESC 
            LIMIT 5
        ''')
        popular_routes = cursor.fetchall()
        
        # Revenue by Month (last 6 months)
        six_months_ago = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT strftime('%Y-%m', created_at) as month, SUM(amount) as revenue
            FROM payments 
            WHERE status = "completed" AND created_at >= ?
            GROUP BY month 
            ORDER BY month DESC
            LIMIT 6
        ''', (six_months_ago,))
        revenue_trends = cursor.fetchall()
        
        # Daily Bookings (last 7 days)
        seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT DATE(created_at) as date, COUNT(*) as bookings
            FROM bookings 
            WHERE created_at >= ?
            GROUP BY date 
            ORDER BY date DESC
            LIMIT 7
        ''', (seven_days_ago,))
        daily_bookings = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_bookings': total_bookings,
            'total_revenue': float(total_revenue),
            'active_users': active_users,
            'popular_routes': [
                {'route': f"{route[0]} to {route[1]}", 'bookings': route[2]}
                for route in popular_routes
            ],
            'revenue_trends': [
                {'month': trend[0], 'revenue': float(trend[1] or 0)}
                for trend in revenue_trends
            ],
            'daily_bookings': [
                {'date': booking[0], 'bookings': booking[1]}
                for booking in daily_bookings
            ]
        }
