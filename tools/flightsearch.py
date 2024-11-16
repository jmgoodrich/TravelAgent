import pandas as pd
from pandas import DataFrame
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type

class FlightInput(BaseModel):
    data: DataFrame = Field(..., description="The flight data to search")
    origin: str = Field(..., description="The origin city of the flight")
    dest: str = Field(..., description="The destination city of the flight")
    date: str = Field(..., description="The date of the flight")

    class Config:
        arbitrary_types_allowed = True

class FlightSearch(BaseTool):
    name: str = "Flight Search"
    description: str = "Search for flights based on origin, destination, and date"
    args_schema: Type[BaseModel] = FlightInput

    def _run(self, data: DataFrame, origin: str, dest: str, date: str) -> DataFrame:
        results = data[(data['OriginCityName'] == origin) & (data['DestCityName'] == dest) & (data['FlightDate'] == date)]
        
        if results.empty:
            return "No flights found"

        return results 
    