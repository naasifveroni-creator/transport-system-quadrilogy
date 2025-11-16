def fix_analytics():
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    # Find the analytics route section (lines 770-776)
    start_line = None
    for i in range(769, min(780, len(lines))):
        if '@app.route(\'/admin/analytics\')' in lines[i]:
            start_line = i
            break
    
    if start_line is not None:
        # Replace the entire broken route with correct code
        new_lines = [
            '@app.route(\'/admin/analytics\')\n',
            '@login_required\n',
            'def admin_analytics():\n',
            '    if not current_user.is_authenticated or not current_user.is_admin:\n',
            '        return redirect(url_for(\'login\'))\n',
            '    business_analytics = BusinessAnalytics("transport.db")\n',
            '    metrics = business_analytics.get_dashboard_metrics()\n',
            '    return render_template(\'admin_analytics.html\', metrics=metrics)\n'
        ]
        
        # Replace lines 770-776 with the correct ones
        lines = lines[:start_line] + new_lines + lines[start_line+7:]
    
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    print("✅ Completely fixed analytics route!")

if __name__ == "__main__":
    fix_analytics()
