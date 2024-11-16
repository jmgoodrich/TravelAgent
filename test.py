from tools.flightsearch import FlightSearch
import pandas as pd

flight_csv = pd.read_csv("./database/flights.csv").dropna()[['Flight Number', 'Price', 'DepTime', 'ArrTime', 'ActualElapsedTime','FlightDate','OriginCityName','DestCityName','Distance']]

flight_tool = FlightSearch()


result = flight_tool.run({
    "data": flight_csv,
    "origin": "Sarasota",
    "dest": "Chicago",
    "date": "2022-03-22"
})

print(result)