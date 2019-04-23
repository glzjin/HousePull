import requests


def transform(location):
    parameters = {'coordsys': 'gps', 'address': location, 'city': '北京', 'key': '241cd198d49f31ce745e31b96d7e8285'}
    base = 'https://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    return answer['geocodes'][0]['location'].split(',')
