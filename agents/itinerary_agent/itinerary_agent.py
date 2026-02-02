"""
Itinerary Agent - Creates detailed day-by-day Umrah schedules
"""

from strands_agents import Agent, Task, Crew
from typing import Dict, List, Any
import os


class ItineraryAgent:
    """Specialized agent for creating Umrah itineraries"""
    
    def __init__(self):
        self.model = os.getenv("ITINERARY_AGENT_MODEL", "anthropic.claude-sonnet-4-5-20250929-v1:0")
        
        self.agent = Agent(
            role="Umrah Itinerary Specialist",
            goal="Create detailed, spiritually enriching itineraries for Umrah pilgrims",
            backstory="""You are an expert in Islamic pilgrimage rituals and logistics.
            You have deep knowledge of Umrah procedures, the significance of various sites,
            optimal timing for rituals, and practical considerations for pilgrims. You create
            itineraries that balance spiritual fulfillment with physical comfort and safety.""",
            model=self.model,
            verbose=True
        )
    
    def create_itinerary(self, trip_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create comprehensive day-by-day itinerary
        
        Args:
            trip_details: Dict containing:
                - departure_date: str
                - return_date: str
                - arrival_city: str
                - num_travelers: int
                - first_time_umrah: bool
                - elderly_travelers: bool
                - special_requirements: List[str]
        
        Returns:
            Detailed itinerary with daily activities
        """
        
        task = Task(
            description=f"""
            Create a detailed Umrah itinerary based on these details:
            {trip_details}
            
            The itinerary should include:
            
            DAY 1 - ARRIVAL:
            - Airport arrival and immigration
            - Transfer to hotel
            - Entering Ihram state
            - Performing first Umrah (Tawaf and Sa'i)
            - Important duas and etiquette
            
            MAKKAH DAYS:
            - Daily prayer schedules at Masjid al-Haram
            - Ziyarat (visiting historical sites):
              * Jabal al-Nour (Cave of Hira)
              * Jabal Thawr
              * Jannat al-Mu'alla cemetery
              * Museum of the Two Holy Mosques
            - Optional additional Umrah
            - Rest periods
            
            TRANSFER TO MADINAH:
            - Best time to travel
            - Journey duration and stops
            
            MADINAH DAYS:
            - Prayers at Masjid an-Nabawi
            - Visiting Rawdah (the blessed garden)
            - Ziyarat in Madinah:
              * Quba Mosque
              * Masjid Qiblatain
              * Uhud Mountain and martyrs cemetery
              * Date farms
            - Islamic history lessons
            
            DEPARTURE:
            - Final prayers
            - Shopping for gifts (dates, zamzam, etc.)
            - Airport transfer
            
            For each day, provide:
            - Specific timings
            - Activity descriptions
            - Spiritual significance
            - Practical tips
            - Duas to recite
            - Rest periods
            
            Adjust for elderly or first-time pilgrims if specified.
            
            Return as structured JSON with daily breakdown.
            """,
            agent=self.agent,
            expected_output="Comprehensive day-by-day itinerary in JSON format"
        )
        
        crew = Crew(agents=[self.agent], tasks=[task])
        result = crew.kickoff()
        
        return result
    
    def provide_ritual_guidance(self, ritual_type: str) -> Dict[str, Any]:
        """Provide detailed guidance for specific Umrah rituals"""
        
        task = Task(
            description=f"""
            Provide detailed guidance for: {ritual_type}
            
            Include:
            1. Step-by-step procedure
            2. Required duas and their meanings
            3. Common mistakes to avoid
            4. Spiritual significance
            5. Practical tips
            6. Etiquette and manners
            
            Make it easy to understand for first-time pilgrims.
            """,
            agent=self.agent,
            expected_output="Detailed ritual guidance"
        )
        
        crew = Crew(agents=[self.agent], tasks=[task])
        result = crew.kickoff()
        
        return result
    
    def suggest_optimal_times(self, activities: List[str]) -> Dict[str, Any]:
        """Suggest optimal times for various activities"""
        
        task = Task(
            description=f"""
            Suggest optimal times for these activities:
            {activities}
            
            Consider:
            1. Crowd levels at different times
            2. Weather conditions
            3. Prayer times
            4. Physical energy levels
            5. Spiritual atmosphere
            
            Provide recommendations with reasoning.
            """,
            agent=self.agent,
            expected_output="Optimal timing recommendations"
        )
        
        crew = Crew(agents=[self.agent], tasks=[task])
        result = crew.kickoff()
        
        return result


def create_itinerary_agent():
    """Factory function to create itinerary agent"""
    return ItineraryAgent()
