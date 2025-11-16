import csv
import io
from typing import List, Dict
from datetime import datetime
from werkzeug.security import generate_password_hash

class CampaignBulkRegistration:
    def __init__(self, data_loader, data_saver):
        self.data_loader = data_loader
        self.data_saver = data_saver
    
    def register_from_csv(self, csv_file, campaign_id: str, campaign_name: str) -> Dict:
        data = self.data_loader()
        
        if 'campaigns' not in data:
            data['campaigns'] = {}
        
        if campaign_id not in data['campaigns']:
            data['campaigns'][campaign_id] = {
                'name': campaign_name,
                'created_at': datetime.now().isoformat(),
                'users': []
            }
        
        results = {
            'campaign_id': campaign_id,
            'campaign_name': campaign_name,
            'successful': [],
            'failed': [],
            'total_processed': 0
        }
        
        try:
            csv_content = csv_file.stream.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(csv_content))
            
            for row in csv_reader:
                try:
                    username = row.get('username') or row.get('email').split('@')[0]
                    if not username:
                        raise ValueError("No username or email provided")
                    
                    if username in data['users']:
                        results['failed'].append({
                            'username': username,
                            'error': 'Username already exists'
                        })
                        continue
                    
                    hashed_password = generate_password_hash('TempPassword123!')
                    data['users'][username] = {
                        'username': username,
                        'name': row.get('name', username),
                        'password': hashed_password,
                        'is_admin': False,
                        'is_driver': False,
                        'registered_address': row.get('address', ''),
                        'travel_allowance': float(row.get('initial_allowance', 0)),
                        'penalties': [],
                        'campaign_id': campaign_id,
                        'gender': row.get('gender', 'unknown')
                    }
                    
                    results['successful'].append(username)
                    data['campaigns'][campaign_id]['users'].append(username)
                    
                except Exception as e:
                    results['failed'].append({
                        'username': row.get('username', 'unknown'),
                        'error': str(e)
                    })
                
                results['total_processed'] += 1
            
            self.data_saver(data)
            
        except Exception as e:
            results['error'] = f"CSV processing error: {str(e)}"
        
        return results
    
    def get_campaign_users(self, campaign_id: str) -> List[str]:
        data = self.data_loader()
        campaign = data.get('campaigns', {}).get(campaign_id, {})
        return campaign.get('users', [])
