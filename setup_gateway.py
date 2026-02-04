"""
Setup AgentCore Gateway for Umrah Trip Creator
Creates gateway with targets for flight, hotel, and visa APIs
"""

from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
import json
import logging
import uuid
import os
from dotenv import load_dotenv
import time

load_dotenv()

gateway_name = f"UmrahTrip-Gateway-{uuid.uuid4().hex[:8]}"
client = GatewayClient(region_name="us-west-2")
client.logger.setLevel(logging.INFO)

print("="*60)
print("Creating AgentCore Gateway for Umrah Trip Creator")
print("="*60)

# Create OAuth authorizer with Cognito
print("\n1. Creating OAuth authorization server...")
cognito_response = client.create_oauth_authorizer_with_cognito(gateway_name)
print("✅ Authorization server created")

# Create Gateway
print("\n2. Creating Gateway...")
gateway = client.create_mcp_gateway(
    name=gateway_name,
    role_arn=None,  # Auto-creates IAM role
    authorizer_config=cognito_response["authorizer_config"],
    enable_semantic_search=True,
)
print(f"✅ Gateway created: {gateway['gatewayUrl']}")

# Fix IAM permissions
print("\n3. Configuring IAM permissions...")
client.fix_iam_permissions(gateway)
print("⏳ Waiting 30s for IAM propagation...")
time.sleep(30)
print("✅ IAM permissions configured")

# Get access token
print("\n4. Getting access token...")
access_token = client.get_access_token_for_cognito(cognito_response["client_info"])
print("✅ Access token obtained")

# Add Amadeus API target (flights)
print("\n5. Adding Amadeus Flight API target...")
amadeus_api_key = os.getenv("AMADEUS_API_KEY")
amadeus_api_secret = os.getenv("AMADEUS_API_SECRET")

if amadeus_api_key and amadeus_api_secret:
    amadeus_schema = {
        "openApiSchema": {
            "uri": "https://test.api.amadeus.com/v2/shopping/flight-offers"
        }
    }

    amadeus_credentials = {
        "oauth2_provider_config": {
            "customOauth2ProviderConfig": {
                "oauthDiscovery": {
                    "discoveryUrl": "https://test.api.amadeus.com/.well-known/openid-configuration"
                },
                "clientId": amadeus_api_key,
                "clientSecret": amadeus_api_secret
            }
        },
        "scopes": []
    }

    try:
        amadeus_target = client.create_mcp_gateway_target(
            gateway=gateway,
            name="AmadeusFlightAPI",
            target_type="openApiSchema",
            target_payload=amadeus_schema,
            credentials=amadeus_credentials
        )
        print("✅ Amadeus Flight API target added")
    except Exception as e:
        print(f"⚠️  Amadeus API target failed: {e}")
        print("   You can add it later with proper credentials")
else:
    print("⚠️  Amadeus API credentials not found in .env")
    print("   Add AMADEUS_API_KEY and AMADEUS_API_SECRET to enable")

# Add Hotel API target (RapidAPI or Booking.com)
print("\n6. Adding Hotel API target...")
rapidapi_key = os.getenv("RAPIDAPI_KEY")
hotel_api_endpoint = os.getenv("HOTEL_API_ENDPOINT")
booking_api_key = os.getenv("BOOKING_API_KEY")

if rapidapi_key and hotel_api_endpoint:
    # Use RapidAPI
    hotel_schema = {
        "openApiSchema": {
            "uri": hotel_api_endpoint
        }
    }

    hotel_credentials = {
        "api_key": rapidapi_key,
        "credential_location": "header",
        "credential_parameter_name": "X-RapidAPI-Key"
    }

    try:
        hotel_target = client.create_mcp_gateway_target(
            gateway=gateway,
            name="RapidAPIHotelAPI",
            target_type="openApiSchema",
            target_payload=hotel_schema,
            credentials=hotel_credentials
        )
        print("✅ RapidAPI Hotel API target added")
    except Exception as e:
        print(f"⚠️  RapidAPI Hotel target failed: {e}")
        print("   You can add it later with proper credentials")
elif booking_api_key:
    # Use Booking.com direct
    booking_schema = {
        "openApiSchema": {
            "uri": "https://distribution-xml.booking.com/2.9/json"
        }
    }

    booking_credentials = {
        "api_key": booking_api_key,
        "credential_location": "header",
        "credential_parameter_name": "Authorization"
    }

    try:
        booking_target = client.create_mcp_gateway_target(
            gateway=gateway,
            name="BookingHotelAPI",
            target_type="openApiSchema",
            target_payload=booking_schema,
            credentials=booking_credentials
        )
        print("✅ Booking.com Hotel API target added")
    except Exception as e:
        print(f"⚠️  Booking.com API target failed: {e}")
        print("   You can add it later with proper credentials")
else:
    print("⚠️  Hotel API credentials not found in .env")
    print("   Add RAPIDAPI_KEY + HOTEL_API_ENDPOINT or BOOKING_API_KEY to enable")

# Add Lambda target for visa processing
print("\n7. Adding Visa Processing Lambda target...")
visa_schema = {
    "inlinePayload": [
        {
            "name": "check_visa_requirements",
            "description": "Check visa requirements for Saudi Arabia based on nationality",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "nationality": {
                        "type": "string",
                        "description": "Traveler's nationality"
                    },
                    "visa_type": {
                        "type": "string",
                        "enum": ["umrah", "tourist", "business"],
                        "description": "Type of visa"
                    }
                },
                "required": ["nationality", "visa_type"]
            }
        }
    ]
}

try:
    visa_target = client.create_mcp_gateway_target(
        gateway=gateway,
        name="VisaProcessingTool",
        target_type="lambda",
        target_payload={"toolSchema": visa_schema}
    )
    print("✅ Visa Processing Lambda target added")
except Exception as e:
    print(f"⚠️  Visa Lambda target failed: {e}")

# Save configuration
config = {
    "gateway_url": gateway["gatewayUrl"],
    "gateway_id": gateway["gatewayId"],
    "gateway_arn": gateway["gatewayArn"],
    "access_token": access_token,
    "cognito_user_pool_id": cognito_response["client_info"]["user_pool_id"],
    "cognito_client_id": cognito_response["client_info"]["client_id"],
    "cognito_client_secret": cognito_response["client_info"]["client_secret"]
}

with open("gateway_config.json", "w") as f:
    json.dump(config, f, indent=2)

print("\n" + "="*60)
print("✅ Gateway setup complete!")
print("="*60)
print(f"\nGateway URL: {gateway['gatewayUrl']}")
print(f"Gateway ID: {gateway['gatewayId']}")
print("\nConfiguration saved to: gateway_config.json")
print("\nAdd these to your .env file:")
print(f"GATEWAY_URL={gateway['gatewayUrl']}")
print(f"GATEWAY_ID={gateway['gatewayId']}")
print(f"GATEWAY_ACCESS_TOKEN={access_token}")
print(f"COGNITO_USER_POOL_ID={cognito_response['client_info']['user_pool_id']}")
print(f"COGNITO_CLIENT_ID={cognito_response['client_info']['client_id']}")
print(f"COGNITO_CLIENT_SECRET={cognito_response['client_info']['client_secret']}")
print("="*60)
