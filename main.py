import streamlit as st
import datetime
from pandas import *
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain import hub
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.agent_toolkits.amadeus.toolkit import AmadeusToolkit
from amadeus import Client

load_dotenv()

llm = ChatAnthropic(model="claude-3-haiku-20240307", max_tokens=500)

# airports_csv = read_csv("./airports.csv")
# airports = {
#     "airport": airports_csv["AIRPORT"].tolist(),
#     "city": airports_csv["CITY"].tolist(),
#     "state": airports_csv["STATE"].tolist(),
#     "code": airports_csv["IATA"].tolist(),
# }

st.title("Travel Itinerary Planner")
with st.container():

    # if st.checkbox("One-Way"):
    #     travel_dates = st.date_input("Select your vacation dates",
    #                             value=datetime.date.today(),
    #                             format="MM/DD/YYYY",)
    # else:
    travel_dates = st.date_input("Select your vacation dates",
                            value=[datetime.date.today(), datetime.date.today() + datetime.timedelta(days=3)],
                            format="MM/DD/YYYY",)

    vacation_length = (travel_dates[1] - travel_dates[0]).days

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        depart = st.selectbox("From",
                     index=None,
                     options=airports["city"])
        # if depart != None:
        #     depart_city = airports["city"][airports["airport"].index(depart)]
        #     depart_state = airports["state"][airports["airport"].index(depart)]
        #     depart_city, depart_state
    with col2:
        arrive = st.selectbox("To",
                     index=None,
                    options=airports["city"])
        # if arrive != None:
        #     arrive_city = airports["city"][airports["airport"].index(arrive)]
        #     arrive_state = airports["state"][airports["airport"].index(arrive)]
        #     arrive_city, arrive_state
        

activities = st.pills("Activities", ["Art", "Museums", "Outdoors", "Shopping", "Sightseeing"], selection_mode="multi")
budget = st.number_input("What is your budget?", min_value=500, step=50)

if depart != None and arrive != None and activities != None:
    prompt_start = "Generate a {}-day travel itinerary from {} to {}, traveling from {} to {} with a budget of ${}.".format(vacation_length, travel_dates[0], travel_dates[1], depart, arrive, budget)
    prompt_start += " The activities I am interested in are: {}.".format(", ".join(activities))

messages = st.container(height=400)    
if st.button("Generate"):
    messages.chat_message("user").write(prompt_start);
    prompt = prompt_start + """ Example Output:
    Travel Itinerary:
    Day 1: 
    - Location: from New York to Los Angeles
    - Transportation: Flight
    - Activities: Visit the Getty Museum
    - Accommodations: Beverly Hills Hotel
    Day 2:
    - Location: Los Angeles
    - Transportation: Uber
    - Activities: Visit the Griffith Observatory
    - Accommodations: Beverly Hills Hotel

    Only output the itinerary
"""
    m = [HumanMessage(content=prompt)]
    messages.chat_message("assistant").write(llm.invoke(m).content)