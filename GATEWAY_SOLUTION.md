# Gateway Solution for API Credentials

## Problem

Previously, we had to pass API credentials to each agent deployment using the `--env` flag:
```bash
agentcore deploy --env AMADEUS_API_KEY=xxx --env AMADEUS_API_SECRET=yyy
```

**Issues with this approach:**
1. **Repetitive** - Must redeploy every time with credentials
2. **Not scalable** - Each agent needs credentials
3. **Security risk** - Credentials in multiple places
4. **Hard to update** - Must redeploy all agents to change credentials
5. **Not persistent** - Credentials lost if config changes

## Solution: AgentCore Gateway

Use **AgentCore Gateway** to centralize API access. The Gateway:
- Stores API credentials securely
- Handles authentication automatically
- Exposes APIs as MCP tools
- Agents call Gateway instead of APIs directly
- **No credentials needed in agents!**

## Architecture

### Before (Direct API Calls):
```
Agent → Amadeus API (needs credentials)
  ↓
Requires: AMADEUS_API_KEY, AMADEUS_API_SECRET in agent
```

### After (Gateway):
```
Agent → Gateway → Amadeus API
  ↓         ↓
  OAuth   Stores credentials
  token   Handles auth
```

## Benefits

1. **✅ Centralized Credentials** - Stored once in Gateway
2. **✅ No Agent Redeployment** - Update credentials in Gateway only
3. **✅ Better Security** - Credentials never exposed to agents
4. **✅ Easier Management** - One place to manage all API access
5. **✅ Automatic Token Management** - Gateway handles OAuth refresh
6. **✅ Audit Trail** - Gateway logs all API calls
7. **✅ Rate Limiting** - Gateway can enforce limits
8. **✅ Multiple APIs** - Add more APIs without changing agents

## Setup Instructions

### Step 1: Create the Gateway

Run the setup script:
```bash
python3 setup_amadeus_gateway.py
```

This will:
1. Create OAuth authorization server (Cognito)
2. Create AgentCore Gateway
3. Add Amadeus API as OpenAPI target
4. Configure OAuth credentials for Amadeus
5. Save configuration to `amadeus_gateway_config.json`

**What it creates:**
- Gateway URL: `https://gateway-id.gateway.bedrock-agentcore.us-west-2.amazonaws.com/mcp`
- OAuth client credentials for agent access
- Amadeus API target with stored credentials

### Step 2: Test the Gateway

Verify the Gateway works:
```bash
python3 test_amadeus_gateway.py
```

This will:
1. Get OAuth token for Gateway access
2. List available tools (searchFlights, searchHotelsByCity, searchHotelsByLocation)
3. Test flight search
4. Test hotel search

### Step 3: Update Agents to Use Gateway

Instead of calling Amadeus API directly, agents will call Gateway tools.

**Option A: Use MCP Client in Agents**

Update agent code to use MCP client:
```python
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamablehttp_client

# Load gateway config
with open("amadeus_gateway_config.json") as f:
    config = json.load(f)

# Get access token
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
client = GatewayClient(region_name=config["region"])
access_token = client.get_access_token_for_cognito(config["client_info"])

# Create MCP client
def create_transport(mcp_url, token):
    return streamablehttp_client(mcp_url, headers={"Authorization": f"Bearer {token}"})

mcp_client = MCPClient(lambda: create_transport(config["gateway_url"], access_token))

# Use in agent
with mcp_client:
    tools = mcp_client.list_tools_sync()
    agent = Agent(model=model, tools=tools)
```

**Option B: Create Gateway Tool Wrappers**

Create Python functions that call Gateway tools:
```python
import httpx
import json

async def search_flights_via_gateway(origin, destination, departure_date, return_date, adults=2):
    """Search flights through Gateway"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            gateway_url,
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "searchFlights",
                    "arguments": {
                        "originLocationCode": origin,
                        "destinationLocationCode": destination,
                        "departureDate": departure_date,
                        "returnDate": return_date,
                        "adults": adults
                    }
                }
            }
        )
        return response.json()
```

### Step 4: Redeploy Agents (Without Credentials!)

Now you can deploy agents WITHOUT environment variables:
```bash
cd agents/flight_agent
agentcore deploy  # No --env flags needed!

cd agents/hotel_agent
agentcore deploy  # No --env flags needed!
```

## Gateway Configuration

The Gateway is configured with:

### OpenAPI Specification
Defines the Amadeus API endpoints:
- `/v2/shopping/flight-offers` - Flight search
- `/v1/reference-data/locations/hotels/by-city` - Hotel search by city
- `/v1/reference-data/locations/hotels/by-geocode` - Hotel search by location

### OAuth2 Credentials
Stored in Gateway target configuration:
```json
{
  "oauth2_provider_config": {
    "customOauth2ProviderConfig": {
      "oauthDiscovery": {
        "authorizationServerMetadata": {
          "tokenEndpoint": "https://test.api.amadeus.com/v1/security/oauth2/token"
        }
      },
      "clientId": "AMADEUS_API_KEY",
      "clientSecret": "AMADEUS_API_SECRET"
    }
  }
}
```

The Gateway automatically:
- Obtains OAuth tokens from Amadeus
- Refreshes tokens when expired
- Adds tokens to API requests
- Handles authentication errors

## Available Tools

After setup, agents can use these tools through the Gateway:

### 1. searchFlights
Search for flight offers with real-time prices.

**Parameters:**
- `originLocationCode` (required): IATA airport code (e.g., "JFK")
- `destinationLocationCode` (required): IATA airport code (e.g., "JED")
- `departureDate` (required): Date in YYYY-MM-DD format
- `returnDate` (optional): Return date in YYYY-MM-DD format
- `adults` (optional): Number of passengers (default: 1)
- `travelClass` (optional): ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST
- `nonStop` (optional): true for direct flights only
- `max` (optional): Maximum results (default: 5)

### 2. searchHotelsByCity
Find hotels in a specific city.

**Parameters:**
- `cityCode` (required): IATA city code (e.g., "MEC" for Makkah)
- `radius` (optional): Search radius (default: 5)
- `radiusUnit` (optional): KM or MILE (default: KM)

### 3. searchHotelsByLocation
Find hotels near specific coordinates (e.g., near Haram).

**Parameters:**
- `latitude` (required): Latitude (e.g., 21.4225 for Masjid al-Haram)
- `longitude` (required): Longitude (e.g., 39.8262 for Masjid al-Haram)
- `radius` (optional): Search radius (default: 2)
- `radiusUnit` (optional): KM or MILE (default: KM)

## Updating Credentials

To update API credentials:

1. **Update Gateway Target:**
```python
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
import json

with open("amadeus_gateway_config.json") as f:
    config = json.load(f)

client = GatewayClient(region_name=config["region"])

# Update target with new credentials
client.client.update_gateway_target(
    gatewayIdentifier=config["gateway_id"],
    targetId=config["target_id"],
    credentials={
        "oauth2_provider_config": {
            "customOauth2ProviderConfig": {
                "clientId": "NEW_API_KEY",
                "clientSecret": "NEW_API_SECRET",
                # ... rest of config
            }
        }
    }
)
```

2. **No agent redeployment needed!** The Gateway handles the new credentials automatically.

## Adding More APIs

To add more external APIs (e.g., weather, currency exchange):

1. Create OpenAPI spec for the API
2. Add as new Gateway target
3. Configure credentials (API key, OAuth, etc.)
4. Agents automatically get access to new tools

Example:
```python
weather_spec = {
    "openapi": "3.0.0",
    "info": {"title": "Weather API", "version": "1.0.0"},
    "servers": [{"url": "https://api.weather.com"}],
    # ... paths, etc.
}

weather_target = client.create_mcp_gateway_target(
    gateway=gateway,
    name="weather-api",
    target_type="openApiSchema",
    target_payload={"inlinePayload": json.dumps(weather_spec)},
    credentials={
        "api_key": "WEATHER_API_KEY",
        "credential_location": "HEADER",
        "credential_parameter_name": "X-API-Key"
    }
)
```

## Security Features

### Gateway Security:
- **OAuth 2.0 Authentication** - Agents must authenticate to use Gateway
- **Cognito User Pool** - Manages client credentials
- **Token Expiration** - Tokens expire after 1 hour
- **IAM Permissions** - Gateway has minimal required permissions
- **Encrypted Storage** - Credentials encrypted at rest
- **Audit Logs** - All Gateway calls logged to CloudWatch

### Best Practices:
1. **Rotate credentials regularly** - Update in Gateway only
2. **Use least privilege** - Gateway role has minimal permissions
3. **Monitor usage** - Check CloudWatch logs for anomalies
4. **Set rate limits** - Prevent abuse
5. **Use VPC endpoints** - For private network access

## Monitoring

### CloudWatch Logs:
```bash
# Gateway logs
aws logs tail /aws/bedrock-agentcore/gateways/GATEWAY_ID --follow

# View recent errors
aws logs filter-pattern /aws/bedrock-agentcore/gateways/GATEWAY_ID \
  --filter-pattern "ERROR" \
  --since 1h
```

### Metrics to Monitor:
- Request count
- Error rate
- Latency
- Token refresh failures
- API quota usage

## Cleanup

To remove the Gateway:
```python
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
import json

with open("amadeus_gateway_config.json") as f:
    config = json.load(f)

client = GatewayClient(region_name=config["region"])
client.cleanup_gateway(config["gateway_id"], config["client_info"])
print("✅ Gateway deleted")
```

## Troubleshooting

### Gateway not responding:
- Wait 30-60 seconds after creation for DNS propagation
- Check IAM permissions
- Verify OAuth token is valid

### Authentication errors:
- Get new access token (expires after 1 hour)
- Check client ID and secret in config
- Verify Cognito user pool exists

### API errors:
- Check Amadeus API credentials in Gateway
- Verify API quota not exceeded
- Check CloudWatch logs for details

### Tools not appearing:
- Verify target was created successfully
- Check OpenAPI spec is valid
- List tools with `tools/list` method

## Cost Considerations

### Gateway Costs:
- **Gateway** - $0.10 per 1M requests
- **Cognito** - First 50,000 MAUs free, then $0.0055/MAU
- **CloudWatch Logs** - $0.50/GB ingested
- **Data Transfer** - Standard AWS rates

### Amadeus API Costs:
- **Test API** - Free (rate limited)
- **Production API** - Pay per transaction

## Migration Path

### Phase 1: Setup Gateway (Current)
1. ✅ Create Gateway
2. ✅ Add Amadeus API target
3. ✅ Test Gateway

### Phase 2: Update Agents (Next)
1. Modify agents to use Gateway tools
2. Remove direct API calls
3. Redeploy agents without credentials
4. Test end-to-end

### Phase 3: Production (Future)
1. Switch to Amadeus production API
2. Add monitoring and alerts
3. Implement rate limiting
4. Set up VPC endpoints
5. Add more APIs as needed

## Files Created

- `setup_amadeus_gateway.py` - Gateway setup script
- `test_amadeus_gateway.py` - Gateway testing script
- `amadeus_gateway_config.json` - Gateway configuration (created by setup)
- `GATEWAY_SOLUTION.md` - This documentation

## Next Steps

1. **Run setup:** `python3 setup_amadeus_gateway.py`
2. **Test Gateway:** `python3 test_amadeus_gateway.py`
3. **Update agents** to use Gateway tools
4. **Redeploy agents** without credentials
5. **Test complete flow** through frontend
6. **Monitor** Gateway usage in CloudWatch

## Summary

The Gateway solution provides:
- ✅ **Centralized credential management**
- ✅ **No credentials in agents**
- ✅ **Easy updates** (no redeployment)
- ✅ **Better security**
- ✅ **Automatic token management**
- ✅ **Scalable architecture**
- ✅ **Production-ready**

This is the **recommended approach** for production deployments!
