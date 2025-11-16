from datetime import datetime, timedelta

class BillingMIS:
    def __init__(self):
        self.base_fare = 50.00
        self.distance_rate = 15.00
        self.transaction_log = []
    
    def calculate_trip_cost(self, from_location, to_location, distance_km=None):
        cost = self.base_fare
        if distance_km:
            cost += distance_km * self.distance_rate
        
        premium_locations = ['Airport', 'Train Station']
        if from_location in premium_locations or to_location in premium_locations:
            cost *= 1.2
        
        return round(cost, 2)
    
    def generate_invoice(self, trip_data):
        cost = self.calculate_trip_cost(
            trip_data.get('from_location'), 
            trip_data.get('to_location'),
            trip_data.get('distance_km')
        )
        
        invoice = {
            'invoice_id': f"INV-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'trip_id': trip_data.get('booking_id'),
            'user_id': trip_data.get('user_id'),
            'total_amount': cost,
            'payment_status': 'pending',
            'generated_at': datetime.now().isoformat()
        }
        
        self.transaction_log.append(invoice)
        return invoice
    
    def get_financial_report(self, start_date=None, end_date=None):
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        period_transactions = [
            t for t in self.transaction_log 
            if start_date <= t['generated_at'][:10] <= end_date
        ]
        
        total_revenue = sum(t['total_amount'] for t in period_transactions)
        
        return {
            'period': f"{start_date} to {end_date}",
            'total_revenue': total_revenue,
            'total_transactions': len(period_transactions),
            'transactions': period_transactions
        }
