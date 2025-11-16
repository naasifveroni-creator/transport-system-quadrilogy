def fix_indentation():
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    # Fix the analytics route indentation (line 773)
    if len(lines) > 772:
        # Remove the extra spaces at the beginning of line 773
        lines[772] = '    business_analytics = BusinessAnalytics("transport.db")\n'
    
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    print("✅ Fixed indentation error!")

if __name__ == "__main__":
    fix_indentation()
