#!/usr/bin/env python3
"""
Test the Amadeus Gateway
"""

from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
import json
import httpx
import asyncio

async def test_gateway():
    """Test the Amadeus Gateway"""
    
    # Load configuration
    try:
        with open("amadeus_gateway_config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Error: amadeus_gateway_config.json not found!")
        print("Please run 'python setup_amadeus_gateway.py' first.")
        return
    
    gateway_url = config["gateway_url"]
    client_info = config["client_info"]
    region = config["region"]
    
    print("=" * 60)
    print("🧪 Testing Amadeus Gateway")
    print("=" * 60)
    print(f"Gateway URL: {gateway_url}\n")
    
    # Get access token
    print("Step 1: Getting access token...")
    client = GatewayClient(region_name=region)
    access_token = client.get_access_token_for_cognito(client_info)
    print("✓ Access token obtained\n")
    
    # Test 1: List available tools
    print("Step 2: Listing available tools...")
    async with httpx.AsyncClient() as http_client:
        response = await http_client.post(
            gateway_url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            },
            timeout=30.0
        )
        
        result = response.json()
        if "result" in result and "tools" in result["result"]:
            tools = result["result"]["tools"]
            print(f"✓ Found {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool['name']}: {tool.get('description', 'No description')}")
        else:
            print(f"❌ Error listing tools: {result}")
            return
    
    print()
    
    # Test 2: Search flights
    print("Step 3: Testing flight search...")
    async with httpx.AsyncClient() as http_client:
        response = await http_client.post(
            gateway_url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "amadeus-api___searchFlights",  # Use prefixed name
                    "arguments": {
                        "originLocationCode": "JFK",
                        "destinationLocationCode": "JED",
                        "departureDate": "2026-03-15",
                        "returnDate": "2026-03-25",
                        "adults": 2,
                        "max": 3
                    }
                }
            },
            timeout=60.0
        )
        
        result = response.json()
        if "result" in result:
            print("✓ Flight search successful!")
            # Parse the result
            if "content" in result["result"]:
                for content in result["result"]["content"]:
                    if content.get("type") == "text":
                        print(f"  Response: {content['text'][:200]}...")
        else:
            print(f"❌ Error searching flights: {result}")
    
    print()
    
    # Test 3: Search hotels
    print("Step 4: Testing hotel search...")
    async with httpx.AsyncClient() as http_client:
        response = await http_client.post(
            gateway_url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            json={
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "amadeus-api___searchHotelsByLocation",  # Use prefixed name
                    "arguments": {
                        "latitude": 21.4225,
                        "longitude": 39.8262,
                        "radius": 2,
                        "radiusUnit": "KM"
                    }
                }
            },
            timeout=60.0
        )
        
        result = response.json()
        if "result" in result:
            print("✓ Hotel search successful!")
            if "content" in result["result"]:
                for content in result["result"]["content"]:
                    if content.get("type") == "text":
                        print(f"  Response: {content['text'][:200]}...")
        else:
            print(f"❌ Error searching hotels: {result}")
    
    print()
    print("=" * 60)
    print("✅ Gateway testing complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_gateway())
