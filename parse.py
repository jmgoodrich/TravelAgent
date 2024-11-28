from langchain.schema import BaseOutputParser
import re
import json

class TravelPlanParser(BaseOutputParser):
    def parse(self, text: str) -> dict:
        # Initialize results
        parsed_result = {"plan": [], "total_cost": ""}
        
        # Match each day's details
        day_pattern = r"Day (\d+):\nCurrent City: (.+?)\nTransportation: (.+?)\nAttraction: (.+?)\nAccommodation: (.+?)\n"
        day_matches = re.findall(day_pattern, text, re.DOTALL)
        
        # Process matched days
        for match in day_matches:
            day_number, current_city, transportation, attraction, accommodation = match
            parsed_result["plan"].append({
                "day": int(day_number),
                "current_city": current_city.strip(),
                "transportation": transportation.strip(),
                "attraction": attraction.strip(),
                "accommodation": accommodation.strip(),
            })
        
        # Extract total cost
        cost_pattern = r"Total Cost: \$(\d{1,3}(?:,\d{3})*)"
        cost_match = re.search(cost_pattern, text)
        if cost_match:
            parsed_result["total_cost"] = cost_match.group(0).split(": ")[1]

        
        return parsed_result


# Test
# output_text = """
# Day 1:
# Current City: from Ithaca to Charlotte
# Transportation: Flight Number: F3633413, from Ithaca to Charlotte, Departure Time: 05:38, Arrival Time: 07:46
# Attraction: The Charlotte Museum of History, Charlotte
# Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

# Day 2:
# Current City: Charlotte
# Transportation: -
# Attraction: The Mint Museum, Charlotte;Romare Bearden Park, Charlotte.
# Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

# Day 3:
# Current City: from Charlotte to Ithaca
# Transportation: Flight Number: F3786167, from Charlotte to Ithaca, Departure Time: 21:42, Arrival Time: 23:26
# Attraction: Books Monument, Charlotte.
# Accommodation: -

# Total Cost: $29,000
# """

# parser = TravelPlanParser()
# parsed_output = parser.parse(output_text)
# print(json.dumps(parsed_output, indent=4))
