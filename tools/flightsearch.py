import pandas as pd
from langchain_core.tools.base_tool import BaseTool

class FlightSearch(BaseTool):
    name = "FlightSearch"
    description = "Search for flights"

    def __init__(self):
        self.csv_path = "../database/clean_Flights_2022.csv"
