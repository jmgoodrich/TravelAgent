
import streamlit as st
import datetime




st.title("Travel Agent")
travel_dates = st.date_input("Select your vacation dates",
                            value=[datetime.date.today(), datetime.date.today() + datetime.timedelta(days=3)],
                            format="MM/DD/YYYY",)
travel_dates