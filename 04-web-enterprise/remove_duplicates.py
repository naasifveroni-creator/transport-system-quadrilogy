def remove_duplicates():
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    # Find where the duplicate routes start (around line 890)
    start_line = None
    for i, line in enumerate(lines):
        if '# ===== BILLING ROUTES =====' in line and i > 800:
            start_line = i
            break
    
    if start_line:
        # Remove from the duplicate section to the end
        lines = lines[:start_line]
        
        with open('app.py', 'w') as f:
            f.writelines(lines)
        
        print("✅ Removed duplicate routes!")
    else:
        print("✅ No duplicates found")

if __name__ == "__main__":
    remove_duplicates()
