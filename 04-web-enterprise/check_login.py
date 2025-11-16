with open('app.py', 'r') as f:
    content = f.read()

import re
login_match = re.search(r'@app.route\(\'/login\'.*?def login\(\):.*?return render_template\(\'login.html\'\)', content, re.DOTALL)
if login_match:
    print("FOUND LOGIN ROUTE:")
    print(login_match.group(0)[:500] + "..." if len(login_match.group(0)) > 500 else login_match.group(0))
else:
    print("LOGIN ROUTE NOT FOUND IN EXPECTED FORMAT")
