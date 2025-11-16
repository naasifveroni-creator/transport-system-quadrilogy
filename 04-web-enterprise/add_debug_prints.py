def add_debug():
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Add debug prints to each new route
    debug_billing = '''@app.route('/admin/billing')
def admin_billing():
    print("🚀 BILLING ROUTE CALLED")
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    billing = Billing('transport.db')
    overview = billing.get_billing_overview()
    return render_template('admin_billing.html', overview=overview)'''
    
    debug_route = '''@app.route('/admin/route_optimizer')
def admin_route_optimizer():
    print("🚀 ROUTE OPTIMIZER CALLED")  
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    optimizer = RouteOptimizer('transport.db')
    overview = optimizer.get_route_overview()
    return render_template('admin_route_optimizer.html', overview=overview)'''
    
    debug_tracking = '''@app.route('/admin/live_tracking')
def admin_live_tracking():
    print("🚀 LIVE TRACKING CALLED")
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    tracking = LiveTracking('transport.db')
    overview = tracking.get_live_overview()
    return render_template('admin_live_tracking.html', overview=overview)'''
    
    content = content.replace('''@app.route('/admin/billing')
def admin_billing():''', debug_billing)
    content = content.replace('''@app.route('/admin/route_optimizer')
def admin_route_optimizer():''', debug_route)
    content = content.replace('''@app.route('/admin/live_tracking')
def admin_live_tracking():''', debug_tracking)
    
    with open('app.py', 'w') as f:
        f.write(content)
    
    print("✅ Added debug prints")

if __name__ == "__main__":
    add_debug()
