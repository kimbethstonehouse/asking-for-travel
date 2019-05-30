# Asking for Travel

## What it is

Asking for Travel is an Alexa skill that was created as part of a three day hackathon at Amazon's Development Centre Scotland in April 2019. The idea is that the user is going on holiday, and wants to find out more about their destination. The user tells Alexa where they are going and when, mentioning a specific interest of theirs (such as music, or football, or history). The skill returns information about the weather during the trip, the top tourist attractions in the city, and upcoming events related to their interest. A snippet of this information is spoken, and then the user is sent an email with more detailed information for them to review later. 

## Technologies

We used five APIs: Eventbrite for the upcoming local events, Google Places for the top attractions, Google Geocoding to convert a city name to a latitude and longitude, Open Weather Map for the weather and Amazon's SES to send the emails.
