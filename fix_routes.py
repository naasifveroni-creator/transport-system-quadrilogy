with open('app.py', 'r') as f:
    content = f.read()

# Replace the broken routes section
new_routes = '''
# ===== BILLING ROUTES =====
@app.route('/admin/billing')
def admin_billing():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    return render_template('admin_billing.html')

# ===== ROUTE OPTIMIZER ROUTES =====  
@app.route('/admin/route_optimizer')
def admin_route_optimizer():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    return render_template('admin_route_optimizer.html')

# ===== LIVE TRACKING ROUTES =====
@app.route('/admin/live_tracking')
def admin_live_tracking():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    return render_template('admin_live_tracking.html')
'''

import re
content = re.sub(r'# ===== BILLING ROUTES =====.*?if __name__ == "__main__":', new_routes + '\n\nif __name__ == "__main__":', content, flags=re.DOTALL)

with open('app.py', 'w') as f:
    f.write(content)

print("Fixed routes - removed plugin imports")
