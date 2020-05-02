from geopy import Location
from geopy.geocoders import Nominatim, GeoNames
from geopy.distance import Geodesic

geolocator = Nominatim(user_agent="QTestingService")
location: Location = geolocator.geocode("Radioweg 45, Almere")
location2: Location = geolocator.geocode("Vrouwenakker 12a, Vrouwenakker, Nederland")
print(location.address)
print(location.raw)
print(location.latitude, location.longitude)

import requests
import json

send_url = 'http://ipinfo.io/loc'
r = requests.get(send_url)
loc = r.text
print(loc)

location: Location = geolocator.reverse(f"{loc}")
print(location.address)

import geocoder
g = geocoder.ip('me')
print(f"{g.latlng[0]},{g.latlng[1]}")
# print(g.latlng)

location: Location = geolocator.reverse(f"{g.latlng[0]},{g.latlng[1]}")
print(location.address)


def display_ip():
    """  Function To Print GeoIP Latitude & Longitude """
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']
    geo_request = requests.get('https://get.geojs.io/v1/ip/geo/' +my_ip + '.json')
    geo_data = geo_request.json()
    # print({'latitude': geo_data['latitude'], 'longitude': geo_data['longitude']})
    lat2 = geo_data['latitude']
    lon2 = geo_data['longitude']
    print(f"{lat2},{lon2}")

    location: Location = geolocator.reverse(f"{lat2},{lon2}")
    print(location.address)


display_ip()