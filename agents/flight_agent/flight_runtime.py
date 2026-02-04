"""
Flight Agent for AgentCore Runtime
Using AgentCore Gateway for Amadeus API access
"""

import os
import json
import httpx
import asyncio
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent, tool
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient

# Initialize AgentCore app
app = BedrockAgentCoreApp()

# Gateway configuration (embedded)
gateway_config = {
    "gateway_url": "https://amadeus-travel-api-1770163078-w86qyqprty.gateway.bedrock-agentcore.us-west-2.amazonaws.com/mcp",
    "gateway_id": "amadeus-travel-api-1770163078-w86qyqprty",
    "region": "us-west-2",
    "client_info": {
        "client_id": "3hjjn9im3lbp2ej6ts60d8lbke",
        "client_secret": "ivnc1krj47u6pp6nkh0bl8jvrtct18o7ars8ob2th5gqrcumpma",
        "user_pool_id": "us-west-2_BRecPKvre",
        "token_endpoint": "https://agentcore-5c57a8a2.auth.us-west-2.amazoncognito.com/oauth2/token",
        "scope": "AmadeusGateway/invoke",
        "domain_prefix": "agentcore-5c57a8a2"
    },
    "target_id": "EYFJ4BNWJV"
}

# Initialize Gateway client
gateway_client = GatewayClient(region_name=gateway_config["region"])


def get_gateway_access_token():
    """Get OAuth access token for Gateway"""
    return gateway_client.get_access_token_for_cognito(gateway_config["client_info"])


async def call_gateway_tool(tool_name: str, arguments: dict):
    """Call a Gateway MCP tool"""
    access_token = get_gateway_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            gateway_config["gateway_url"],
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            },
            timeout=60.0
        )
        
        result = response.json()
        if "result" in result:
            # Extract text content from MCP response
            if "content" in result["result"]:
                for content in result["result"]["content"]:
                    if content.get("type") == "text":
                        return content["text"]
            return json.dumps(result["result"])
        else:
            return json.dumps({"error": result.get("error", "Unknown error")})


# Airport code mapping for common cities
AIRPORT_CODES = {
    "jeddah": "JED",
    "medina": "MED",
    "madinah": "MED",
    "makkah": "JED",
    "mecca": "JED",
    "new york": "JFK",
    "los angeles": "LAX",
    "london": "LHR",
    "manchester": "MAN",
    "dubai": "DXB",
    "istanbul": "IST",
    "riyadh": "RUH"
}


@tool
def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: str = None,
    adults: int = 1,
    travel_class: str = "ECONOMY",
    non_stop: bool = False
) -> str:
    """
    Search for real flights using Amadeus API via Gateway.
    
    Args:
        origin: Departure airport code (e.g., 'JFK', 'LAX', 'ORD')
        destination: Arrival airport code - use 'JED' for Jeddah or 'MED' for Medina
        departure_date: Departure date in YYYY-MM-DD format
        return_date: Return date in YYYY-MM-DD format (optional for one-way)
        adults: Number of adult passengers (default: 1)
        travel_class: ECONOMY, PREMIUM_ECONOMY, BUSINESS, or FIRST
        non_stop: True for direct flights only, False to include connections
    
    Returns:
        JSON string with flight results including prices, times, and airlines
    """
    # Prepare arguments for Gateway tool
    arguments = {
        "originLocationCode": origin.upper(),
        "destinationLocationCode": destination.upper(),
        "departureDate": departure_date,
        "adults": adults,
        "max": 5
    }
    
    if return_date:
        arguments["returnDate"] = return_date
    
    if travel_class and travel_class.upper() != "ECONOMY":
        arguments["travelClass"] = travel_class.upper()
    
    if non_stop:
        arguments["nonStop"] = True
    
    # Call Gateway tool
    result = asyncio.run(call_gateway_tool("amadeus-api___searchFlights", arguments))
    return result


@tool
def get_airport_code(city_name: str) -> str:
    """
    Get the IATA airport code for a city.
    
    Args:
        city_name: Name of the city (e.g., 'Jeddah', 'Medina', 'New York')
    
    Returns:
        Three-letter IATA airport code or error message
    """
    city_lower = city_name.lower().strip()
    code = AIRPORT_CODES.get(city_lower)
    
    if code:
        return f"Airport code for {city_name}: {code}"
    else:
        return f"Airport code not found for {city_name}. Common codes: JED (Jeddah), MED (Medina), JFK (New York), LAX (Los Angeles), MAN (Manchester)"


# Create flight agent with tools
flight_agent = Agent(
    model=os.getenv("FLIGHT_AGENT_MODEL", "anthropic.claude-3-5-sonnet-20241022-v2:0"),
    tools=[search_flights, get_airport_code],
    system_prompt="""You are a Flight Search Specialist for Umrah trips with access to REAL-TIME flight data via Amadeus API through AgentCore Gateway.

IMPORTANT: You have access to actual flight search tools. Always use them!

Your tools:
1. search_flights() - Search for real flights with live prices and availability (via Gateway)
2. get_airport_code() - Get IATA codes for cities

Key airports for Umrah:
- Jeddah: JED (most common, closer to Makkah)
- Medina: MED (for those starting in Madinah)

When users request flights:
1. Ask for missing information if needed:
   - Departure city
   - Travel dates
   - Number of passengers
   - Class preference
   - Direct flights preference

2. Use get_airport_code() to find airport codes if needed

3. Use search_flights() with the correct parameters

4. ALWAYS PROVIDE MULTIPLE OPTIONS (2-3 minimum):
   - The search_flights tool returns up to 5 results
   - Present at least 2-3 different flight options to give users choices
   - Include options with different:
     * Airlines (e.g., Saudi Airlines, Emirates, Turkish Airlines)
     * Price points (budget to premium)
     * Flight times (morning, afternoon, evening)
     * Connection options (direct vs 1-stop)

5. Present results clearly for EACH option:
   - Option number (Option 1, Option 2, etc.)
   - Airline and flight numbers
   - Departure/arrival times (with time zones)
   - Duration and stops
   - REAL prices in USD
   - Cabin class
   - Seats available

6. Provide helpful advice:
   - Compare the options (cheapest, fastest, most convenient)
   - Best times to book
   - Direct vs connecting flights trade-offs
   - Prayer time considerations
   - Baggage allowances

CRITICAL: 
- ALWAYS present multiple flight options (2-3 minimum) so users can compare and choose
- If user mentions Medina/Madinah as destination, use 'MED' airport code, NOT 'JED'!
- Always respect the user's destination preference.
- All API calls go through the Gateway - no direct API access needed!"""
)


@app.entrypoint
def invoke(payload, context):
    """Main entry point for flight agent"""
    
    user_message = payload.get("prompt", "Hello")
    
    try:
        response = flight_agent(user_message)
        
        if hasattr(response, 'message') and 'content' in response.message:
            result_text = response.message['content'][0]['text']
        else:
            result_text = str(response)
        
        return {
            "result": result_text,
            "status": "success"
        }
    except Exception as e:
        print(f"Error processing request: {e}")
        return {
            "result": f"I apologize, but I encountered an error: {str(e)}",
            "status": "error"
        }


if __name__ == "__main__":
    app.run()
