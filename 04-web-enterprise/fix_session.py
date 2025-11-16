with open('app.py', 'r') as f:
    content = f.read()

# Add session modification after login
new_login_code = '''
    session['user_id'] = user[0]
    session['role'] = user[5]
    session.modified = True  # Force session save
    flash('Login successful!', 'success')
'''

import re
content = re.sub(r"session\['user_id'\] = user\[0\].*?flash\('Login successful!', 'success'\)", new_login_code, content, flags=re.DOTALL)

with open('app.py', 'w') as f:
    f.write(content)

print("Fixed session persistence")
