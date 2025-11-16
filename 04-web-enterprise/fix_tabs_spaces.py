def fix_tabs_spaces():
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Replace tabs with 4 spaces
    content = content.replace('\t', '    ')
    
    # Fix specific problematic lines - replace 20 spaces with 4 spaces
    content = content.replace('                    user_mgr = UserManager("transport.db")', '    user_mgr = UserManager("transport.db")')
    content = content.replace('                    users = user_mgr.get_all_users()', '    users = user_mgr.get_all_users()')
    content = content.replace('                    return render_template(', '    return render_template(')
    content = content.replace('                    data = load_data()', '    data = load_data()')
    
    with open('app.py', 'w') as f:
        f.write(content)
    
    print("✅ Fixed tabs and spaces!")
    
    # Test
    import subprocess
    result = subprocess.run(['python', '-m', 'py_compile', 'app.py'], capture_output=True, text=True)
    if result.returncode == 0:
        print("🎉 SUCCESS! Starting Flask...")
        subprocess.run(['python', 'app.py'])
    else:
        print("❌ Still broken:")
        print(result.stderr)

if __name__ == "__main__":
    fix_tabs_spaces()
