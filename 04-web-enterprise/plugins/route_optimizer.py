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
    
    def optimize_route(self, stops, algorithm='nearest_neighbor'):
        if len(stops) <= 2:
            return stops
        
        if algorithm == 'nearest_neighbor':
            return self._nearest_neighbor(stops)
        
        return stops
    
    def _nearest_neighbor(self, stops):
        optimized = [stops[0]]
        unvisited = stops[1:]
        
        while unvisited:
            last_stop = optimized[-1]
            nearest = min(unvisited, key=lambda stop: self._calculate_distance(last_stop, stop))
            optimized.append(nearest)
            unvisited.remove(nearest)
        
        return optimized
    
    def _calculate_distance(self, stop1, stop2):
        coords1 = self.location_coordinates.get(stop1, {'lat': 0, 'lng': 0})
        coords2 = self.location_coordinates.get(stop2, {'lat': 0, 'lng': 0})
        return ((coords2['lat'] - coords1['lat'])**2 + (coords2['lng'] - coords1['lng'])**2)**0.5
