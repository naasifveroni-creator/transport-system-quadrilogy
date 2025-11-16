import re

def fix_timeslot_calls():
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Find and replace all old TimeSlotManager() calls
    old_pattern = r'TimeSlotManager\(\)'
    new_content = re.sub(old_pattern, 'TimeSlotManager("transport.db")', content)
    
    # Also fix any other instances without parameters
    old_pattern2 = r'TimeSlotManager\s*\('
    new_content = re.sub(old_pattern2, 'TimeSlotManager("transport.db", ', new_content)
    
    with open('app.py', 'w') as f:
        f.write(new_content)
    
    print("✅ Fixed all TimeSlotManager calls in app.py")

if __name__ == "__main__":
    fix_timeslot_calls()
