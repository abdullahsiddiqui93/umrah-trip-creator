"""
Main Orchestrator Agent for Umrah Trip Creator
Coordinates all specialized agents and manages user interaction
"""

from strands_agents import Agent, Task, Crew
from typing import Dict, List, Any
import os


class UmrahOrchestratorAgent:
    """Main orchestrator that coordinates all specialized agents"""
    
    def __init__(self):
        self.model = os.getenv("ORCHESTRATOR_MODEL", "anthropic.claude-sonnet-4-5-20250929-v1:0")
        
        # Define the orchestrator agent
        self.agent = Agent(
            role="Umrah Trip Coordinator",
            goal="Collect user requirements and coordinate specialized agents to plan complete Umrah trips",
            backstory="""You are an experienced Umrah travel coordinator with deep knowledge 
            of Islamic pilgrimage requirements. You excel at understanding traveler needs and 
            coordinating with specialized teams for flights, hotels, visas, and itinerary planning.
            You are patient, detail-oriented, and ensure all religious and practical requirements are met.""",
            model=self.model,
            verbose=True
        )
    
    def collect_user_requirements(self, user_input: str) -> Dict[str, Any]:
        """
        Collect and validate user requirements for Umrah trip
        
        Returns structured data:
        - travel_dates: {departure: str, return: str}
        - travelers: [{name: str, nationality: str, age: int, passport_number: str}]
        - hotel_preferences: {proximity_to_haram: str, star_rating: int, amenities: List[str]}
        - budget: {total: float, currency: str, flexibility: str}
        - special_requirements: List[str]
        """
        
        task = Task(
            description=f"""
            Analyze the user input and extract all relevant information for planning an Umrah trip.
            
            User Input: {user_input}
            
            Extract and structure the following information:
            1. Travel dates (departure and return)
            2. Number of travelers and their details (names, nationalities, ages)
            3. Hotel preferences (proximity to Haram, star rating, amenities)
            4. Budget constraints
            5. Special requirements (wheelchair access, dietary needs, etc.)
            
            If any critical information is missing, identify what needs to be asked.
            
            Return a structured JSON with all collected information and list of missing items.
            """,
            agent=self.agent,
            expected_output="Structured JSON with user requirements and missing information list"
        )
        
        crew = Crew(agents=[self.agent], tasks=[task])
        result = crew.kickoff()
        
        return result
    
    def coordinate_agents(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate all specialized agents to create complete trip plan
        """
        
        task = Task(
            description=f"""
            Based on the collected requirements, coordinate with specialized agents:
            
            Requirements: {requirements}
            
            1. Delegate to Flight Agent: Search flights to Jeddah/Medina
            2. Delegate to Hotel Agent: Find hotels in Makkah and Madinah
            3. Delegate to Visa Agent: Check visa requirements for all travelers
            4. Delegate to Itinerary Agent: Create day-by-day Umrah schedule
            
            Collect results from all agents and create a comprehensive trip proposal.
            Ensure all components are compatible (dates, locations, timing).
            
            Return a complete trip plan with all options and recommendations.
            """,
            agent=self.agent,
            expected_output="Complete Umrah trip plan with flights, hotels, visa info, and itinerary"
        )
        
        crew = Crew(agents=[self.agent], tasks=[task])
        result = crew.kickoff()
        
        return result
    
    def present_options(self, trip_plan: Dict[str, Any]) -> str:
        """
        Present trip options to user in a clear, organized format
        """
        
        task = Task(
            description=f"""
            Present the following trip plan to the user in a clear, organized format:
            
            Trip Plan: {trip_plan}
            
            Structure the presentation as:
            1. Summary of trip (dates, travelers, destinations)
            2. Flight options (with prices, timings, airlines)
            3. Hotel options (with prices, locations, amenities)
            4. Visa requirements and processing steps
            5. Detailed itinerary for Umrah rituals
            6. Total cost breakdown
            7. Next steps for booking
            
            Make it easy to understand and compare options.
            """,
            agent=self.agent,
            expected_output="Well-formatted trip presentation for user review"
        )
        
        crew = Crew(agents=[self.agent], tasks=[task])
        result = crew.kickoff()
        
        return result
    
    def handle_booking(self, selected_options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process booking confirmations for selected options
        """
        
        task = Task(
            description=f"""
            Process booking for the selected options:
            
            Selected Options: {selected_options}
            
            1. Confirm flight bookings
            2. Confirm hotel reservations
            3. Initiate visa applications
            4. Send confirmation emails with itinerary
            5. Provide booking references and payment details
            
            Return booking confirmation with all reference numbers.
            """,
            agent=self.agent,
            expected_output="Booking confirmation with reference numbers and next steps"
        )
        
        crew = Crew(agents=[self.agent], tasks=[task])
        result = crew.kickoff()
        
        return result


def create_orchestrator_agent():
    """Factory function to create orchestrator agent"""
    return UmrahOrchestratorAgent()
