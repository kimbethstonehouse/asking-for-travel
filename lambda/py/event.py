import requests
import json

eventbrite_api_key = "************"

eventCategoryResolution = {
    "nerdy things": "Technology",
    "nerd stuff": "Technology",
    "mathematics": "Technology",
    "data science": "Technology",
    "data": "Technology",
    "hackathons": "Technology",
    "mechanics": "Technology",
    "engineering": "Technology",
    "comp ski": "Technology",
    "computer science": "Technology",
    "programming": "Technology",
    "coding": "Technology",
    "computers": "Technology",
    "chemistry": "Technology",
    "maths": "Technology",
    "biology": "Technology",
    "physics": "Technology",
    "science": "Technology",
    "tech": "Technology",
    "Technology": "Technology",
    "brexit": "Business",
    "politics": "Business",
    "government": "Business",
    "coaching": "Business",
    "employment": "Business",
    "networking": "Business",
    "career": "Business",
    "conference": "Business",
    "work": "Business",
    "business": "Business",
    "Business": "Business",
    "food and drink": "Food",
    "scran": "Food",
    "cocktails": "Food",
    "drinking": "Food",
    "bar": "Food",
    "restaurants": "Food",
    "alcohol": "Food",
    "eat": "Food",
    "eating out": "Food",
    "drink": "Food",
    "food": "Food",
    "Food": "Food",
    "charity": "Family",
    "community": "Family",
    "school holiday": "Family",
    "school": "Family",
    "reading": "Family",
    "learning experience ": "Family",
    "learning": "Family",
    "children's activities ": "Family",
    "school activities ": "Family",
    "family": "Family",
    "education": "Family",
    "Family": "Family",
    "explore": "Sport",
    "flying": "Sport",
    "plane": "Sport",
    "boat": "Sport",
    "sports": "Sport",
    "fitness": "Sport",
    "health": "Sport",
    "cycling": "Sport",
    "biking": "Sport",
    "walking": "Sport",
    "sailing": "Sport",
    "walk": "Sport",
    "mountain": "Sport",
    "beach": "Sport",
    "in the open ": "Sport",
    "woods": "Sport",
    "picnic": "Sport",
    "trip": "Sport",
    "tour": "Sport",
    "nature": "Sport",
    "expedition": "Sport",
    "outside": "Sport",
    "sightseeing": "Sport",
    "excursion": "Sport",
    "outdoor": "Sport",
    "travel": "Sport",
    "football": "Sport",
    "rugby": "Sport",
    "golf": "Sport",
    "basketball": "Sport",
    "swimming": "Sport",
    "Sport": "Sport",
    "media": "Arts",
    "heritage": "Arts",
    "historical": "Arts",
    "history": "Arts",
    "sculpture": "Arts",
    "painting": "Arts",
    "writing": "Arts",
    "drama": "Arts",
    "concert": "Arts",
    "live music ": "Arts",
    "jazz": "Arts",
    "opera": "Arts",
    "cinema": "Arts",
    "movie": "Arts",
    "arts and craft ": "Arts",
    "museum": "Arts",
    "art museum ": "Arts",
    "art gallery ": "Arts",
    "gallery": "Arts",
    "fashion": "Arts",
    "media": "Arts",
    "film": "Arts",
    "arts": "Arts",
    "art": "Arts",
    "music": "Arts",
    "Arts": "Arts"
}

event_type = { "Sport": [107, 108, 109, 118], "Food": [110], "Business": [101, 113, 112], "Technology": [102], "Arts": [105, 104, 103, 106], "Family": [115, 120, 113, 111]}

def get_event(lat, lng, start_date, type, adult) :
    end_date = start_date + "T23:59:59"
    start_date = start_date + "T00:00:00"

    url = "https://www.eventbriteapi.com/v3/events/search/?sort_by=date&location.within=10km&location.latitude={}&location.longitude={}&start_date.range_start={}&start_date.range_end={}&categories=".format(lat, lng, start_date, end_date)

    for category_id in event_type[eventCategoryResolution[type]]:
        url += "{}%2C".format(category_id)
    url = url[:-3]

    if adult:
        url += "&include_adult_events=on"
    else:
        url += "&include_adult_events=off"

    url += "&token={}".format(eventbrite_api_key)

    r = requests.get(url)
    result = json.loads(r.content)

    event_list = []

    if len(result["events"]) == 0:
        event_list.append((0, "no event"))
        event_list.append((1, "no event"))
        event_list.append((2, "no event"))

    else:
        for event in result["events"]:
            event_list.append((event["id"], event['name']['text']))

    return event_list

if __name__ == '__main__':
    print(get_event(55.468405, -4.629838, "2019-04-20T09:10:02", "2019-04-22T00:00:00", "Travel & Outdoor", True))

