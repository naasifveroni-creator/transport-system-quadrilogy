with open('app.py', 'r') as f:
    content = f.read()

# Replace the routes to provide empty overview data
new_billing_route = '''@app.route('/admin/billing')
def admin_billing():
    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect('/login')
    # Provide empty overview data for now
    overview = {"total_revenue": 0, "pending_invoices": 0, "paid_invoices": 0}
    return render_template('admin_billing.html', overview=overview)'''

new_optimizer_route = '''@app.route('/admin/route_optimizer')
def admin_route_optimizer():
    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect('/login')
    # Provide empty overview data for now
    overview = {"total_routes": 0, "optimized_routes": 0, "fuel_savings": 0}
    return render_template('admin_route_optimizer.html', overview=overview)'''

new_tracking_route = '''@app.route('/admin/live_tracking')
def admin_live_tracking():
    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect('/login')
    # Provide empty overview data for now
    overview = {"total_vehicles": 0, "active_vehicles": 0, "idle_vehicles": 0}
    return render_template('admin_live_tracking.html', overview=overview)'''

import re
content = re.sub(r"@app.route\('/admin/billing'\).*?return render_template\('admin_billing.html'\)", new_billing_route, content, flags=re.DOTALL)
content = re.sub(r"@app.route\('/admin/route_optimizer'\).*?return render_template\('admin_route_optimizer.html'\)", new_optimizer_route, content, flags=re.DOTALL)
content = re.sub(r"@app.route\('/admin/live_tracking'\).*?return render_template\('admin_live_tracking.html'\)", new_tracking_route, content, flags=re.DOTALL)

with open('app.py', 'w') as f:
    f.write(content)

print("Fixed template variables - routes should work now")
