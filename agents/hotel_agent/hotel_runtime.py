"""
Hotel Agent for AgentCore Runtime
Using AgentCore Gateway for Amadeus Hotel API access
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

# Landmark coordinates for Umrah
LANDMARKS = {
    'masjid_al_haram': {
        'name': 'Masjid al-Haram (Makkah)',
        'latitude': 21.4225,
        'longitude': 39.8262
    },
    'masjid_nabawi': {
        'name': 'Masjid an-Nabawi (Medina)',
        'latitude': 24.4672,
        'longitude': 39.6111
    }
}

# City code mapping
CITY_CODES = {
    "makkah": "MEC",
    "mecca": "MEC",
    "medina": "MED",
    "madinah": "MED",
    "jeddah": "JED",
    "riyadh": "RUH"
}


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


@tool
def search_hotels(
    city: str,
    check_in: str,
    check_out: str,
    adults: int = 2,
    star_rating: str = None,
    near_haram: bool = True,
    max_results: int = 10
) -> str:
    """
    Search for real hotels using Amadeus Hotel API via Gateway.
    
    Args:
        city: City name - use 'Makkah' or 'Medina' for Umrah
        check_in: Check-in date in YYYY-MM-DD format
        check_out: Check-out date in YYYY-MM-DD format
        adults: Number of adult guests (default: 2)
        star_rating: Filter by star rating - use '4,5' for 4 and 5 star hotels
        near_haram: If True, search near Haram/Masjid (default: True)
        max_results: Maximum number of results to return (default: 10)
    
    Returns:
        JSON string with hotel results including prices, ratings, and distances
    """
    city_lower = city.lower().strip()
    
    # Determine search method
    if near_haram:
        # Search near Haram landmarks for better proximity results
        if city_lower in ['makkah', 'mecca']:
            landmark = LANDMARKS['masjid_al_haram']
            arguments = {
                "latitude": landmark['latitude'],
                "longitude": landmark['longitude'],
                "radius": 2,
                "radiusUnit": "KM"
            }
            result = asyncio.run(call_gateway_tool("amadeus-api___searchHotelsByLocation", arguments))
        elif city_lower in ['medina', 'madinah']:
            landmark = LANDMARKS['masjid_nabawi']
            arguments = {
                "latitude": landmark['latitude'],
                "longitude": landmark['longitude'],
                "radius": 2,
                "radiusUnit": "KM"
            }
            result = asyncio.run(call_gateway_tool("amadeus-api___searchHotelsByLocation", arguments))
        else:
            # Fallback to city search
            city_code = CITY_CODES.get(city_lower)
            if not city_code:
                return json.dumps({
                    "error": f"Unknown city: {city}. Please use 'Makkah' or 'Medina'"
                })
            
            arguments = {
                "cityCode": city_code,
                "radius": 5,
                "radiusUnit": "KM"
            }
            result = asyncio.run(call_gateway_tool("amadeus-api___searchHotelsByCity", arguments))
    else:
        # City-wide search
        city_code = CITY_CODES.get(city_lower)
        if not city_code:
            return json.dumps({
                "error": f"Unknown city: {city}. Please use 'Makkah' or 'Medina'"
            })
        
        arguments = {
            "cityCode": city_code,
            "radius": 5,
            "radiusUnit": "KM"
        }
        result = asyncio.run(call_gateway_tool("amadeus-api___searchHotelsByCity", arguments))
    
    return result


@tool
def get_city_code(city_name: str) -> str:
    """
    Get the IATA city code for hotel search.
    
    Args:
        city_name: Name of the city (e.g., 'Makkah', 'Medina')
    
    Returns:
        Three-letter IATA city code or error message
    """
    city_lower = city_name.lower().strip()
    code = CITY_CODES.get(city_lower)
    
    if code:
        return f"City code for {city_name}: {code}"
    else:
        return f"City code not found for {city_name}. Common codes: MEC (Makkah), MED (Medina), JED (Jeddah)"


# Create hotel agent with tools
hotel_agent = Agent(
    model=os.getenv("HOTEL_AGENT_MODEL", "anthropic.claude-3-5-sonnet-20241022-v2:0"),
    tools=[search_hotels, get_city_code],
    system_prompt="""You are a Hotel Booking Specialist for Umrah trips with access to REAL-TIME hotel data via Amadeus API through AgentCore Gateway.

IMPORTANT: You have access to actual hotel search tools. Always use them!

Your tools:
1. search_hotels() - Search for real hotels with live prices and availability (via Gateway)
2. get_city_code() - Get IATA city codes for hotel searches

Key cities for Umrah:
- Makkah (Mecca): Hotels near Masjid al-Haram
- Medina (Madinah): Hotels near Masjid an-Nabawi

When users request hotels:
1. Ask for missing information if needed:
   - City (Makkah, Medina, or both)
   - Check-in and check-out dates
   - Number of guests
   - Star rating preference (4-5 stars recommended)
   - Budget range

2. Use search_hotels() with the correct parameters
   - Set near_haram=True for hotels close to the Haram (highly recommended)
   - This searches within 2km of Masjid al-Haram or Masjid an-Nabawi
   - Set max_results=10 to get multiple options

3. ALWAYS PROVIDE MULTIPLE OPTIONS (2-3 minimum):
   - The search_hotels tool returns up to 10 results
   - Present at least 2-3 different hotel options to give users choices
   - Include options with different:
     * Star ratings (3-star, 4-star, 5-star)
     * Price points (budget to luxury)
     * Distances from Haram (walking distance vs further)
     * Amenities and features

4. Present results clearly for EACH option:
   - Option number (Option 1, Option 2, etc.)
   - Hotel name and star rating
   - Distance to Haram (very important!)
   - REAL prices per night and total stay cost
   - Address and location details
   - Available amenities
   - Room types and descriptions
   - Cancellation policies

5. Provide helpful advice:
   - Compare the options (closest, best value, most luxurious)
   - Proximity to Haram (walking distance is highly valued)
   - Best areas to stay
   - Family-friendly options
   - Transportation options
   - Prayer facilities

6. For Makkah hotels:
   - Emphasize distance to Masjid al-Haram
   - Mention if within walking distance (<1km is ideal)
   - Note proximity to Clock Tower area
   - Highlight Haram view availability

7. For Medina hotels:
   - Emphasize distance to Masjid an-Nabawi
   - Mention proximity to historical sites
   - Note if within walking distance

8. Handle Custom Itineraries:
   - If user specifies staying in different cities for specific durations, search each separately
   - Example: "Madinah 1 night, then Makkah 4 nights, then Madinah 4 nights"
     * Search Madinah hotels for first date range
     * Search Makkah hotels for second date range
     * Search Madinah hotels for third date range
   - Present options for each leg of the journey

CRITICAL: 
- ALWAYS present multiple hotel options (2-3 minimum per city) so users can compare and choose
- Always use the search_hotels() tool to get real, current prices and availability from Amadeus API via Gateway!
- All API calls go through the Gateway - no direct API access needed!

The Amadeus API provides:
- Real-time pricing in USD
- Actual hotel availability
- Detailed hotel information
- Distance calculations from landmarks
- Room descriptions and policies

Be specific about dates and always show the actual prices returned by the API."""
)


@app.entrypoint
def invoke(payload, context):
    """Main entry point for hotel agent"""
    
    user_message = payload.get("prompt", "Hello")
    
    try:
        response = hotel_agent(user_message)
        
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
