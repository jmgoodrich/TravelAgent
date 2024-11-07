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

llm = ChatAnthropic(model="claude-3-haiku-20240307", max_tokens=100)

# amadeus_client = Client(
#     client_id=os.getenv("AMADEUS_CLIENT_ID"),
#     client_secret=os.getenv("AMADEUS_CLIENT_SECRET"),
# )

# toolkit = AmadeusToolkit(client=amadeus_client, llm=llm)
# tools = toolkit.get_tools()

# prompt = hub.pull("hwchase17/react")
# agent = create_react_agent(llm=llm, prompt=prompt)

# agent_executor = AgentExecutor(agent=agent, handle_parsing_errors=True)


airports_csv = read_csv("./airports.csv")
airports = {
    "airport": airports_csv["AIRPORT"].tolist(),
    "city": airports_csv["CITY"].tolist(),
    "state": airports_csv["STATE"].tolist(),
    "code": airports_csv["IATA"].tolist(),
}

st.title("Travel Agent")
with st.container():

    if st.checkbox("One-Way"):
        travel_dates = st.date_input("Select your vacation dates",
                                value=datetime.date.today(),
                                format="MM/DD/YYYY",)
    else:
        travel_dates = st.date_input("Select your vacation dates",
                                value=[datetime.date.today(), datetime.date.today() + datetime.timedelta(days=3)],
                                format="MM/DD/YYYY",)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        depart = st.selectbox("From",
                     index=None,
                     options=airports["airport"])
        if depart != None:
            depart_city = airports["city"][airports["airport"].index(depart)]
            depart_state = airports["state"][airports["airport"].index(depart)]
            depart_city, depart_state
    with col2:
        arrive = st.selectbox("To",
                     index=None,
                    options=airports["airport"])
        if arrive != None:
            arrive_city = airports["city"][airports["airport"].index(arrive)]
            arrive_state = airports["state"][airports["airport"].index(arrive)]
            arrive_city, arrive_state
        

with st.container():
    art = st.checkbox("Art")
    museums = st.checkbox("Museums")
    outdoor = st.checkbox("Outdoor Activities")
    shopping = st.checkbox("Shopping")
    sightseeing = st.checkbox("Sightseeing")
    nightlife = st.checkbox("Nightlife")
    food = st.checkbox("Food")

with st.sidebar:
    st.sidebar.title("Have a question?")
    messages = st.container(height=300)
    if question := st.chat_input("Ask me anything about flights, hotels, or activities"):
        messages.chat_message("user").write(question);
        m = [HumanMessage(content=question)]
        messages.chat_message("assistant").write(llm.invoke(m).content)