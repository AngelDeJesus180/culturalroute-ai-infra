import math

class GeoService:

    def __init__(self):
        self.points = {}

    def save_point(self, point):
        self.points[point.place_id] = point
        return {"message": "Ubicación guardada"}

    def get_location(self, place_id):
        return self.points.get(place_id, "No encontrado")

    def calculate_distance(self, lat1, lng1, lat2, lng2):
        # Fórmula simple (Haversine simplificada)
        return {
            "distance": math.sqrt((lat2 - lat1)**2 + (lng2 - lng1)**2)
        }
