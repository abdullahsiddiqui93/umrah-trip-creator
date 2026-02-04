"""
Orchestrator Agent for AgentCore Runtime
With Agent-to-Agent communication for real API data
"""

import os
import json
import boto3
import uuid
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent, tool

# Initialize AgentCore app
app = BedrockAgentCoreApp()

# Initialize boto3 client for calling other agents
bedrock_client = boto3.client('bedrock-agentcore', region_name=os.getenv('AWS_REGION', 'us-west-2'))

# Agent ARNs from environment
FLIGHT_AGENT_ARN = "arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_flight_agent-ufM0XiC3fw"
HOTEL_AGENT_ARN = "arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_hotel_agent-P3Am0WF25G"
VISA_AGENT_ARN = "arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_visa_agent-KR3L9yDFDl"
ITINERARY_AGENT_ARN = "arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_itinerary_agent-1XwH666geK"


@tool
def search_flights(request: str) -> str:
    """
    Search for real flights using the Flight Agent with Amadeus API.
    
    Args:
        request: Natural language request for flights (e.g., "Find flights from New York to Medina departing March 15, 2026 returning March 25, 2026 for 2 adults")
    
    Returns:
        Flight search results with real prices and availability
    """
    try:
        # Prepare payload as JSON bytes
        payload = json.dumps({"prompt": request}).encode()
        
        # Invoke the flight agent with proper session ID (must be 33+ chars)
        response = bedrock_client.invoke_agent_runtime(
            agentRuntimeArn=FLIGHT_AGENT_ARN,
            runtimeSessionId=str(uuid.uuid4()),  # 36 characters
            payload=payload
        )
        
        # Handle streaming response
        content_type = response.get("contentType", "")
        if "text/event-stream" in content_type:
            # Handle streaming response
            content = []
            for line in response["response"].iter_lines(chunk_size=10):
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        line = line[6:]
                        content.append(line)
            return "\n".join(content)
        elif content_type == "application/json":
            # Handle standard JSON response
            content = []
            for chunk in response.get("response", []):
                content.append(chunk.decode('utf-8'))
            return ''.join(content)
        else:
            return str(response)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error searching flights: {error_details}")
        return f"Error searching flights: {str(e)}"


@tool
def search_hotels(request: str) -> str:
    """
    Search for real hotels using the Hotel Agent with Booking.com API.
    
    Args:
        request: Natural language request for hotels (e.g., "Find hotels in Makkah near Haram for March 15-20, 2026 for 2 adults, prefer 4-5 star")
    
    Returns:
        Hotel search results with real prices and availability
    """
    try:
        # Prepare payload as JSON bytes
        payload = json.dumps({"prompt": request}).encode()
        
        # Invoke the hotel agent with proper session ID (must be 33+ chars)
        response = bedrock_client.invoke_agent_runtime(
            agentRuntimeArn=HOTEL_AGENT_ARN,
            runtimeSessionId=str(uuid.uuid4()),  # 36 characters
            payload=payload
        )
        
        # Handle streaming response
        content_type = response.get("contentType", "")
        if "text/event-stream" in content_type:
            # Handle streaming response
            content = []
            for line in response["response"].iter_lines(chunk_size=10):
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        line = line[6:]
                        content.append(line)
            return "\n".join(content)
        elif content_type == "application/json":
            # Handle standard JSON response
            content = []
            for chunk in response.get("response", []):
                content.append(chunk.decode('utf-8'))
            return ''.join(content)
        else:
            return str(response)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error searching hotels: {error_details}")
        return f"Error searching hotels: {str(e)}"


@tool
def get_visa_info(request: str) -> str:
    """
    Get visa requirements and information using the Visa Agent.
    
    Args:
        request: Natural language request for visa info (e.g., "What are the visa requirements for US citizens?")
    
    Returns:
        Visa requirements and application process information
    """
    try:
        # Prepare payload as JSON bytes
        payload = json.dumps({"prompt": request}).encode()
        
        # Invoke the visa agent with proper session ID (must be 33+ chars)
        response = bedrock_client.invoke_agent_runtime(
            agentRuntimeArn=VISA_AGENT_ARN,
            runtimeSessionId=str(uuid.uuid4()),  # 36 characters
            payload=payload
        )
        
        # Handle streaming response
        content_type = response.get("contentType", "")
        if "text/event-stream" in content_type:
            # Handle streaming response
            content = []
            for line in response["response"].iter_lines(chunk_size=10):
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        line = line[6:]
                        content.append(line)
            return "\n".join(content)
        elif content_type == "application/json":
            # Handle standard JSON response
            content = []
            for chunk in response.get("response", []):
                content.append(chunk.decode('utf-8'))
            return ''.join(content)
        else:
            return str(response)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error getting visa info: {error_details}")
        return f"Error getting visa info: {str(e)}"


@tool
def create_itinerary(request: str) -> str:
    """
    Create a detailed Umrah itinerary using the Itinerary Agent.
    
    Args:
        request: Natural language request for itinerary (e.g., "Create a 10-day Umrah itinerary starting in Medina")
    
    Returns:
        Detailed day-by-day itinerary with Umrah rituals and recommendations
    """
    try:
        # Prepare payload as JSON bytes
        payload = json.dumps({"prompt": request}).encode()
        
        # Invoke the itinerary agent with proper session ID (must be 33+ chars)
        response = bedrock_client.invoke_agent_runtime(
            agentRuntimeArn=ITINERARY_AGENT_ARN,
            runtimeSessionId=str(uuid.uuid4()),  # 36 characters
            payload=payload
        )
        
        # Handle streaming response
        content_type = response.get("contentType", "")
        if "text/event-stream" in content_type:
            # Handle streaming response
            content = []
            for line in response["response"].iter_lines(chunk_size=10):
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        line = line[6:]
                        content.append(line)
            return "\n".join(content)
        elif content_type == "application/json":
            # Handle standard JSON response
            content = []
            for chunk in response.get("response", []):
                content.append(chunk.decode('utf-8'))
            return ''.join(content)
        else:
            return str(response)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error creating itinerary: {error_details}")
        return f"Error creating itinerary: {str(e)}"


@app.entrypoint
def invoke(payload, context):
    """Main entry point for orchestrator agent"""
    
    user_message = payload.get("prompt", "Hello")
    
    try:
        # Create a NEW agent instance for each request to avoid concurrency issues
        orchestrator = Agent(
            model=os.getenv("ORCHESTRATOR_MODEL", "anthropic.claude-3-5-sonnet-20241022-v2:0"),
            tools=[search_flights, search_hotels, get_visa_info, create_itinerary],
            system_prompt="""You are the main Umrah Trip Coordinator with access to specialized agents for real-time data.

CRITICAL: You have access to tools that call specialized agents with REAL APIs:
1. search_flights() - Calls Flight Agent with Amadeus API for REAL flight data
2. search_hotels() - Calls Hotel Agent with Amadeus Hotel API for REAL hotel data
3. get_visa_info() - Calls Visa Agent for visa requirements
4. create_itinerary() - Calls Itinerary Agent for detailed Umrah plans

ALWAYS use these tools when users ask about flights, hotels, visas, or itineraries!

Your workflow:
1. Greet users and understand their Umrah planning needs
2. Gather key information:
   - Travel dates
   - Number of travelers (adults, children)
   - Departure city
   - Destination preference (Jeddah or Medina arrival)
   - Budget range
   - Hotel preferences (star rating, proximity to Haram)
   - Nationality (for visa requirements)
   - Custom itinerary requirements (which cities, in what order, for how many days)

3. When you have enough information, USE THE TOOLS TO GET MULTIPLE OPTIONS:
   
   For FLIGHTS - Request AT LEAST 2-3 OPTIONS:
   - Call search_flights() and explicitly ask for "multiple flight options with different airlines and price points"
   - Example: "Find 2-3 flight options from New York to Jeddah departing March 15, 2026 returning March 25, 2026 for 2 adults. Include different airlines and price ranges."
   
   For HOTELS - Request AT LEAST 2-3 OPTIONS PER CITY:
   - If user has custom itinerary (e.g., "Madinah first, then Makkah"), follow it exactly
   - Call search_hotels() separately for each city with specific dates
   - Example for custom itinerary "Madinah 1 night, Makkah 4 nights, Madinah 4 nights":
     * "Find 2-3 hotel options in Madinah near Haram for March 15-16, 2026 for 2 adults, 4-5 star"
     * "Find 2-3 hotel options in Makkah near Haram for March 16-20, 2026 for 2 adults, 4-5 star"
     * "Find 2-3 hotel options in Madinah near Haram for March 20-24, 2026 for 2 adults, 4-5 star"
   - If no custom itinerary, use standard split (e.g., half in Makkah, half in Madinah)
   
   For VISAS:
   - Call get_visa_info() with nationality
   
   For ITINERARY:
   - Call create_itinerary() with trip details and custom requirements if provided

4. Present results clearly with MULTIPLE OPTIONS:
   - Show ALL flight options (2-3) with prices, airlines, times
   - Show ALL hotel options (2-3 per city) with prices, star ratings, distances
   - Highlight key details (flight times, hotel distances to Haram)
   - Provide recommendations based on the data
   - Calculate total trip costs for different combinations

5. Handle Custom Itineraries:
   - If user specifies "Madinah first, then Makkah" or similar, FOLLOW IT EXACTLY
   - Book hotels in the order and duration specified
   - Adjust flight arrival/departure cities accordingly
   - Explain the itinerary flow clearly

6. Help users make decisions:
   - Compare options (budget vs premium, direct vs connecting flights)
   - Explain trade-offs
   - Provide Islamic guidance
   - Answer follow-up questions

IMPORTANT NOTES:
- ALWAYS request multiple options (2-3) from each agent
- If user has custom itinerary requirements, follow them precisely when booking hotels
- If user mentions Medina/Madinah as arrival city, make sure to specify that in flight search
- Always emphasize hotel proximity to Haram (very important for pilgrims)
- Consider prayer times when suggesting flight schedules
- Be patient and helpful throughout the planning process

Remember: You are coordinating specialized agents - use them to provide accurate, real-time information with MULTIPLE OPTIONS!"""
        )
        
        response = orchestrator(user_message)
        return {"result": response.message}
    except Exception as e:
        print(f"Error processing request: {e}")
        import traceback
        traceback.print_exc()
        return {
            "result": {"content": [{"text": f"I apologize, but I encountered an error: {str(e)}"}]},
            "status": "error"
        }


if __name__ == "__main__":
    app.run()
