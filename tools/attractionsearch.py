import pandas as pd
from pandas import DataFrame
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type

class AttractionInput(BaseModel):
    data: DataFrame = Field(..., description="The attraction data to search")
    city: str = Field(..., description="The city of the attraction")

    class Config:
        arbitrary_types_allowed = True

class AttractionSearch(BaseTool):
    name: str = "Attraction Search"
    description: str = "Search for attractions for a given city"
    args_schema: Type[BaseModel] = AttractionInput

    def _run(self, data: DataFrame, city: str) -> DataFrame:
        results = data[data['City'] == city]

        if results.empty:
            return "No attractions found in this city"

        return results 