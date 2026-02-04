"""
AWS Bedrock AgentCore Client
Handles communication with deployed agents via AWS SDK
"""

import boto3
import json
from typing import Dict, Any, Optional
import uuid


class AgentCoreClient:
    """Client for invoking AgentCore agents via AWS SDK"""
    
    # Agent ARNs from deployment
    AGENT_ARNS = {
        'orchestrator': 'arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo',
        'flight': 'arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_flight_agent-ufM0XiC3fw',
        'hotel': 'arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_hotel_agent-P3Am0WF25G',
        'visa': 'arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_visa_agent-KR3L9yDFDl',
        'itinerary': 'arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_itinerary_agent-1XwH666geK'
    }
    
    def __init__(self, region_name: str = 'us-west-2'):
        """Initialize the AgentCore client"""
        self.region_name = region_name
        self.session_id = str(uuid.uuid4())
        
        # Configure boto3 with longer timeout for agent coordination (can take 2-3 minutes)
        from botocore.config import Config
        config = Config(
            read_timeout=300,  # 5 minutes
            connect_timeout=10,
            retries={'max_attempts': 0}  # Don't retry, let the agent finish
        )
        self.client = boto3.client('bedrock-agentcore', region_name=region_name, config=config)
    
    def invoke_agent(self, agent_type: str, prompt: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Invoke an AgentCore agent via AWS SDK
        
        Args:
            agent_type: Type of agent ('orchestrator', 'flight', 'hotel', 'visa', 'itinerary')
            prompt: User prompt/query
            session_id: Optional session ID for conversation continuity
            
        Returns:
            Dict containing the agent's response
        """
        if agent_type not in self.AGENT_ARNS:
            raise ValueError(f"Unknown agent type: {agent_type}. Must be one of {list(self.AGENT_ARNS.keys())}")
        
        agent_arn = self.AGENT_ARNS[agent_type]
        session = session_id or self.session_id
        
        try:
            # Prepare the payload
            payload = json.dumps({"prompt": prompt}).encode()
            
            # Invoke the agent
            response = self.client.invoke_agent_runtime(
                agentRuntimeArn=agent_arn,
                runtimeSessionId=session,
                payload=payload
            )
            
            # Process the response
            if "text/event-stream" in response.get("contentType", ""):
                # Handle streaming response
                content = []
                for line in response["response"].iter_lines(chunk_size=10):
                    if line:
                        line = line.decode("utf-8")
                        if line.startswith("data: "):
                            line = line[6:]
                            content.append(line)
                
                # Parse the complete response
                if content:
                    return json.loads(content[-1])  # Return the last chunk which should be complete
                else:
                    return {'error': 'No content in streaming response'}
                    
            elif response.get("contentType") == "application/json":
                # Handle standard JSON response
                content = []
                for chunk in response.get("response", []):
                    content.append(chunk.decode('utf-8'))
                return json.loads(''.join(content))
            else:
                return {'error': 'Unexpected content type', 'response': str(response)}
                
        except Exception as e:
            return {
                'error': str(e),
                'agent_type': agent_type,
                'agent_arn': agent_arn
            }
    
    def invoke_orchestrator(self, user_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the orchestrator agent with user requirements
        
        Args:
            user_requirements: Dictionary containing all user trip requirements
            
        Returns:
            Orchestrator's response with trip plan
        """
        # Format the requirements into a natural language prompt
        prompt = self._format_requirements_prompt(user_requirements)
        # Use a new unique session ID for each request to avoid conflicts
        new_session_id = str(uuid.uuid4())
        return self.invoke_agent('orchestrator', prompt, session_id=new_session_id)
    
    def invoke_flight_agent(self, flight_query: str) -> Dict[str, Any]:
        """Invoke the flight search agent"""
        new_session_id = str(uuid.uuid4())
        return self.invoke_agent('flight', flight_query, session_id=new_session_id)
    
    def invoke_hotel_agent(self, hotel_query: str) -> Dict[str, Any]:
        """Invoke the hotel search agent"""
        new_session_id = str(uuid.uuid4())
        return self.invoke_agent('hotel', hotel_query, session_id=new_session_id)
    
    def invoke_visa_agent(self, visa_query: str) -> Dict[str, Any]:
        """Invoke the visa requirements agent"""
        new_session_id = str(uuid.uuid4())
        return self.invoke_agent('visa', visa_query, session_id=new_session_id)
    
    def invoke_itinerary_agent(self, itinerary_query: str) -> Dict[str, Any]:
        """Invoke the itinerary planning agent"""
        new_session_id = str(uuid.uuid4())
        return self.invoke_agent('itinerary', itinerary_query, session_id=new_session_id)
    
    def _format_requirements_prompt(self, requirements: Dict[str, Any]) -> str:
        """Format user requirements into a natural language prompt"""
        
        travel_dates = requirements.get('travel_dates', {})
        travelers = requirements.get('travelers', [])
        budget = requirements.get('budget', {})
        hotel_prefs = requirements.get('hotel_preferences', {})
        flight_prefs = requirements.get('flight_preferences', {})
        special_reqs = requirements.get('special_requirements', {})
        
        prompt = f"""I want to plan an Umrah trip with the following details:

**Travel Dates:**
- Departing from: {travel_dates.get('departure_airport', 'N/A')}
- Departure date: {travel_dates.get('departure', 'N/A')}
- Return date: {travel_dates.get('return', 'N/A')}
- Duration: {travel_dates.get('duration', 'N/A')} days
- Arrival city: {travel_dates.get('arrival_city', 'Jeddah')}

**Travelers:**
- Number of travelers: {len(travelers)}
"""
        
        for i, traveler in enumerate(travelers, 1):
            prompt += f"- Traveler {i}: {traveler.get('name', 'N/A')}, {traveler.get('nationality', 'N/A')}, Age {traveler.get('age', 'N/A')}\n"
        
        prompt += f"""
**Budget:**
- Total budget: {budget.get('currency', 'USD')} {budget.get('total', 'N/A')}
- Per person: {budget.get('currency', 'USD')} {budget.get('per_person', 'N/A')}
- Flexibility: {budget.get('flexibility', 'Moderate')}

**Hotel Preferences:**
- Makkah: {hotel_prefs.get('makkah', {}).get('star_rating', 4)} stars, {hotel_prefs.get('makkah', {}).get('proximity', 'Walking distance')}
- Madinah: {hotel_prefs.get('madinah', {}).get('star_rating', 4)} stars, {hotel_prefs.get('madinah', {}).get('proximity', 'Walking distance')}

**Flight Preferences:**
- Cabin class: {flight_prefs.get('cabin_class', 'Economy')}
- Direct flights: {flight_prefs.get('direct_flights', True)}

**Special Requirements:**
"""
        
        if special_reqs.get('wheelchair_access'):
            prompt += "- Wheelchair accessibility required\n"
        if special_reqs.get('elderly_travelers'):
            prompt += "- Elderly travelers need special assistance\n"
        if special_reqs.get('first_time_umrah'):
            prompt += "- First time performing Umrah\n"
        if special_reqs.get('additional_notes'):
            prompt += f"- Additional notes: {special_reqs.get('additional_notes')}\n"
        
        # Add custom itinerary requirements
        if special_reqs.get('custom_itinerary'):
            prompt += f"\n**Custom Itinerary Requirements:**\n{special_reqs.get('custom_itinerary')}\n"
            prompt += "\nIMPORTANT: Please follow this custom itinerary when booking hotels. Book hotels in each city for the specified number of days.\n"
        
        prompt += "\nPlease help me plan this Umrah trip with MULTIPLE flight options (at least 2-3 options), MULTIPLE hotel recommendations for each city (at least 2-3 options per city), visa requirements, and a detailed itinerary."
        prompt += "\n\nFor flights: Provide at least 2-3 different flight options with different airlines, times, and price points."
        prompt += "\nFor hotels: Provide at least 2-3 hotel options for each city (Makkah and Madinah) with different star ratings and distances from Haram."
        
        return prompt
    
    def extract_text_from_response(self, response: Dict[str, Any]) -> str:
        """
        Extract text from agent response
        
        Args:
            response: Agent response dictionary
            
        Returns:
            Extracted text string
        """
        if 'error' in response:
            return f"Error: {response['error']}"
        
        # Handle different response formats
        if 'result' in response:
            result = response['result']
            
            # If result is a dict with content
            if isinstance(result, dict):
                if 'content' in result and isinstance(result['content'], list):
                    # Extract text from content array
                    texts = []
                    for item in result['content']:
                        if isinstance(item, dict) and 'text' in item:
                            texts.append(item['text'])
                    return '\n'.join(texts) if texts else str(result)
                else:
                    return str(result)
            else:
                return str(result)
        
        return str(response)


# Don't use singleton - create new client for each request to avoid session conflicts
def get_agentcore_client() -> AgentCoreClient:
    """Create a new AgentCore client instance"""
    return AgentCoreClient()
