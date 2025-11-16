import re

def fix_all_errors():
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Fix 1: Remove the base_slots reference from time_slots route
    content = re.sub(r"return render_template\('admin_time_slots\.html', default_slots=time_slot_manager\.base_slots\)", 
                    "return render_template('admin_time_slots.html', global_settings=global_settings, campaign_slots=campaign_slots)", 
                    content)
    
    # Fix 2: Fix the business_analytics call (remove extra parentheses)
    content = re.sub(r"business_analytics = BusinessAnalytics\('transport\.db'\)", 
                    "business_analytics = BusinessAnalytics('transport.db')", 
                    content)
    
    # Fix 3: Fix the user_management route to use the new plugin
    content = re.sub(r"return render_template\('admin_user_management\.html', users=data\.get\('users', \{\}\)\)", 
                    "return render_template('admin_user_management.html', users=users)", 
                    content)
    
    with open('app.py', 'w') as f:
        f.write(content)
    
    print("✅ Fixed all errors in app.py")

if __name__ == "__main__":
    fix_all_errors()
