from weather import get_weather
from tourist_attractions import get_lat_lng, get_interesting_places
from event import get_event

def produce_text(city, date, category):
    # find weather, tourist attractions and upcoming events
    (lat, lng) = get_lat_lng(city)
    (weather_description, weather_temperature) = get_weather(lat, lng, date)
    list_attractions = get_interesting_places(lat, lng)
    list_events = get_event(lat, lng, date, category, True)

    spoken_text = '<speak><voice name="Geraint">In {}, the temperature will be {} degrees. You might like to visit {} or {}. Also, an ' \
                  'upcoming event you may be interested in is {}. I\'ll send you an email ' \
                  'with some more detailed information!</voice></speak>'.format(city, weather_temperature, list_attractions[0], list_attractions[1], list_events[0][1])

    email_text = """Here's some more information on your upcoming trip to {} on {}.
                 \n\nThere's going to be {}, with a temperature of {} degrees.
                 \n\nSome points of interest in {} are:
                 \n    {}
                 \n    {}
                 \n    {}
                 \n\nHere's some upcoming events you might enjoy:
                 \n    {}
                 \n    {}
                 \n    {}
                 \n\nIf you want to know more about popular tourist attractions, visit www.tripadvisor.com.
                 \nFor more details about the weather, visit www.bbc.com/weather.
                 \nFor more information on upcoming events, visit www.eventbrite.com.""".format(city, date,
                              weather_description, weather_temperature, city, list_attractions[0],
                              list_attractions[1], list_attractions[2], list_events[0][1], list_events[1][1], list_events[2][1])

    email_html = """<html>
<head></head>
<body>
<h3>Here's some more information on your upcoming trip to {} on {}.</h3>
<p>There's going to be {}, with a temperature of {} degrees.</p>

<p>Some points of interest in {} are:</p>
<ul>
    <li>{}</li>
    <li>{}</li>
    <li>{}</li>
</ul>

<p>Here's some upcoming events you might enjoy:</p>
<ul>
    <li>{}</li>
    <li>{}</li>
    <li>{}</li>
</ul>

<p>If you want to know more about popular tourist attractions, visit <a href='https://www.tripadvisor.co.uk/Search?&q={}'>TripAdvisor</a>.</p>
<p>For more details about the weather, visit <a href='bbc.com/weather'>BBC Weather</a>.</p>
<p>For more information on upcoming events, visit <a href='https://www.eventbrite.com/d/united-kingdom--{}/events/'>Eventbrite</a>.</p>
</body>
</html>
            """.format(city, date, weather_description, weather_temperature, city, list_attractions[0],
                              list_attractions[1], list_attractions[2], list_events[0][1], list_events[1][1],
                       list_events[2][1], city, city)

    print(email_html)

    return spoken_text, email_text, email_html

if __name__ == '__main__':
    # currently hard coded, but would be passed
    # in by Alexa depending on the user's reponse
    city = "Perth"
    date = "2019-04-20"
    category = "Travel & Outdoor"

    # produce email body
    (spoken_text, email_text, email_html) = produce_text(city, date, category)
    # print(email_text)
    # print("\n" + spoken_text)
    #pass
