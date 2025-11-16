from datetime import datetime, timedelta
from typing import Dict, List

class BillingMIS:
    def __init__(self):
        self.base_fare = 50.00
        self.distance_rate = 15.00
        self.transaction_log = []
    
    def calculate_trip_cost(self, from_location: str, to_location: str, distance_km: float = None) -> float:
        base_cost = self.base_fare
        
        if distance_km:
            base_cost += distance_km * self.distance_rate
        
        premium_locations = ['Airport', 'Train Station']
        if from_location in premium_locations or to_location in premium_locations:
            base_cost *= 1.2
        
        return round(base_cost, 2)
    
    def generate_invoice(self, trip_data: Dict) -> Dict:
        cost = self.calculate_trip_cost(
            trip_data.get('from_location'), 
            trip_data.get('to_location'),
            trip_data.get('distance_km')
        )
        
        invoice = {
            'invoice_id': f"INV-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'trip_id': trip_data.get('booking_id'),
            'user_id': trip_data.get('user_id'),
            'driver_id': trip_data.get('driver_id'),
            'base_fare': self.base_fare,
            'distance_charge': (trip_data.get('distance_km', 0) * self.distance_rate) if trip_data.get('distance_km') else 0,
            'total_amount': cost,
            'payment_status': 'pending',
            'generated_at': datetime.now().isoformat(),
            'trip_details': {
                'from': trip_data.get('from_location'),
                'to': trip_data.get('to_location'),
                'date_time': trip_data.get('date_time')
            }
        }
        
        self.transaction_log.append(invoice)
        return invoice
    
    def get_financial_report(self, start_date: str = None, end_date: str = None) -> Dict:
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        period_transactions = [
            t for t in self.transaction_log 
            if start_date <= t['generated_at'][:10] <= end_date
        ]
        
        total_revenue = sum(t['total_amount'] for t in period_transactions)
        total_trips = len(period_transactions)
        
        return {
            'period': f"{start_date} to {end_date}",
            'total_revenue': total_revenue,
            'total_trips': total_trips,
            'average_revenue_per_trip': total_revenue / total_trips if total_trips > 0 else 0,
            'transactions': period_transactions
        }
