# Let's see what's actually in the time_slots route
with open('app.py', 'r') as f:
    lines = f.readlines()

# Find the time_slots route
for i, line in enumerate(lines):
    if 'def admin_time_slots():' in line:
        print(f"Time Slots route at line {i}:")
        for j in range(i, min(i+10, len(lines))):
            print(f"{j}: {lines[j].rstrip()}")
        break

print("\n" + "="*50)

# Find the analytics route  
for i, line in enumerate(lines):
    if 'def admin_analytics():' in line:
        print(f"Analytics route at line {i}:")
        for j in range(i, min(i+10, len(lines))):
            print(f"{j}: {lines[j].rstrip()}")
        break

print("\n" + "="*50)

# Find the user_management route
for i, line in enumerate(lines):
    if 'def admin_user_management():' in line:
        print(f"User Management route at line {i}:")
        for j in range(i, min(i+10, len(lines))):
            print(f"{j}: {lines[j].rstrip()}")
        break
