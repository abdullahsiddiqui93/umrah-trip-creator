"""
Visa Agent - Handles visa requirements and processing for Umrah travelers
"""

from strands_agents import Agent, Task, Crew
from typing import Dict, List, Any
import os


class VisaAgent:
    """Specialized agent for visa requirements and processing"""
    
    def __init__(self):
        self.model = os.getenv("VISA_AGENT_MODEL", "gpt-4o-2024-08-06")
        
        self.agent = Agent(
            role="Visa Processing Specialist",
            goal="Guide travelers through visa requirements and application process for Saudi Arabia Umrah visa",
            backstory="""You are an expert in Saudi Arabia visa regulations and requirements.
            You have comprehensive knowledge of visa types, application procedures, required 
            documents, and processing times for different nationalities. You stay updated on 
            the latest visa policies and help pilgrims navigate the application process smoothly.""",
            model=self.model,
            verbose=True
        )
    
    def check_visa_requirements(self, travelers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Check visa requirements for each traveler based on nationality
        
        Args:
            travelers: List of dicts containing:
                - name: str
                - nationality: str
                - age: int
                - passport_number: str (optional)
        
        Returns:
            List of visa requirements for each traveler
        """
        
        task = Task(
            description=f"""
            Check visa requirements for these travelers:
            {travelers}
            
            For each traveler, determine:
            1. Visa type required (Umrah visa, eVisa, visa on arrival, etc.)
            2. Processing time and validity period
            3. Required documents
            4. Application procedure (online, embassy, etc.)
            5. Visa fees
            6. Special requirements based on nationality
            7. Vaccination requirements (Meningitis, COVID-19, etc.)
            
            Provide detailed, accurate information for each traveler.
            
            Return as structured JSON array with complete visa information.
            """,
            agent=self.agent,
            expected_output="JSON array of visa requirements for each traveler"
        )
        
        crew = Crew(agents=[self.agent], tasks=[task])
        result = crew.kickoff()
        
        return result
    
    def create_application_guide(self, visa_requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create step-by-step visa application guide"""
        
        task = Task(
            description=f"""
            Create a comprehensive visa application guide based on these requirements:
            {visa_requirements}
            
            Provide:
            1. Step-by-step application process
            2. Document checklist
            3. Timeline and deadlines
            4. Common mistakes to avoid
            5. Tips for faster processing
            6. Contact information for support
            
            Make it easy to follow and actionable.
            """,
            agent=self.agent,
            expected_output="Comprehensive visa application guide"
        )
        
        crew = Crew(agents=[self.agent], tasks=[task])
        result = crew.kickoff()
        
        return result
    
    def estimate_processing_time(self, nationalities: List[str]) -> Dict[str, Any]:
        """Estimate visa processing time for different nationalities"""
        
        task = Task(
            description=f"""
            Estimate visa processing times for these nationalities:
            {nationalities}
            
            Provide:
            1. Standard processing time
            2. Express processing options (if available)
            3. Factors that may delay processing
            4. Best time to apply
            5. Success rate statistics
            
            Return as structured data.
            """,
            agent=self.agent,
            expected_output="Processing time estimates with details"
        )
        
        crew = Crew(agents=[self.agent], tasks=[task])
        result = crew.kickoff()
        
        return result


def create_visa_agent():
    """Factory function to create visa agent"""
    return VisaAgent()
