"""
Flight Agent - Searches and books flights for Umrah trips
"""

from strands_agents import Agent, Task, Crew
from typing import Dict, List, Any
import os


class FlightAgent:
    """Specialized agent for flight search and booking"""
    
    def __init__(self):
        self.model = os.getenv("FLIGHT_AGENT_MODEL", "gpt-4o-2024-08-06")
        
        self.agent = Agent(
            role="Flight Search Specialist",
            goal="Find the best flight options for Umrah travelers based on their preferences and budget",
            backstory="""You are an expert flight booking agent with extensive knowledge of 
            routes to Saudi Arabia. You specialize in finding the best deals for religious 
            pilgrimage travel, understanding the importance of convenient timings, direct 
            flights when possible, and generous baggage allowances for Umrah travelers.""",
            model=self.model,
            verbose=True
        )
    
    def search_flights(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search for flight options based on requirements
        
        Args:
            requirements: Dict containing:
                - departure_date: str
                - return_date: str
                - origin: str
                - destination: str (Jeddah or Madinah)
                - num_travelers: int
                - cabin_class: str
                - budget_per_person: float
                - direct_flights_only: bool
        
        Returns:
            List of flight options with pricing and details
        """
        
        task = Task(
            description=f"""
            Search for flights with the following requirements:
            {requirements}
            
            Find at least 3 flight options that:
            1. Match the travel dates and destinations
            2. Fit within the budget
            3. Prioritize direct flights if requested
            4. Include generous baggage allowances
            5. Consider reputable airlines (Saudi, Emirates, Qatar, Turkish, etc.)
            
            For each option, provide:
            - Airline and flight numbers
            - Departure and arrival times
            - Duration and number of stops
            - Price per person and total
            - Baggage allowance
            - Cabin class and amenities
            
            Return as structured JSON array.
            """,
            agent=self.agent,
            expected_output="JSON array of flight options with complete details"
        )
        
        crew = Crew(agents=[self.agent], tasks=[task])
        result = crew.kickoff()
        
        return result
    
    def compare_flights(self, flight_options: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare flight options and provide recommendations"""
        
        task = Task(
            description=f"""
            Compare these flight options and provide recommendations:
            {flight_options}
            
            Analyze based on:
            1. Best value for money
            2. Most convenient timings
            3. Shortest travel time
            4. Best airline reputation
            5. Baggage allowance
            
            Provide a recommendation with reasoning.
            """,
            agent=self.agent,
            expected_output="Comparison analysis with recommendation"
        )
        
        crew = Crew(agents=[self.agent], tasks=[task])
        result = crew.kickoff()
        
        return result


def create_flight_agent():
    """Factory function to create flight agent"""
    return FlightAgent()
