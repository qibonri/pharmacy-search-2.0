import sys
import math
from io import BytesIO
import requests
from PIL import Image
import map_delta_func
import map_search


def distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)

    return distance


toponym_to_find = " ".join(sys.argv[1:])
toponym = map_delta_func.address_to_geocode(toponym_to_find)
lat, lon = map_delta_func.get_coordinates(toponym_to_find)
coord = f'{lat},{lon}'
span = '0.005,0.005'
org = map_search.find_bisiness(coord, span, 'аптека')
org_lat, org_lon = org['geometry']['coordinates']
distance = distance([lat, lon], [org_lat, org_lon])
snippet = {'address': org['properties']['CompanyMetaData']['address'],
           'name': org['properties']['CompanyMetaData']['name'],
           'hours': org['properties']['CompanyMetaData']['Hours']['text']}
for key, val in snippet.items():
    print(f'{key}: {val}')
print(f'{int(distance)} метров')

map_params = {
    "ll": ",".join([str(lat), str(lon)]),
    "pt": ",".join([str(lat), str(lon), 'org']) + '~' + ",".join([str(org_lat), str(org_lon), 'org']),
    "l": "map"
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()
