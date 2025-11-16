import re

def update_app_py():
    # Read the current app.py
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Define the COMPLETE plugin routes block
    complete_plugin_routes = '''
# ===== COMPLETE PLUGIN ROUTES =====
from plugins.time_slot_manager import TimeSlotManager
from plugins.business_analytics import BusinessAnalytics
from plugins.user_manager import UserManager
from plugins.campaign_manager import CampaignManager

# Time Slot Manager Routes
@app.route('/admin/time_slots')
def admin_time_slots():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    
    time_slot_mgr = TimeSlotManager('transport.db')
    global_settings = time_slot_mgr.get_global_settings()
    campaign_slots = time_slot_mgr.get_campaign_slots()
    
    return render_template('admin_time_slots.html',
                         global_settings=global_settings,
                         campaign_slots=campaign_slots)

@app.route('/admin/time_slots/update_global', methods=['POST'])
def update_global_time_slots():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    try:
        enabled = request.form.get('enabled') == 'true'
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        
        time_slot_mgr = TimeSlotManager('transport.db')
        time_slot_mgr.update_global_settings(enabled, start_time, end_time)
        
        return jsonify({'success': True, 'message': 'Global settings updated'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/time_slots/create_campaign', methods=['POST'])
def create_campaign_slot():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    try:
        campaign_name = request.form.get('campaign_name')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        days_of_week = request.form.get('days_of_week', '1,2,3,4,5,6,7')
        
        time_slot_mgr = TimeSlotManager('transport.db')
        time_slot_mgr.create_campaign_slot(campaign_name, start_time, end_time, days_of_week)
        
        return jsonify({'success': True, 'message': 'Campaign time slot created'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Business Analytics Routes
@app.route('/admin/analytics')
def admin_analytics():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    
    analytics = BusinessAnalytics('transport.db')
    metrics = analytics.get_dashboard_metrics()
    
    return render_template('admin_analytics.html', metrics=metrics)

@app.route('/admin/analytics/data')
def analytics_data():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'})
    
    analytics = BusinessAnalytics('transport.db')
    metrics = analytics.get_dashboard_metrics()
    
    return jsonify(metrics)

# User Management Routes
@app.route('/admin/user_management')
def admin_user_management():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    
    user_mgr = UserManager('transport.db')
    users = user_mgr.get_all_users()
    
    return render_template('admin_user_management.html', users=users)

@app.route('/admin/user_management/bulk_action', methods=['POST'])
def user_bulk_action():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    try:
        user_ids = request.form.getlist('user_ids[]')
        action = request.form.get('action')
        
        user_mgr = UserManager('transport.db')
        success, message = user_mgr.bulk_update_users(user_ids, action)
        
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/user_management/export')
def export_users():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    
    user_mgr = UserManager('transport.db')
    csv_data = user_mgr.export_users_csv()
    
    response = make_response(csv_data)
    response.headers["Content-Disposition"] = "attachment; filename=users_export.csv"
    response.headers["Content-type"] = "text/csv"
    return response

@app.route('/admin/user_management/search')
def search_users():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'})
    
    query = request.args.get('q', '')
    user_mgr = UserManager('transport.db')
    users = user_mgr.search_users(query)
    
    return jsonify(users)

# Campaign Registration Routes
@app.route('/admin/bulk_register')
def admin_bulk_register():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    
    campaign_mgr = CampaignManager('transport.db')
    campaigns = campaign_mgr.get_campaigns()
    import_history = campaign_mgr.get_import_history()
    
    return render_template('admin_bulk_register.html', 
                         campaigns=campaigns, 
                         import_history=import_history)

@app.route('/admin/bulk_register/create_campaign', methods=['POST'])
def create_campaign():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    try:
        name = request.form.get('name')
        description = request.form.get('description', '')
        
        campaign_mgr = CampaignManager('transport.db')
        campaign_id = campaign_mgr.create_campaign(name, description)
        
        return jsonify({'success': True, 'message': 'Campaign created successfully', 'campaign_id': campaign_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/bulk_register/upload_csv', methods=['POST'])
def upload_csv():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    try:
        campaign_id = request.form.get('campaign_id')
        csv_file = request.files.get('csv_file')
        
        if not csv_file or not csv_file.filename.endswith('.csv'):
            return jsonify({'success': False, 'error': 'Please upload a valid CSV file'})
        
        campaign_mgr = CampaignManager('transport.db')
        success, message = campaign_mgr.process_csv_import(campaign_id, csv_file)
        
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
'''

    # Strategy 1: Remove existing plugin routes if they exist
    patterns_to_remove = [
        r'# ===== PLUGIN ROUTES.*?@app\.route\(\'/admin/bulk_register\'\).*?return render_template.*?\)',
        r'@app\.route\(\'/admin/time_slots\'\).*?def admin_bulk_register\(\):.*?return render_template.*?\)',
        r'# ===== TIME SLOT MANAGER ROUTES.*?@app\.route\(\'/admin/bulk_register/upload_csv\'\).*?return jsonify.*?\)',
    ]
    
    cleaned_content = content
    for pattern in patterns_to_remove:
        cleaned_content = re.sub(pattern, '', cleaned_content, flags=re.DOTALL)
    
    # Strategy 2: Find a good insertion point (before app.run)
    if 'if __name__ == "__main__":' in cleaned_content:
        # Insert before app.run
        new_content = cleaned_content.replace(
            'if __name__ == "__main__":',
            complete_plugin_routes + '\n\nif __name__ == "__main__":'
        )
        print("✅ Inserted plugin routes before app.run")
    else:
        # Just append to the end
        new_content = cleaned_content + '\n\n' + complete_plugin_routes
        print("✅ Appended plugin routes to end of file")
    
    # Write the updated content
    with open('app.py', 'w') as f:
        f.write(new_content)
    
    print("🎉 SUCCESS! app.py has been automatically updated with all plugin routes!")
    print("📋 All 4 plugins are now fully integrated:")
    print("   ✅ Time Slot Manager")
    print("   ✅ Business Analytics") 
    print("   ✅ User Management")
    print("   ✅ Campaign Registration")
    print("🚀 Restart your Flask app and test all plugins!")

if __name__ == "__main__":
    update_app_py()
