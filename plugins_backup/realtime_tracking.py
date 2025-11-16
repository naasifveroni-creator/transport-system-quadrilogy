import time
from datetime import datetime
from typing import Dict, List

class RealTimeTracker:
    def __init__(self):
        self.driver_locations = {}
        self.trip_tracking = {}
    
    def update_driver_location(self, driver_id: str, lat: float, lng: float, trip_id: str = None):
        self.driver_locations[driver_id] = {
            'lat': lat,
            'lng': lng,
            'timestamp': datetime.now().isoformat(),
            'trip_id': trip_id,
            'speed': self._calculate_speed(driver_id, lat, lng)
        }
        
        if trip_id:
            if trip_id not in self.trip_tracking:
                self.trip_tracking[trip_id] = []
            
            self.trip_tracking[trip_id].append({
                'lat': lat,
                'lng': lng,
                'timestamp': datetime.now().isoformat(),
                'driver_id': driver_id
            })
    
    def get_driver_location(self, driver_id: str) -> Dict:
        return self.driver_locations.get(driver_id)
    
    def get_trip_path(self, trip_id: str) -> List[Dict]:
        return self.trip_tracking.get(trip_id, [])
    
    def _calculate_speed(self, driver_id: str, new_lat: float, new_lng: float) -> float:
        previous = self.driver_locations.get(driver_id)
        if not previous:
            return 0.0
        
        time_diff = (datetime.now() - datetime.fromisoformat(previous['timestamp'])).total_seconds()
        if time_diff == 0:
            return 0.0
        
        distance = ((new_lat - previous['lat'])**2 + (new_lng - previous['lng'])**2)**0.5
        speed_kmh = (distance * 111) / (time_diff / 3600)
        
        return round(speed_kmh, 2)

class TimeSlotManager:
    def __init__(self):
        self.base_slots = ['6pm','7pm','8pm','9pm','10pm','11pm','12pm','12am','1am','2am','3am','4am','5am','6am']
        self.campaign_preferences = {}
    
    def get_available_slots(self, campaign_id: str = None) -> List[str]:
        if campaign_id and campaign_id in self.campaign_preferences:
            return self.campaign_preferences[campaign_id]
        
        return self.base_slots
    
    def set_campaign_slots(self, campaign_id: str, slots: List[str]):
        self.campaign_preferences[campaign_id] = slots
    
    def add_campaign_from_csv(self, csv_data: str):
        pass
