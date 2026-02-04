#!/usr/bin/env python3
"""
Setup AgentCore Gateway for Amadeus API
This creates a Gateway that exposes Amadeus Flight and Hotel APIs as MCP tools
The API credentials are stored in the Gateway, so agents don't need them
"""

from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_amadeus_openapi_spec():
    """Create OpenAPI specification for Amadeus APIs"""
    
    # Simplified OpenAPI spec for Amadeus Flight and Hotel APIs
    amadeus_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Amadeus Travel API",
            "description": "Flight and Hotel search APIs from Amadeus",
            "version": "1.0.0"
        },
        "servers": [
            {"url": "https://test.api.amadeus.com"}
        ],
        "paths": {
            "/v2/shopping/flight-offers": {
                "get": {
                    "operationId": "searchFlights",
                    "summary": "Search for flight offers",
                    "description": "Search for real-time flight offers with prices and availability",
                    "parameters": [
                        {
                            "name": "originLocationCode",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": "IATA airport code for departure (e.g., JFK, LAX)"
                        },
                        {
                            "name": "destinationLocationCode",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": "IATA airport code for arrival (e.g., JED for Jeddah, MED for Medina)"
                        },
                        {
                            "name": "departureDate",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string", "format": "date"},
                            "description": "Departure date in YYYY-MM-DD format"
                        },
                        {
                            "name": "returnDate",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string", "format": "date"},
                            "description": "Return date in YYYY-MM-DD format (optional for one-way)"
                        },
                        {
                            "name": "adults",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer", "default": 1},
                            "description": "Number of adult passengers"
                        },
                        {
                            "name": "travelClass",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string", "enum": ["ECONOMY", "PREMIUM_ECONOMY", "BUSINESS", "FIRST"]},
                            "description": "Cabin class preference"
                        },
                        {
                            "name": "nonStop",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "boolean", "default": False},
                            "description": "If true, only direct flights"
                        },
                        {
                            "name": "max",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer", "default": 5},
                            "description": "Maximum number of results"
                        },
                        {
                            "name": "currencyCode",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string", "default": "USD"},
                            "description": "Currency for prices"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Flight offers found",
                            "content": {
                                "application/json": {
                                    "schema": {"type": "object"}
                                }
                            }
                        }
                    }
                }
            },
            "/v1/reference-data/locations/hotels/by-city": {
                "get": {
                    "operationId": "searchHotelsByCity",
                    "summary": "Search hotels by city",
                    "description": "Find hotels in a specific city",
                    "parameters": [
                        {
                            "name": "cityCode",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": "IATA city code (e.g., MEC for Makkah, MED for Medina)"
                        },
                        {
                            "name": "radius",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer", "default": 5},
                            "description": "Search radius"
                        },
                        {
                            "name": "radiusUnit",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string", "enum": ["KM", "MILE"], "default": "KM"},
                            "description": "Unit for radius"
                        },
                        {
                            "name": "hotelSource",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string", "default": "ALL"},
                            "description": "Hotel source"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Hotels found",
                            "content": {
                                "application/json": {
                                    "schema": {"type": "object"}
                                }
                            }
                        }
                    }
                }
            },
            "/v1/reference-data/locations/hotels/by-geocode": {
                "get": {
                    "operationId": "searchHotelsByLocation",
                    "summary": "Search hotels by geographic coordinates",
                    "description": "Find hotels near a specific location (e.g., near Haram)",
                    "parameters": [
                        {
                            "name": "latitude",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "number"},
                            "description": "Latitude (e.g., 21.4225 for Masjid al-Haram)"
                        },
                        {
                            "name": "longitude",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "number"},
                            "description": "Longitude (e.g., 39.8262 for Masjid al-Haram)"
                        },
                        {
                            "name": "radius",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer", "default": 2},
                            "description": "Search radius"
                        },
                        {
                            "name": "radiusUnit",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string", "enum": ["KM", "MILE"], "default": "KM"},
                            "description": "Unit for radius"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Hotels found",
                            "content": {
                                "application/json": {
                                    "schema": {"type": "object"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "securitySchemes": {
                "OAuth2": {
                    "type": "oauth2",
                    "flows": {
                        "clientCredentials": {
                            "tokenUrl": "https://test.api.amadeus.com/v1/security/oauth2/token",
                            "scopes": {}
                        }
                    }
                }
            }
        },
        "security": [{"OAuth2": []}]
    }
    
    return amadeus_spec


def setup_amadeus_gateway():
    """Setup Gateway for Amadeus API"""
    
    # Configuration
    region = "us-west-2"
    
    print("=" * 60)
    print("🚀 Setting up AgentCore Gateway for Amadeus API")
    print("=" * 60)
    print(f"Region: {region}\n")
    
    # Get API credentials from environment
    api_key = os.getenv("AMADEUS_API_KEY")
    api_secret = os.getenv("AMADEUS_API_SECRET")
    
    if not api_key or not api_secret:
        print("❌ Error: AMADEUS_API_KEY and AMADEUS_API_SECRET must be set in .env file")
        return None
    
    print(f"✓ API Key: {api_key[:10]}...{api_key[-4:]}")
    print(f"✓ API Secret: {api_secret[:10]}...{api_secret[-4:]}\n")
    
    # Initialize client
    client = GatewayClient(region_name=region)
    
    # Step 1: Create OAuth authorizer
    print("Step 1: Creating OAuth authorization server...")
    cognito_response = client.create_oauth_authorizer_with_cognito("AmadeusGateway")
    print("✓ Authorization server created\n")
    
    # Step 2: Create Gateway
    print("Step 2: Creating Gateway...")
    
    # Use timestamp to ensure unique name
    import time
    gateway_name = f"amadeus-travel-api-{int(time.time())}"
    
    gateway = client.create_mcp_gateway(
        name=gateway_name,
        role_arn=None,  # Will be created automatically
        authorizer_config=cognito_response["authorizer_config"],
        enable_semantic_search=True,
    )
    print(f"✓ Gateway created: {gateway['gatewayUrl']}\n")
    
    # Fix IAM permissions
    client.fix_iam_permissions(gateway)
    print("⏳ Waiting 30s for IAM propagation...")
    import time
    time.sleep(30)
    print("✓ IAM permissions configured\n")
    
    # Step 3: Create OpenAPI spec
    print("Step 3: Creating Amadeus OpenAPI specification...")
    amadeus_spec = create_amadeus_openapi_spec()
    print("✓ OpenAPI spec created\n")
    
    # Step 4: Add Amadeus API as target with OAuth credentials
    print("Step 4: Adding Amadeus API target with OAuth credentials...")
    
    # Note: Amadeus uses OAuth2 client credentials flow
    # The Gateway will handle token management automatically
    amadeus_target = client.create_mcp_gateway_target(
        gateway=gateway,
        name="amadeus-api",
        target_type="openApiSchema",
        target_payload={"inlinePayload": json.dumps(amadeus_spec)},
        credentials={
            "oauth2_provider_config": {
                "customOauth2ProviderConfig": {
                    "oauthDiscovery": {
                        "authorizationServerMetadata": {
                            "issuer": "https://test.api.amadeus.com",
                            "authorizationEndpoint": "https://test.api.amadeus.com/v1/security/oauth2/authorize",
                            "tokenEndpoint": "https://test.api.amadeus.com/v1/security/oauth2/token"
                        }
                    },
                    "clientId": api_key,
                    "clientSecret": api_secret
                }
            }
        }
    )
    print("✓ Amadeus API target added\n")
    
    # Step 5: Save configuration
    config = {
        "gateway_url": gateway["gatewayUrl"],
        "gateway_id": gateway["gatewayId"],
        "region": region,
        "client_info": cognito_response["client_info"],
        "target_id": amadeus_target["targetId"]
    }
    
    with open("amadeus_gateway_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("=" * 60)
    print("✅ Amadeus Gateway setup complete!")
    print(f"Gateway URL: {gateway['gatewayUrl']}")
    print(f"Gateway ID: {gateway['gatewayId']}")
    print(f"Target ID: {amadeus_target['targetId']}")
    print("\nConfiguration saved to: amadeus_gateway_config.json")
    print("\nNext steps:")
    print("1. Update agents to use Gateway instead of direct API calls")
    print("2. Remove environment variables from agent deployments")
    print("3. Test the Gateway with: python test_amadeus_gateway.py")
    print("=" * 60)
    
    return config


if __name__ == "__main__":
    setup_amadeus_gateway()
