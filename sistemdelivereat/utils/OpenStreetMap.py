from geopy.geocoders import Nominatim

class Geocoder:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="sistemdelivereat")
        self.error = None

    def obtener_coordenadas(self, direccion):
        try:
            location = self.geolocator.geocode(direccion)
            if location:
                return (location.latitude, location.longitude)
            else:
                return None
        except Exception as e:
            self.error = str(e)
            return None

