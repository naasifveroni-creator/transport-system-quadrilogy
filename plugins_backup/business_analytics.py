from datetime import datetime, timedelta
from typing import Dict, List

class BusinessAnalytics:
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def get_dashboard_metrics(self) -> Dict:
        data = self.data_loader()
        
        total_users = len(data.get('users', {}))
        total_drivers = len([u for u in data.get('users', {}).values() if u.get('is_driver')])
        total_agents = total_users - total_drivers - 1
        
        bookings = data.get('bookings', [])
        completed_trips = [b for b in bookings if b.get('status') == 'completed']
        pending_trips = [b for b in bookings if b.get('status') in ['unassigned', 'assigned', 'in-progress']]
        
        estimated_revenue = len(completed_trips) * 50
        
        return {
            'user_metrics': {
                'total_users': total_users,
                'total_drivers': total_drivers,
                'total_agents': total_agents,
                'new_users_today': self._get_new_users_today(data)
            },
            'booking_metrics': {
                'total_bookings': len(bookings),
                'completed_trips': len(completed_trips),
                'pending_trips': len(pending_trips),
                'completion_rate': len(completed_trips) / len(bookings) if bookings else 0
            },
            'financial_metrics': {
                'estimated_revenue': estimated_revenue,
                'average_trip_value': 50,
                'revenue_trend': 'up'
            },
            'operational_metrics': {
                'popular_routes': self._get_popular_routes(completed_trips),
                'peak_hours': self._get_peak_hours(bookings)
            }
        }
    
    def _get_new_users_today(self, data: Dict) -> int:
        return 0
    
    def _get_popular_routes(self, trips: List[Dict]) -> List[Dict]:
        route_counts = {}
        for trip in trips:
            route_key = f"{trip.get('from_location')} → {trip.get('to_location')}"
            route_counts[route_key] = route_counts.get(route_key, 0) + 1
        
        return [{'route': route, 'count': count} 
                for route, count in sorted(route_counts.items(), 
                                         key=lambda x: x[1], reverse=True)[:5]]
    
    def _get_peak_hours(self, bookings: List[Dict]) -> List[Dict]:
        hour_counts = {f"{i}pm" if i >= 18 else f"{i}am": 0 for i in range(18, 24)}
        hour_counts.update({f"{i}am": 0 for i in range(0, 7)})
        
        for booking in bookings:
            time_slot = booking.get('date_time', '').split()[-1] if ' ' in booking.get('date_time', '') else booking.get('date_time', '')
            if time_slot in hour_counts:
                hour_counts[time_slot] += 1
        
        return [{'hour': hour, 'bookings': count} 
                for hour, count in hour_counts.items()]

class GenderSafetyAlert:
    def __init__(self):
        self.safety_threshold = 0.7
    
    def check_trip_safety(self, passengers: List[Dict]) -> Dict:
        if not passengers:
            return {'alert': False, 'message': 'No passengers'}
        
        gender_count = {'male': 0, 'female': 0, 'other': 0}
        
        for passenger in passengers:
            gender = passenger.get('gender', 'unknown').lower()
            if gender in gender_count:
                gender_count[gender] += 1
            else:
                gender_count['other'] += 1
        
        total_passengers = len(passengers)
        male_ratio = gender_count['male'] / total_passengers if total_passengers > 0 else 0
        
        if gender_count['female'] == 1 and male_ratio >= self.safety_threshold:
            return {
                'alert': True,
                'level': 'high',
                'message': 'Safety alert: Single female passenger with male majority',
                'gender_breakdown': gender_count,
                'recommendations': [
                    'Assign female driver if available',
                    'Enable enhanced tracking',
                    'Share trip details with security'
                ]
            }
        elif gender_count['female'] > 0 and male_ratio >= 0.8:
            return {
                'alert': True,
                'level': 'medium',
                'message': 'Gender imbalance alert',
                'gender_breakdown': gender_count,
                'recommendations': [
                    'Monitor trip closely',
                    'Ensure driver is aware of composition'
                ]
            }
        
        return {
            'alert': False,
            'message': 'Trip composition appears normal',
            'gender_breakdown': gender_count
        }
