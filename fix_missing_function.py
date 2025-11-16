def fix_missing_function():
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    # Find the broken user_management route (around line 778)
    for i in range(777, 783):
        if '@app.route(\'/admin/user_management\')' in lines[i]:
            # Insert the missing function definition
            lines.insert(i + 2, 'def admin_user_management():\n')
            break
    
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    print("✅ Added missing function definition!")
    
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
    fix_missing_function()
