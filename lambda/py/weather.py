import requests

from tourist_attractions import get_lat_lng

weather_api_key = "******************"

def get_weather(lat, lng, date):
    url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}".format(lat, lng, weather_api_key)

    response = requests.get(url).json()
    all_results = response["list"]

    weather_for_date = list(filter(lambda x: date in x['dt_txt'] and '12:00:00' in x['dt_txt'], all_results))[0]

    description = weather_for_date['weather'][0]['description']
    temperature = weather_for_date['main']['temp']

    temperature = float(temperature) - 273.15
    temperature = round(temperature)

    return description, temperature


if __name__ == '__main__':
    (lat, lng) = get_lat_lng("Manchester")
    get_weather(lat, lng, '2019-04-20')
