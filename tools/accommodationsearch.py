from pandas import DataFrame
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class AccommodationInput(BaseModel):
    data: DataFrame = Field(..., description="The accommodation data to search")
    city: str = Field(..., description="The city of the accommodation")

    class Config:
        arbitrary_types_allowed = True

class AccommodationSearch(BaseTool):
    name: str = "Accommodation Search"
    description: str = "Search for attractions for a given city"
    args_schema: Type[BaseModel] = AccommodationInput

    def _run(self, data: DataFrame, city: str) -> DataFrame:
        results = data[data['city'] == city]

        if results.empty:
            return "No accommodations found"

        return results 