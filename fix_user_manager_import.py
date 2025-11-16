def fix_import():
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    # Find where to add the import (after other plugin imports)
    for i, line in enumerate(lines):
        if 'from plugins.business_analytics import BusinessAnalytics' in line:
            lines.insert(i + 1, 'from plugins.user_manager import UserManager\n')
            break
    
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    print("✅ Added UserManager import")

if __name__ == "__main__":
    fix_import()
