from tools.flightsearch import FlightSearch
from tools.attractionsearch import AttractionSearch
from tools.accommodationsearch import AccommodationSearch
import pandas as pd

flight_csv = pd.read_csv("./database/flights.csv").dropna()[['Flight Number', 'Price', 'DepTime', 'ArrTime','FlightDate','OriginCityName','DestCityName']]
attractions_csv = pd.read_csv("./database/attractions.csv").drop(columns=['Latitude', 'Longitude', 'Phone', 'Website', 'Address'])
accommodations_csv = pd.read_csv("./database/accommodations.csv").dropna()[['NAME','price','room type','house_rules', 'minimum nights', 'maximum occupancy', 'city']]

flight_tool = FlightSearch()
result_flights = flight_tool.run({
    "data": flight_csv,
    "origin": "Sarasota",
    "dest": "Chicago",
    "date": "2022-03-22"
})

attractions_tool = AttractionSearch()
result_attr = attractions_tool.run({
    "data": attractions_csv,
    "city": "Chicago"
})

accommodations_tool = AccommodationSearch()
result_accom = accommodations_tool.run({
    "data": accommodations_csv,
    "city": "Chicago"
})

print(result_flights)
print(result_attr)
print(result_accom)

