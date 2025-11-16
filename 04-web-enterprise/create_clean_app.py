def create_clean_app():
    # Read the original working parts
    with open('app.py.corrupted', 'r') as f:
        content = f.read()
    
    # Remove everything from the corrupted billing routes onward
    import re
    content = re.sub(r'# ===== BILLING ROUTES =====.*', '', content, flags=re.DOTALL)
    
    # Add clean, simple routes at the end
    clean_routes = '''
# ===== BILLING ROUTES =====
from plugins.billing import Billing

@app.route('/admin/billing')
def admin_billing():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    billing = Billing('transport.db')
    overview = billing.get_billing_overview()
    return render_template('admin_billing.html', overview=overview)

# ===== ROUTE OPTIMIZER ROUTES =====
from plugins.route_optimizer import RouteOptimizer

@app.route('/admin/route_optimizer')
def admin_route_optimizer():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    optimizer = RouteOptimizer('transport.db')
    overview = optimizer.get_route_overview()
    return render_template('admin_route_optimizer.html', overview=overview)

# ===== LIVE TRACKING ROUTES =====
from plugins.live_tracking import LiveTracking

@app.route('/admin/live_tracking')
def admin_live_tracking():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    tracking = LiveTracking('transport.db')
    overview = tracking.get_live_overview()
    return render_template('admin_live_tracking.html', overview=overview)
'''
    
    # Add the clean routes before app.run()
    if 'if __name__ == "__main__":' in content:
        content = content.replace('if __name__ == "__main__":', clean_routes + '\n\nif __name__ == "__main__":')
    
    with open('app.py', 'w') as f:
        f.write(content)
    
    print("✅ Created clean app.py with working routes")

if __name__ == "__main__":
    create_clean_app()
