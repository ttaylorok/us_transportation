import googlemaps
from datetime import datetime
import json
import pandas as pd

gmaps = googlemaps.Client(key='AIzaSyAZu3lFrESMW38bsSHKIkg8aeLkeg9x6pU')

cities = {"Albany" : 104,
          "Atlanta" : 122,
          "Birmingham, AL" : 142,
          "Boston" : 148,
          "Buffalo" : 160,
          "Charlotte" : 172,
          "Chigago" : 176,
          "Cincinnati" : 178,
          "Cleveland" : 184,
          "Columbus" : 198,
          "Corpus Christi" : 204,
          "Dallas" : 206,
          "Dayton" : 212,
          "Denver" : 216,
          "Detroit" : 220,
          "El Paso" : 238,
          "Fort Wayne" : 258,
          "Fresno" : 260,
          "Grand Rapids MI" : 266,
          "Greensboro, NC" : 268,
          "Greenville, SC" : 273,
          "Houston, TX" : 288,
          "Indianapolis, IN" : 294,
          "Jacksonville, FL" : 300,
          "Kansas City" : 312,
          "Knoxville, TN" : 314,
          "Las Vegas" : 332,
          "Los Angeles" : 348,
          "Louisville, KY" : 350,
          "Memphis, TN" : 368,
          "Miami, FL" : 370,
          "Milwaukee, WI" : 376,
          "Minneapolis, MN" : 378,
          "Mobile, AL" : 380,
          "Nashville, TN" : 400,
          "New Orleans" : 406,
          "New York City" : 408,
          "Oklahoma City" : 416,
          "Omaha, NE" : 420,
          "Orlando, FL" : 422,
          "Philadelphia" : 428,
          "Pittsburgh" : 430,
          "Portland" : 440,
          "Raleigh, NC" : 450,
          "Rochester" : 464,
          "Sacramento" : 472,
          "St. Louis, MO" : 476,
          "Salt Lake City" : 482,
          "San Jose, CA" : 488,
          "Savannah, GA" : 496,
          "Seattle" : 500,
          "Tucson, AZ" : 536,
          "Tulsa, OK" : 538,
          "Virgina Beach, VA" : 545,
          "Wichita, KS" : 556,
          "Austin, TX" : 12420,
          "Baltimore, MD" : 12580,
          "Baton Rouge, LA" : 12940,
          "Beaumont, TX" : 13140,
          "Charleston, SC" : 16700,
          "Hartford, CT" : 25540,
          "Lake Charles, LA" : 29340,
          "Laredo, TX" : 29700,
          "Phoenix, AZ" : 38060,
          "Richmond, VA" : 40060,
          "San Antonio, TX" : 41700,
          "San Diego, CA" : 41740,
          "Tampa, FL" : 45300,
          "Honolulu" : 46520,
          "Washington, DC" : 47900   
          }
arr = []
for c in cities.keys():
    out1 = gmaps.find_place(c,
                              fields=["geometry","name"],
                              input_type="textquery")
    arr.append([c,
                cities[c],
                out1["candidates"][0]["geometry"]["location"]["lat"],
                out1["candidates"][0]["geometry"]["location"]["lng"]])
    
df = pd.DataFrame(arr, columns = ["city", "code", "lat", "lng"])
df.to_csv("cities_with_lat_lng.csv")



# out2 = gmaps.places_nearby(location="32.780916,-96.799794",
#                              radius=2000,
#                              keyword="bar")

# out3 = gmaps.places_nearby(location="32.780916,-96.799794",
#                              radius=100000,
#                              type="restaurant")

# w_out1 = open("gmap_bars_100k.txt",'w')
# w_out1.write(json.dumps(out3))
# w_out1.close()
# for x in out3["results"]:
#     print(x["name"],x["geometry"]["location"]["lat"],x["geometry"]["location"]["lng"])

# # Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# # Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# # Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions("Sydney Town Hall",
#                                      "Parramatta, NSW",
#                                      mode="transit",
#                                      departure_time=now)