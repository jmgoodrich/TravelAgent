import streamlit as st
import datetime
import pandas as pd
from pandas import *
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain import hub
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate

from tools.flightsearch import FlightSearch
from tools.attractionsearch import AttractionSearch
from tools.accommodationsearch import AccommodationSearch

flight_csv = pd.read_csv("./database/flights.csv").dropna()[['Flight Number', 'Price', 'DepTime', 'ArrTime', 'ActualElapsedTime','FlightDate','OriginCityName','DestCityName','Distance']]
attractions_csv = pd.read_csv("./database/attractions.csv").drop(columns=['Latitude', 'Longitude', 'Phone', 'Website'])
accommodations_csv = pd.read_csv("./database/accommodations.csv").dropna()[['NAME','price','room type','house_rules', 'minimum nights', 'maximum occupancy', 'city']]
locations = pd.read_csv("./database/locations.csv")


load_dotenv()

llm = ChatAnthropic(model="claude-3-haiku-20240307", max_tokens=10000)

flight_search = FlightSearch()
attraction_search = AttractionSearch()
accommodation_search = AccommodationSearch()

tools = [flight_search, attraction_search, accommodation_search]

parse_prompt = PromptTemplate(
    input_variables=["query"],
    template=(
        """You are a tool calling agent. You should extract the relevant information and return tool calls 
        
        "User's request: {query}"""
    )
)

plan_prompt = PromptTemplate(
    input_variables=["text","query"],
    template=(
        """You are a proficient planner. Based on the provided information and query, please give me a detailed plan, including specifics such as flight numbers (e.g., F0123456) and accommodation names. Note that all the information in your plan should be derived from the provided data. You must adhere to the format given in the example. Additionally, all details should align with commonsense. The symbol '-' indicates that information is unnecessary. For example, in the provided sample, you do not need to plan after returning to the departure city. When you travel to two cities in one day, you should note it in the 'Current City' section as in the example (i.e., from A to B).

    ***** Example *****
    Query: Could you create a travel plan for 7 people from Ithaca to Charlotte spanning 3 days, from March 8th to March 14th, 2022, with a budget of $30,200?
    Travel Plan:
    Day 1:
    Current City: from Ithaca to Charlotte
    Transportation: Flight Number: F3633413, from Ithaca to Charlotte, Departure Time: 05:38, Arrival Time: 07:46
    Attraction: The Charlotte Museum of History, Charlotte
    Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

    Day 2:
    Current City: Charlotte
    Transportation: -
    Attraction: The Mint Museum, Charlotte;Romare Bearden Park, Charlotte.
    Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

    Day 3:
    Current City: from Charlotte to Ithaca
    Transportation: Flight Number: F3786167, from Charlotte to Ithaca, Departure Time: 21:42, Arrival Time: 23:26
    Attraction: Books Monument, Charlotte.
    Accommodation: -

    ***** Example Ends *****

    Given information: {text}
    Query: {query}
    Travel Plan:"""
    )
)





# st.title("Travel Itinerary Planner")
# with st.container():
#     travel_dates = st.date_input("Select your vacation dates",
#                             value=[datetime.date.today(), datetime.date.today() + datetime.timedelta(days=3)],
#                             format="MM/DD/YYYY",)

#     vacation_length = (travel_dates[1] - travel_dates[0]).days

# with st.container():
#     col1, col2 = st.columns(2)
#     with col1:
#         depart = st.selectbox("From",
#                      index=0,
#                      options=locations["City"])
#     with col2:
#         arrive = st.selectbox("To",
#                      index=1,
#                     options=locations["City"])
        
# room_rules = st.pills("Accommodation Rules", ["Smoking Friendly", "Pets Allowed", "Parties Allowed", "Visitors Allowed", "Children Allowed"], selection_mode="multi")
# room_type = st.pills("Accommodation Constraints", ["Entire Room", "Private Room", "Shared Room", "No Shared Room"])
# budget = st.number_input("What is your budget?", min_value=500, step=50)

# if depart != None and arrive != None:
#     prompt_start = "Generate a {}-day travel itinerary from {} to {}, traveling from {} to {} with a budget of ${}.".format(vacation_length, travel_dates[0], travel_dates[1], depart, arrive, budget)

# if room_rules != []:
#     prompt_start += " Accommodation must be {}.".format(", ".join(room_rules))

# if room_type != None:
#     prompt_start += " Accommodation must be {}.".format(room_type)

# messages = st.container(height=400)    
# if st.button("Generate"):
#     messages.chat_message("user").write(prompt_start);
#     prompt = prompt_start + """ Example Output:
#     Travel Itinerary:
#     Day 1: 
#     - Location: from New York to Los Angeles
#     - Transportation: Flight
#     - Activities: Visit the Getty Museum
#     - Accommodations: Beverly Hills Hotel
#     Day 2:
#     - Location: Los Angeles
#     - Transportation: Uber
#     - Activities: Visit the Griffith Observatory
#     - Accommodations: Beverly Hills Hotel

#     Only output the itinerary
# """
#     m = [HumanMessage(content=prompt)]
#     # messages.chat_message("assistant").write(llm.invoke(m).content)