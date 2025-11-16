import math
from typing import List, Dict

class RouteOptimizer:
    def __init__(self):
        self.location_coordinates = {
            'Blvd': {'lat': -33.9249, 'lng': 18.4241},
            'Match Factory': {'lat': -33.9270, 'lng': 18.4260},
            'Adderly': {'lat': -33.9215, 'lng': 18.4220},
            'Wembly Sqr': {'lat': -33.9190, 'lng': 18.4200},
            'Campus A': {'lat': -33.9300, 'lng': 18.4300},
            'Campus B': {'lat': -33.9320, 'lng': 18.4320},
            'Campus C': {'lat': -33.9280, 'lng': 18.4280},
            'Downtown': {'lat': -33.9250, 'lng': 18.4250},
            'Airport': {'lat': -33.9648, 'lng': 18.6017},
            'Train Station': {'lat': -33.9199, 'lng': 18.4298}
        }
    
    def optimize_route(self, stops: List[str], algorithm='nearest_neighbor') -> List[str]:
        if not stops or len(stops) < 2:
            return stops
        
        if algorithm == 'nearest_neighbor':
            return self._nearest_neighbor(stops)
        else:
            return stops
    
    def _nearest_neighbor(self, stops: List[str]) -> List[str]:
        if len(stops) <= 2:
            return stops
        
        optimized = [stops[0]]
        unvisited = stops[1:]
        
        while unvisited:
            last_stop = optimized[-1]
            nearest = min(unvisited, 
                         key=lambda stop: self._calculate_distance(
                             self.location_coordinates.get(last_stop, {}).get('lat', 0),
                             self.location_coordinates.get(last_stop, {}).get('lng', 0),
                             self.location_coordinates.get(stop, {}).get('lat', 0),
                             self.location_coordinates.get(stop, {}).get('lng', 0)
                         ))
            optimized.append(nearest)
            unvisited.remove(nearest)
        
        return optimized
    
    def _calculate_distance(self, lat1, lng1, lat2, lng2):
        return math.sqrt((lat2 - lat1)**2 + (lng2 - lng1)**2)
    
    def generate_map_data(self, route: List[str]) -> Dict:
        coordinates = []
        for location in route:
            if location in self.location_coordinates:
                coords = self.location_coordinates[location]
                coordinates.append({
                    'location': location,
                    'lat': coords['lat'],
                    'lng': coords['lng']
                })
        
        return {
            'route': route,
            'coordinates': coordinates,
            'waypoints': len(coordinates)
        }
