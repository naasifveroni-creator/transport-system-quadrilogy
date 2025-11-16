def fix_all_indentation():
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    # Fix line 782 (user_management route)
    if len(lines) > 781:
        lines[781] = '    user_mgr = UserManager("transport.db")\n'
    
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    print("✅ Fixed user_management route indentation!")
    
    # Verify no more syntax errors
    import subprocess
    result = subprocess.run(['python', '-m', 'py_compile', 'app.py'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("🎉 No more syntax errors! App should run now.")
    else:
        print("❌ Still has errors:")
        print(result.stderr)

if __name__ == "__main__":
    fix_all_indentation()
