from datetime import datetime

class RealTimeTracker:
    def __init__(self):
        self.driver_locations = {}
        self.trip_tracking = {}
    
    def update_driver_location(self, driver_id, lat, lng, trip_id=None):
        self.driver_locations[driver_id] = {
            'lat': lat, 'lng': lng, 'timestamp': datetime.now().isoformat(), 'trip_id': trip_id
        }
        
        if trip_id:
            if trip_id not in self.trip_tracking:
                self.trip_tracking[trip_id] = []
            self.trip_tracking[trip_id].append({
                'lat': lat, 'lng': lng, 'timestamp': datetime.now().isoformat(), 'driver_id': driver_id
            })
    
    def get_driver_location(self, driver_id):
        return self.driver_locations.get(driver_id)
    
    def get_trip_path(self, trip_id):
        return self.trip_tracking.get(trip_id, [])
