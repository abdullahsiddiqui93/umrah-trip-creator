"""
Hotel Agent - Searches and books hotels in Makkah and Madinah
"""

from strands_agents import Agent, Task, Crew
from typing import Dict, List, Any
import os


class HotelAgent:
    """Specialized agent for hotel search and booking"""
    
    def __init__(self):
        self.model = os.getenv("HOTEL_AGENT_MODEL", "anthropic.claude-sonnet-4-5-20250929-v1:0")
        
        self.agent = Agent(
            role="Hotel Booking Specialist",
            goal="Find the best hotel accommodations near the Holy Mosques for Umrah pilgrims",
            backstory="""You are an expert in hotel bookings for Umrah and Hajj pilgrims.
            You have deep knowledge of hotels in Makkah and Madinah, understanding the 
            importance of proximity to the Haram, quality of service, and amenities that 
            matter to pilgrims. You prioritize hotels with good reviews from Muslim travelers.""",
            model=self.model,
            verbose=True
        )
    
    def search_hotels(self, city: str, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search for hotels in Makkah or Madinah
        
        Args:
            city: "Makkah" or "Madinah"
            requirements: Dict containing:
                - check_in: str
                - check_out: str
                - num_rooms: int
                - num_guests: int
                - proximity: str (walking distance, close, moderate, far)
                - star_rating: int
                - budget_per_night: float
                - amenities: List[str]
                - haram_view: bool
        
        Returns:
            List of hotel options with pricing and details
        """
        
        task = Task(
            description=f"""
            Search for hotels in {city} with these requirements:
            {requirements}
            
            Find at least 3 hotel options that:
            1. Match the proximity preference to the Haram
            2. Meet the star rating requirement
            3. Fit within the budget
            4. Have the requested amenities
            5. Have good reviews from Muslim travelers
            
            For each option, provide:
            - Hotel name and star rating
            - Distance from Haram (in meters)
            - Price per night and total cost
            - Available amenities
            - Guest rating and reviews
            - Room type and capacity
            - Special features (Haram view, prayer facilities, etc.)
            
            Return as structured JSON array.
            """,
            agent=self.agent,
            expected_output="JSON array of hotel options with complete details"
        )
        
        crew = Crew(agents=[self.agent], tasks=[task])
        result = crew.kickoff()
        
        return result
    
    def recommend_hotels(self, makkah_hotels: List[Dict], madinah_hotels: List[Dict]) -> Dict[str, Any]:
        """Provide hotel recommendations for both cities"""
        
        task = Task(
            description=f"""
            Analyze these hotel options and provide recommendations:
            
            Makkah Hotels: {makkah_hotels}
            Madinah Hotels: {madinah_hotels}
            
            Consider:
            1. Best value for money
            2. Proximity to Haram
            3. Quality and cleanliness
            4. Amenities for pilgrims
            5. Overall guest satisfaction
            
            Provide recommendations for both cities with reasoning.
            """,
            agent=self.agent,
            expected_output="Hotel recommendations with detailed reasoning"
        )
        
        crew = Crew(agents=[self.agent], tasks=[task])
        result = crew.kickoff()
        
        return result


def create_hotel_agent():
    """Factory function to create hotel agent"""
    return HotelAgent()
