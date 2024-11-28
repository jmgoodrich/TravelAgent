import streamlit as st
import datetime
import pandas as pd
from pandas import *
import os
from dotenv import load_dotenv
import json
import csv

from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate

from tools.flightsearch import FlightSearch
from tools.attractionsearch import AttractionSearch
from tools.accommodationsearch import AccommodationSearch

from parse import TravelPlanParser

flight_csv = pd.read_csv("./database/flights.csv").dropna()[['Flight Number', 'Price', 'DepTime', 'ArrTime','FlightDate','OriginCityName','DestCityName']]
attractions_csv = pd.read_csv("./database/attractions.csv").drop(columns=['Latitude', 'Longitude', 'Phone', 'Website', 'Address'])
accommodations_csv = pd.read_csv("./database/accommodations.csv").dropna()[['NAME','price','room type','house_rules', 'minimum nights', 'maximum occupancy', 'city']]
locations = pd.read_csv("./database/locations.csv")

load_dotenv()

llm = ChatAnthropic(model="claude-3-haiku-20240307", max_tokens=4096)

flight_search = FlightSearch()
attraction_search = AttractionSearch()
accommodation_search = AccommodationSearch()

tools = [flight_search, attraction_search, accommodation_search]

parser = TravelPlanParser()
# parsed_output = parser.parse(output_text)
# print(json.dumps(parsed_output, indent=4))

plan_prompt = PromptTemplate(
    input_variables=["query","flight_out", "flight_return", "attractions", "accommodations"],
    template=(
        """You are a proficient planner. Based on the provided information and query, please give me a detailed plan, including specifics such as flight numbers (e.g., F0123456) and accommodation names. Note that all the information in your plan should be derived from the provided data. You must adhere to the format given in the example. Additionally, all details should align with commonsense. The symbol '-' indicates that information is unnecessary. For example, in the provided sample, you do not need to plan after returning to the departure city. 
    Only output the itinerary.
        
    ***** Example *****
    Query: Could you create a travel plan for 7 people from Ithaca to Charlotte spanning 3 days, from March 8th to March 14th, 2022, with a budget of $30,200?
    Travel Plan:\n
    Day 1:\n
    Current City: from Ithaca to Charlotte\n
    Transportation: Flight Number: F3633413, from Ithaca to Charlotte, Departure Time: 05:38, Arrival Time: 07:46\n
    Attraction: The Charlotte Museum of History, Charlotte\n
    Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte\n

    Day 2:\n
    Current City: Charlotte\n
    Transportation: -\n
    Attraction: The Mint Museum, Charlotte;Romare Bearden Park, Charlotte.\n
    Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte\n

    Day 3:
    Current City: from Charlotte to Ithaca\n
    Transportation: Flight Number: F3786167, from Charlotte to Ithaca, Departure Time: 21:42, Arrival Time: 23:26\n
    Attraction: Books Monument, Charlotte.\n
    Accommodation: -\n

    Total Cost: $29,000
    ***** Example Ends *****

    Given information: {flight_out}, {flight_return}, {attractions}, {accommodations}
    Query: {query}
    """
    )
)

st.title("Travel Itinerary Planner")
with st.container():
    travel_dates = st.date_input("Select your vacation dates",
                            value=[datetime.date.today(), datetime.date.today() + datetime.timedelta(days=3)],
                            format="MM/DD/YYYY",)

    vacation_length = (travel_dates[1] - travel_dates[0]).days + 1
start = travel_dates[0].strftime("%Y-%m-%d")
end = travel_dates[1].strftime("%Y-%m-%d")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        depart = st.selectbox("From",
                     index=0,
                     options=locations["City"])
    with col2:
        arrive = st.selectbox("To",
                     index=1,
                    options=locations["City"])
        
travelers = st.number_input("How many people are traveling?", min_value=1, step=1)
room_rules = st.pills("Accommodation Allows:", ["Smoking", "Pets", "Parties", "Visitors", "Children"], selection_mode="multi")
room_type = st.pills("Accommodation Constraints", ["Entire Room", "Private Room", "Shared Room"])
budget = st.number_input("What is your budget?", min_value=500, step=50)

if depart != None and arrive != None:
    if travelers > 1:
        query = "Generate a {}-day travel itinerary from {} to {}, for {} people, traveling from {} to {} with a budget of ${}.".format(vacation_length, travel_dates[0], travel_dates[1], travelers, depart, arrive, budget)
    else:
        query = "Generate a {}-day travel itinerary from {} to {}, for 1 person, traveling from {} to {} with a budget of ${}.".format(vacation_length, travel_dates[0], travel_dates[1], depart, arrive, budget)

if room_rules != []:
    query += " Accommodation must allow {}.".format(", ".join(room_rules).lower())

if room_type != None:
    query += " The room should be a(n) {}.".format(room_type.lower())

messages = st.container(height=400) 
if st.button("Generate"):
    messages.chat_message("user").write(query);
    result_flights_depart = flight_search.run({
        "data": flight_csv,
        "origin": depart,
        "dest": arrive,
        "date": start
    })

    result_flights_return = flight_search.run({
        "data": flight_csv,
        "origin": depart,
        "dest": arrive,
        "date": end
    })

    result_attr = attraction_search.run({
        "data": attractions_csv,
        "city": arrive
    })

    result_accom = accommodation_search.run({
        "data": accommodations_csv,
        "city": arrive
    }) 
    chain = plan_prompt | llm
    output = chain.invoke({"query": query, "flight_out" : result_flights_depart, "flight_return" : result_flights_return, "attractions" : result_attr, "accommodations" : result_accom})

    messages.chat_message("assistant").write(output.content)

