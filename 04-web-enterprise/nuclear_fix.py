def nuclear_fix():
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    # Delete line 773 and insert a new one
    if len(lines) > 772:
        del lines[772]
        lines.insert(772, '    business_analytics = BusinessAnalytics("transport.db")\n')
    
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    print("✅ Nuclear fix applied!")

if __name__ == "__main__":
    nuclear_fix()
