def fix_routes():
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    # Fix Time Slots route (line 762-765)
    if len(lines) > 762:
        lines[762] = 'def admin_time_slots():\n'
        lines[763] = '    if not current_user.is_authenticated or not current_user.is_admin:\n'
        lines[764] = '        return redirect(url_for(\'login\'))\n'
        lines[765] = '    time_slot_mgr = TimeSlotManager("transport.db")\n'
        lines.insert(766, '    global_settings = time_slot_mgr.get_global_settings()\n')
        lines.insert(767, '    campaign_slots = time_slot_mgr.get_campaign_slots()\n')
        lines.insert(768, '    return render_template(\'admin_time_slots.html\', global_settings=global_settings, campaign_slots=campaign_slots)\n')
    
    # Fix Analytics route (line 769-773)
    if len(lines) > 772:
        lines[772] = '    business_analytics = BusinessAnalytics("transport.db")\n'
        lines[773] = '    metrics = business_analytics.get_dashboard_metrics()\n'
        lines[774] = '    return render_template(\'admin_analytics.html\', metrics=metrics)\n'
    
    # Fix User Management route (line 777-781)
    if len(lines) > 780:
        lines[780] = '    user_mgr = UserManager("transport.db")\n'
        lines[781] = '    users = user_mgr.get_all_users()\n'
        lines[782] = '    return render_template(\'admin_user_management.html\', users=users)\n'
    
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    print("✅ Fixed ALL routes with proper plugin initialization!")

if __name__ == "__main__":
    fix_routes()
