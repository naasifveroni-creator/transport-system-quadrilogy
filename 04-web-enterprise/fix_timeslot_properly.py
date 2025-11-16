def fix_timeslot():
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    # Fix line 96 specifically
    if len(lines) > 95:
        lines[95] = 'time_slot_manager = TimeSlotManager("transport.db")\n'
    
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    print("✅ Fixed line 96 in app.py")

if __name__ == "__main__":
    fix_timeslot()
