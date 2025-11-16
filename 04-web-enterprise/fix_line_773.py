def fix_line_773():
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    # Fix line 773 - ensure it has exactly 4 spaces of indentation
    if len(lines) > 772:
        lines[772] = '    business_analytics = BusinessAnalytics("transport.db")\n'
    
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    print("✅ Fixed line 773 indentation!")
    
    # Verify the fix
    with open('app.py', 'r') as f:
        fixed_line = f.readlines()[772]
        print(f"Line 773 now: '{fixed_line.rstrip()}'")

if __name__ == "__main__":
    fix_line_773()
