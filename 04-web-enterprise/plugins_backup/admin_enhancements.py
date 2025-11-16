from typing import List, Dict
from datetime import datetime

class AdminUserManager:
    def __init__(self, data_loader, data_saver):
        self.data_loader = data_loader
        self.data_saver = data_saver
    
    def bulk_user_operations(self, operation: str, user_ids: List[str], **kwargs) -> Dict:
        data = self.data_loader()
        results = {
            'operation': operation,
            'successful': [],
            'failed': [],
            'total_processed': len(user_ids)
        }
        
        for user_id in user_ids:
            try:
                if user_id not in data['users']:
                    results['failed'].append({
                        'user_id': user_id,
                        'error': 'User not found'
                    })
                    continue
                
                if operation == 'deactivate':
                    data['users'][user_id]['active'] = False
                    results['successful'].append(user_id)
                
                elif operation == 'activate':
                    data['users'][user_id]['active'] = True
                    results['successful'].append(user_id)
                
                elif operation == 'update_role':
                    new_role = kwargs.get('new_role')
                    if new_role in ['agent', 'driver']:
                        data['users'][user_id]['is_driver'] = (new_role == 'driver')
                        results['successful'].append(user_id)
                    else:
                        results['failed'].append({
                            'user_id': user_id,
                            'error': f'Invalid role: {new_role}'
                        })
                
                elif operation == 'reset_password':
                    from werkzeug.security import generate_password_hash
                    data['users'][user_id]['password'] = generate_password_hash('TempPassword123!')
                    results['successful'].append(user_id)
                
                else:
                    results['failed'].append({
                        'user_id': user_id,
                        'error': f'Unknown operation: {operation}'
                    })
                    
            except Exception as e:
                results['failed'].append({
                    'user_id': user_id,
                    'error': str(e)
                })
        
        if results['successful']:
            self.data_saver(data)
        
        return results
    
    def advanced_user_search(self, filters: Dict) -> List[Dict]:
        data = self.data_loader()
        users = data.get('users', {})
        results = []
        
        for user_id, user_data in users.items():
            if user_id == 'admin':
                continue
            
            matches = True
            
            if filters.get('user_type'):
                if filters['user_type'] == 'driver' and not user_data.get('is_driver'):
                    matches = False
                elif filters['user_type'] == 'agent' and user_data.get('is_driver'):
                    matches = False
            
            if matches and filters.get('campaign_id'):
                if user_data.get('campaign_id') != filters['campaign_id']:
                    matches = False
            
            if matches and filters.get('active') is not None:
                if user_data.get('active', True) != filters['active']:
                    matches = False
            
            if matches:
                results.append({
                    'user_id': user_id,
                    'name': user_data.get('name'),
                    'is_driver': user_data.get('is_driver', False),
                    'campaign_id': user_data.get('campaign_id'),
                    'registered_address': user_data.get('registered_address'),
                    'travel_allowance': user_data.get('travel_allowance', 0),
                    'active': user_data.get('active', True)
                })
        
        return results

class AdminDashboardMetrics:
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def get_enhanced_overview(self) -> Dict:
        data = self.data_loader()
        
        from plugins.business_analytics import BusinessAnalytics
        analytics = BusinessAnalytics(self.data_loader)
        business_metrics = analytics.get_dashboard_metrics()
        
        admin_metrics = {
            'system_health': {
                'total_bookings_today': self._get_todays_bookings_count(data),
                'active_drivers': self._get_active_drivers_count(data),
                'system_uptime': '99.9%',
                'pending_actions': self._get_pending_actions_count(data)
            },
            'safety_metrics': {
                'safety_alerts_today': 0,
                'incidents_reported': 0,
                'preventive_alerts': 0
            }
        }
        
        return {
            **business_metrics,
            **admin_metrics
        }
    
    def _get_todays_bookings_count(self, data: Dict) -> int:
        today = datetime.now().strftime('%Y-%m-%d')
        return len([b for b in data.get('bookings', []) 
                   if b.get('date_time', '').startswith(today)])
    
    def _get_active_drivers_count(self, data: Dict) -> int:
        return len([u for u in data.get('users', {}).values() 
                   if u.get('is_driver') and u.get('active', True)])
    
    def _get_pending_actions_count(self, data: Dict) -> int:
        return len([b for b in data.get('bookings', []) 
                   if b.get('status') in ['unassigned', 'assigned']])
