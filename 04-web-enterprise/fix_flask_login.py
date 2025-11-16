with open('app.py', 'r') as f:
    content = f.read()

# Replace all the old session checks with Flask-Login checks
content = content.replace(
    "if 'user_id' not in session or session.get('role') != 'admin':", 
    "if not current_user.is_authenticated or not current_user.is_admin:"
)

with open('app.py', 'w') as f:
    f.write(content)

print("Fixed route protection to use Flask-Login")
