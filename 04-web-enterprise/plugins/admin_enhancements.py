class AdminUserManager:
    def __init__(self, data_loader, data_saver):
        self.data_loader = data_loader
        self.data_saver = data_saver
    
    def bulk_operations(self, operation, user_ids, **kwargs):
        data = self.data_loader()
        results = {'successful': [], 'failed': []}
        
        for user_id in user_ids:
            try:
                if user_id in data['users']:
                    if operation == 'deactivate':
                        data['users'][user_id]['active'] = False
                    elif operation == 'activate':
                        data['users'][user_id]['active'] = True
                    elif operation == 'delete':
                        del data['users'][user_id]
                    results['successful'].append(user_id)
                else:
                    results['failed'].append({'user_id': user_id, 'error': 'User not found'})
            except Exception as e:
                results['failed'].append({'user_id': user_id, 'error': str(e)})
        
        if results['successful']:
            self.data_saver(data)
        
        return results
