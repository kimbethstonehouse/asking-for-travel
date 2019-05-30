import requests
import json

google_api_key = "*****************"

def get_lat_lng(city):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(city, google_api_key)

    result = requests.get(url).json()
    lat = result['results'][0]['geometry']['location']['lat']
    lng = result['results'][0]['geometry']['location']['lng']

    return lat, lng

def get_interesting_places(lat, lng):
    filtered_results = []

    # request results for park
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}," \
          "{}&radius=5000&type=park&key={}".format(lat,lng,google_api_key)
    r = requests.get(url)
    response = json.loads(r.content)
    if response['results']:
        filtered_results.append(response['results'][0]['name'])
    else:
        filtered_results.append("no attraction")

    # request results for museum
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}," \
          "{}&radius=5000&type=museum&key={}".format(lat, lng, google_api_key)
    r = requests.get(url)
    response = json.loads(r.content)
    if response['results']:
        filtered_results.append(response['results'][0]['name'])
    else:
        filtered_results.append("no attraction")

    # request results for stadium
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}," \
          "{}&radius=5000&type=stadium&key={}".format(lat, lng, google_api_key)
    r = requests.get(url)
    response = json.loads(r.content)
    if response['results']:
        filtered_results.append(response['results'][0]['name'])
    else:
        filtered_results.append("no attraction")

    return filtered_results

if __name__ == '__main__':
    (lat, lng) = get_lat_lng("Edinburgh")
    places = get_interesting_places(lat, lng)
