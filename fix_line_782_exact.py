def fix_line_782():
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    # Show what we're replacing
    print(f"Before: '{lines[781].rstrip()}'")
    
    # Replace line 782 with EXACT 4-space indentation
    lines[781] = '    user_mgr = UserManager("transport.db")\n'
    
    print(f"After: '{lines[781].rstrip()}'")
    
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    # Verify the fix
    import subprocess
    result = subprocess.run(['python', '-m', 'py_compile', 'app.py'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("🎉 SUCCESS! No more syntax errors!")
    else:
        print("❌ STILL BROKEN:")
        print(result.stderr)

if __name__ == "__main__":
    fix_line_782()
