import requests
from config import GOOGLE_MAPS_API_KEY

def calc_duration(origin_location, destination_location, mode=None):
    print(f"mode: ", mode)

    params = {
        'origin': f"{origin_location['lat']},{origin_location['lng']}",
        'destination': f"{destination_location['lat']},{destination_location['lng']}",
        'mode': mode,
        'departure_time': 'now',
        'key': GOOGLE_MAPS_API_KEY
    }

    url = 'https://maps.googleapis.com/maps/api/directions/json'
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        route = data['routes'][0]
        leg = route['legs'][0]
        duration = leg['duration']['text']
        return duration
    else:
        print(f"Google Maps API error: {data['status']}")
        return None
