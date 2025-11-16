def fix_indentation():
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    # Fix line 782 - ensure proper 4-space indentation
    if len(lines) > 781:
        print(f"Fixing line 782: '{lines[781].rstrip()}'")
        lines[781] = '    user_mgr = UserManager("transport.db")\n'
        print(f"Fixed to: '{lines[781].rstrip()}'")
    
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    print("✅ Fixed indentation in backup")
    
    # Test if it compiles
    import subprocess
    result = subprocess.run(['python', '-m', 'py_compile', 'app.py'], capture_output=True, text=True)
    if result.returncode == 0:
        print("🎉 Backup now compiles! Starting Flask...")
        subprocess.run(['python', 'app.py'])
    else:
        print("❌ Still broken:")
        print(result.stderr)

if __name__ == "__main__":
    fix_indentation()
