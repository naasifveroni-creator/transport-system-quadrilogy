def fix_user_management():
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    # Find the user_management route section
    for i in range(780, min(790, len(lines))):
        if '@app.route(\'/admin/user_management\')' in lines[i]:
            # Replace the broken route with correct code
            new_lines = [
                '@app.route(\'/admin/user_management\')\n',
                '@login_required\n', 
                'def admin_user_management():\n',
                '    if not current_user.is_authenticated or not current_user.is_admin:\n',
                '        return redirect(url_for(\'login\'))\n',
                '    user_mgr = UserManager("transport.db")\n',
                '    users = user_mgr.get_all_users()\n',
                '    return render_template(\'admin_user_management.html\', users=users)\n'
            ]
            
            # Replace the broken section (remove the old broken lines)
            lines = lines[:i] + new_lines + lines[i+6:]
            break
    
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    print("✅ Fixed user_management route with proper function definition!")
    
    # Verify no syntax errors
    import subprocess
    result = subprocess.run(['python', '-m', 'py_compile', 'app.py'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("🎉 ALL SYNTAX ERRORS FIXED! Starting Flask...")
        subprocess.run(['python', 'app.py'])
    else:
        print("❌ Still has errors:")
        print(result.stderr)

if __name__ == "__main__":
    fix_user_management()
