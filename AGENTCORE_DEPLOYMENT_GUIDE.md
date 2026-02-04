# AgentCore Deployment Guide for Umrah Trip Creator

This guide walks you through deploying your multi-agent Umrah Trip Creator to AWS AgentCore with Runtime, Memory, Identity, and Gateway for real-world API integration.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                   Streamlit Frontend (S3/CloudFront)            │
│                   + Cognito Authentication                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              AgentCore Runtime - Orchestrator Agent             │
│              + AgentCore Memory (STM + LTM)                     │
│              + AgentCore Identity (Cognito OAuth)               │
└─────┬──────────┬──────────┬──────────┬────────────────────────┘
      │          │          │          │
      │ A2A      │ A2A      │ A2A      │ A2A
      │          │          │          │
      ▼          ▼          ▼          ▼
┌──────────┐ ┌────────┐ ┌────────┐ ┌──────────────┐
│ Flight   │ │ Hotel  │ │ Visa   │ │ Itinerary    │
│ Agent    │ │ Agent  │ │ Agent  │ │ Agent        │
│ Runtime  │ │Runtime │ │Runtime │ │  Runtime     │
└────┬─────┘ └───┬────┘ └───┬────┘ └──────┬───────┘
     │           │          │             │
     ▼           ▼          ▼             ▼
┌─────────────────────────────────────────────────┐
│         AgentCore Gateway (MCP)                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Amadeus  │ │ Booking  │ │  Visa    │       │
│  │   API    │ │   API    │ │   API    │       │
│  └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────┘
```

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured: `aws configure`
3. **Python 3.10+** installed
4. **API Keys**:
   - Amadeus API credentials (for flights)
   - Booking.com API key (for hotels)
   - OpenAI API key
   - Anthropic API key

## Step 1: Install AgentCore CLI

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install AgentCore toolkit
pip install bedrock-agentcore-starter-toolkit bedrock-agentcore strands-agents

# Verify installation
agentcore --version
```

## Step 2: Set Up AgentCore Memory

Create memory resources for conversation persistence and user preferences.

### Create Memory Setup Script

Create `setup_memory.py`:

```python
"""
Setup AgentCore Memory for Umrah Trip Creator
Creates both short-term and long-term memory resources
"""

from bedrock_agentcore.memory import MemoryClient
import uuid

client = MemoryClient(region_name='us-west-2')

print("Creating memory resources for Umrah Trip Creator...\n")

# Short-Term Memory (STM) - for conversation within sessions
stm = client.create_memory_and_wait(
    name=f"UmrahTrip_STM_{uuid.uuid4().hex[:8]}",
    strategies=[],  # No extraction strategies
    event_expiry_days=7
)
print(f"✅ STM Memory Created: {stm['id']}")
print("   - Stores conversation within sessions")
print("   - 7-day retention\n")

# Long-Term Memory (LTM) - for user preferences across sessions
ltm = client.create_memory_and_wait(
    name=f"UmrahTrip_LTM_{uuid.uuid4().hex[:8]}",
    strategies=[
        # Extract user travel preferences
        {"userPreferenceMemoryStrategy": {
            "name": "travel_preferences",
            "namespaces": [
                "/user/preferences/travel/",
                "/user/preferences/hotel/",
                "/user/preferences/budget/"
            ]
        }},
        # Extract user facts (nationality, family size, etc.)
        {"semanticMemoryStrategy": {
            "name": "user_facts",
            "namespaces": [
                "/user/facts/personal/",
                "/user/facts/travel_history/"
            ]
        }}
    ],
    event_expiry_days=90  # Keep for 90 days
)
print(f"✅ LTM Memory Created: {ltm['id']}")
print("   - Extracts preferences and facts")
print("   - 90-day retention")
print("   - Cross-session memory\n")

print("="*60)
print("Save these IDs to your .env file:")
print(f"MEMORY_STM_ID={stm['id']}")
print(f"MEMORY_LTM_ID={ltm['id']}")
print("="*60)
```

Run the script:

```bash
python setup_memory.py
```

Save the memory IDs to your `.env` file.

## Step 3: Set Up AgentCore Gateway for Real-World APIs

Create gateway with targets for Amadeus (flights), Booking.com (hotels), and visa APIs.

### Create Gateway Setup Script

Create `setup_gateway.py`:

```python
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

load_dotenv()

gateway_name = f"UmrahTrip_Gateway_{uuid.uuid4().hex[:8]}"
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
import time
time.sleep(30)
print("✅ IAM permissions configured")

# Get access token
print("\n4. Getting access token...")
access_token = client.get_access_token_for_cognito(cognito_response["client_info"])
print("✅ Access token obtained")

# Add Amadeus API target (flights)
print("\n5. Adding Amadeus Flight API target...")
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
            "clientId": os.getenv("AMADEUS_API_KEY"),
            "clientSecret": os.getenv("AMADEUS_API_SECRET")
        }
    },
    "scopes": []
}

amadeus_target = client.create_mcp_gateway_target(
    gateway=gateway,
    name="AmadeusFlightAPI",
    target_type="openApiSchema",
    target_payload=amadeus_schema,
    credentials=amadeus_credentials
)
print("✅ Amadeus Flight API target added")

# Add Booking.com API target (hotels)
print("\n6. Adding Booking.com Hotel API target...")
booking_schema = {
    "openApiSchema": {
        "uri": "https://distribution-xml.booking.com/2.9/json"
    }
}

booking_credentials = {
    "api_key": os.getenv("BOOKING_API_KEY"),
    "credential_location": "header",
    "credential_parameter_name": "Authorization"
}

booking_target = client.create_mcp_gateway_target(
    gateway=gateway,
    name="BookingHotelAPI",
    target_type="openApiSchema",
    target_payload=booking_schema,
    credentials=booking_credentials
)
print("✅ Booking.com Hotel API target added")

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

visa_target = client.create_mcp_gateway_target(
    gateway=gateway,
    name="VisaProcessingTool",
    target_type="lambda",
    target_payload={"toolSchema": visa_schema}
)
print("✅ Visa Processing Lambda target added")

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
print(f"COGNITO_USER_POOL_ID={cognito_response['client_info']['user_pool_id']}")
print(f"COGNITO_CLIENT_ID={cognito_response['client_info']['client_id']}")
print("="*60)
```

Run the script:

```bash
python setup_gateway.py
```

Save the gateway configuration to your `.env` file.

## Step 4: Prepare Agents for AgentCore Runtime

Each agent needs to be wrapped with `BedrockAgentCoreApp` for deployment.

### Update Orchestrator Agent

Create `agents/orchestrator/orchestrator_runtime.py`:


```python
"""
Orchestrator Agent for AgentCore Runtime
Coordinates all specialized agents with Memory and Gateway integration
"""

import os
import json
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from bedrock_agentcore.memory import MemoryClient
from strands import Agent
from strands.hooks import AgentInitializedEvent, HookProvider, MessageAddedEvent
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
import asyncio

# Initialize AgentCore app
app = BedrockAgentCoreApp()

# Memory client
memory_client = MemoryClient(region_name='us-west-2')
MEMORY_ID = os.getenv('MEMORY_LTM_ID')  # Use long-term memory

# Gateway configuration
GATEWAY_URL = os.getenv('GATEWAY_URL')
GATEWAY_TOKEN = os.getenv('GATEWAY_ACCESS_TOKEN')


class MemoryHook(HookProvider):
    """Handles memory operations for conversation persistence"""
    
    def on_agent_initialized(self, event):
        """Load conversation history when agent starts"""
        if not MEMORY_ID:
            return
        
        session_id = event.agent.state.get("session_id", "default")
        user_id = event.agent.state.get("user_id", "anonymous")
        
        # Get last 5 conversation turns
        turns = memory_client.get_last_k_turns(
            memory_id=MEMORY_ID,
            actor_id=user_id,
            session_id=session_id,
            k=5
        )
        
        if turns:
            context = "\n".join([
                f"{m['role']}: {m['content']['text']}"
                for t in turns for m in t
            ])
            event.agent.system_prompt += f"\n\nPrevious conversation:\n{context}"
    
    def on_message_added(self, event):
        """Save messages to memory"""
        if not MEMORY_ID:
            return
        
        msg = event.agent.messages[-1]
        session_id = event.agent.state.get("session_id", "default")
        user_id = event.agent.state.get("user_id", "anonymous")
        
        memory_client.create_event(
            memory_id=MEMORY_ID,
            actor_id=user_id,
            session_id=session_id,
            messages=[(str(msg["content"]), msg["role"])]
        )
    
    def register_hooks(self, registry):
        registry.add_callback(AgentInitializedEvent, self.on_agent_initialized)
        registry.add_callback(MessageAddedEvent, self.on_message_added)


async def get_gateway_tools():
    """Get tools from AgentCore Gateway"""
    if not GATEWAY_URL or not GATEWAY_TOKEN:
        return []
    
    try:
        headers = {"Authorization": f"Bearer {GATEWAY_TOKEN}"}
        
        async with streamablehttp_client(GATEWAY_URL, headers=headers) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools_result = await session.list_tools()
                return tools_result.tools
    except Exception as e:
        print(f"Gateway error: {e}")
        return []


# Create orchestrator agent
orchestrator = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    system_prompt="""You are the main Umrah Trip Coordinator.
    
Your role:
1. Collect user requirements (dates, travelers, preferences, budget)
2. Coordinate with specialized agents via A2A protocol:
   - Flight Agent: Search flights to Jeddah/Medina
   - Hotel Agent: Find hotels in Makkah and Madinah
   - Visa Agent: Check visa requirements
   - Itinerary Agent: Create Umrah schedule
3. Present comprehensive trip options
4. Handle booking confirmations

You have access to:
- Memory: Remember user preferences across sessions
- Gateway Tools: Access real-world APIs for flights, hotels, visas

Be helpful, patient, and ensure all Islamic requirements are met.""",
    hooks=[MemoryHook()] if MEMORY_ID else [],
    state={"session_id": "default", "user_id": "anonymous"}
)


@app.entrypoint
def invoke(payload, context):
    """Main entry point for orchestrator agent"""
    
    # Set session and user context
    if hasattr(context, 'session_id'):
        orchestrator.state.set("session_id", context.session_id)
    if hasattr(context, 'user_id'):
        orchestrator.state.set("user_id", context.user_id)
    
    # Load gateway tools
    try:
        tools = asyncio.run(get_gateway_tools())
        if tools:
            orchestrator.tools = tools
    except Exception as e:
        print(f"Error loading gateway tools: {e}")
    
    # Process user message
    user_message = payload.get("prompt", "Hello")
    response = orchestrator(user_message)
    
    return {
        "result": response.message['content'][0]['text'],
        "session_id": orchestrator.state.get("session_id"),
        "user_id": orchestrator.state.get("user_id")
    }


if __name__ == "__main__":
    app.run()
```

Create `agents/orchestrator/requirements.txt`:

```
bedrock-agentcore
strands-agents
mcp
```

### Update Flight Agent

Create `agents/flight_agent/flight_runtime.py`:

```python
"""
Flight Agent for AgentCore Runtime
Searches flights using Amadeus API via Gateway
"""

import os
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
import asyncio

app = BedrockAgentCoreApp()

GATEWAY_URL = os.getenv('GATEWAY_URL')
GATEWAY_TOKEN = os.getenv('GATEWAY_ACCESS_TOKEN')


async def get_flight_tools():
    """Get Amadeus flight tools from gateway"""
    if not GATEWAY_URL or not GATEWAY_TOKEN:
        return []
    
    try:
        headers = {"Authorization": f"Bearer {GATEWAY_TOKEN}"}
        
        async with streamablehttp_client(GATEWAY_URL, headers=headers) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools_result = await session.list_tools()
                # Filter for Amadeus flight tools
                return [t for t in tools_result.tools if 'flight' in t.name.lower()]
    except Exception as e:
        print(f"Gateway error: {e}")
        return []


flight_agent = Agent(
    model="gpt-4o-2024-08-06",
    system_prompt="""You are a Flight Search Specialist for Umrah trips.

Your responsibilities:
1. Search flights to Jeddah (JED) or Medina (MED) from user's departure city
2. Consider:
   - Direct vs connecting flights
   - Departure/arrival times suitable for Umrah
   - Baggage allowances for pilgrims
   - Cabin class preferences
   - Budget constraints
3. Present multiple options with clear comparisons
4. Recommend best value options

Use the Amadeus API tools to search real flight data.""",
    state={}
)


@app.entrypoint
def invoke(payload, context):
    """Flight agent entry point"""
    
    # Load flight tools from gateway
    try:
        tools = asyncio.run(get_flight_tools())
        if tools:
            flight_agent.tools = tools
    except Exception as e:
        print(f"Error loading flight tools: {e}")
    
    # Process request
    request = payload.get("prompt", "")
    response = flight_agent(request)
    
    return {
        "result": response.message['content'][0]['text']
    }


if __name__ == "__main__":
    app.run()
```

Create `agents/flight_agent/requirements.txt`:

```
bedrock-agentcore
openai
mcp
```

### Update Hotel Agent

Create `agents/hotel_agent/hotel_runtime.py`:

```python
"""
Hotel Agent for AgentCore Runtime
Searches hotels using Booking.com API via Gateway
"""

import os
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
import asyncio

app = BedrockAgentCoreApp()

GATEWAY_URL = os.getenv('GATEWAY_URL')
GATEWAY_TOKEN = os.getenv('GATEWAY_ACCESS_TOKEN')


async def get_hotel_tools():
    """Get Booking.com hotel tools from gateway"""
    if not GATEWAY_URL or not GATEWAY_TOKEN:
        return []
    
    try:
        headers = {"Authorization": f"Bearer {GATEWAY_TOKEN}"}
        
        async with streamablehttp_client(GATEWAY_URL, headers=headers) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools_result = await session.list_tools()
                # Filter for hotel/booking tools
                return [t for t in tools_result.tools if 'hotel' in t.name.lower() or 'booking' in t.name.lower()]
    except Exception as e:
        print(f"Gateway error: {e}")
        return []


hotel_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    system_prompt="""You are a Hotel Booking Specialist for Umrah trips.

Your responsibilities:
1. Search hotels in Makkah and Madinah
2. Prioritize:
   - Proximity to Haram (walking distance preferred)
   - Star rating matching user preferences
   - Amenities (WiFi, breakfast, elevator, prayer facilities)
   - Haram view options
   - Group booking availability
3. Present options for both cities
4. Consider budget constraints

Use the Booking.com API tools to search real hotel data.""",
    state={}
)


@app.entrypoint
def invoke(payload, context):
    """Hotel agent entry point"""
    
    # Load hotel tools from gateway
    try:
        tools = asyncio.run(get_hotel_tools())
        if tools:
            hotel_agent.tools = tools
    except Exception as e:
        print(f"Error loading hotel tools: {e}")
    
    # Process request
    request = payload.get("prompt", "")
    response = hotel_agent(request)
    
    return {
        "result": response.message['content'][0]['text']
    }


if __name__ == "__main__":
    app.run()
```

Create `agents/hotel_agent/requirements.txt`:

```
bedrock-agentcore
strands-agents
mcp
```

### Update Visa Agent

Create `agents/visa_agent/visa_runtime.py`:

```python
"""
Visa Agent for AgentCore Runtime
Checks visa requirements using Gateway Lambda function
"""

import os
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
import asyncio

app = BedrockAgentCoreApp()

GATEWAY_URL = os.getenv('GATEWAY_URL')
GATEWAY_TOKEN = os.getenv('GATEWAY_ACCESS_TOKEN')


async def get_visa_tools():
    """Get visa processing tools from gateway"""
    if not GATEWAY_URL or not GATEWAY_TOKEN:
        return []
    
    try:
        headers = {"Authorization": f"Bearer {GATEWAY_TOKEN}"}
        
        async with streamablehttp_client(GATEWAY_URL, headers=headers) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools_result = await session.list_tools()
                # Filter for visa tools
                return [t for t in tools_result.tools if 'visa' in t.name.lower()]
    except Exception as e:
        print(f"Gateway error: {e}")
        return []


visa_agent = Agent(
    model="gpt-4o-2024-08-06",
    system_prompt="""You are a Visa Requirements Specialist for Saudi Arabia Umrah visas.

Your responsibilities:
1. Check visa requirements based on traveler nationality
2. Provide:
   - Visa type (Umrah visa, e-visa, visa on arrival)
   - Required documents
   - Application process steps
   - Processing time
   - Visa fees
   - Validity period
3. Special considerations:
   - Vaccination requirements (Meningitis)
   - Mahram requirements for women
   - Age restrictions
   - Previous visa history

Use the visa processing tools to get accurate, up-to-date information.""",
    state={}
)


@app.entrypoint
def invoke(payload, context):
    """Visa agent entry point"""
    
    # Load visa tools from gateway
    try:
        tools = asyncio.run(get_visa_tools())
        if tools:
            visa_agent.tools = tools
    except Exception as e:
        print(f"Error loading visa tools: {e}")
    
    # Process request
    request = payload.get("prompt", "")
    response = visa_agent(request)
    
    return {
        "result": response.message['content'][0]['text']
    }


if __name__ == "__main__":
    app.run()
```

Create `agents/visa_agent/requirements.txt`:

```
bedrock-agentcore
openai
mcp
```

### Update Itinerary Agent

Create `agents/itinerary_agent/itinerary_runtime.py`:

```python
"""
Itinerary Agent for AgentCore Runtime
Creates detailed Umrah ritual schedules
"""

import os
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent

app = BedrockAgentCoreApp()


itinerary_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    system_prompt="""You are an Umrah Itinerary Planning Specialist.

Your responsibilities:
1. Create detailed day-by-day schedules for Umrah trips
2. Include:
   - Umrah ritual steps (Ihram, Tawaf, Sa'i, Halq/Taqsir)
   - Prayer times at Haram
   - Ziyarat (historical sites) visits
   - Rest periods
   - Meal times
   - Transportation between cities
3. Consider:
   - Trip duration
   - Traveler ages and physical abilities
   - First-time vs experienced pilgrims
   - Crowd management (best times to visit)
4. Provide Islamic guidance for each ritual

Create practical, realistic schedules that balance worship with rest.""",
    state={}
)


@app.entrypoint
def invoke(payload, context):
    """Itinerary agent entry point"""
    
    # Process request
    request = payload.get("prompt", "")
    response = itinerary_agent(request)
    
    return {
        "result": response.message['content'][0]['text']
    }


if __name__ == "__main__":
    app.run()
```

Create `agents/itinerary_agent/requirements.txt`:

```
bedrock-agentcore
strands-agents
```

## Step 5: Deploy Agents to AgentCore Runtime

Deploy each agent to AgentCore Runtime with memory and gateway configuration.

### Deploy Orchestrator Agent

```bash
cd agents/orchestrator

# Configure agent
agentcore configure \
  --entrypoint orchestrator_runtime.py \
  --name umrah-orchestrator \
  --runtime PYTHON_3_12 \
  --requirements-file requirements.txt \
  --protocol A2A \
  --non-interactive

# Deploy with environment variables
agentcore launch \
  --agent umrah-orchestrator \
  --env MEMORY_LTM_ID=$MEMORY_LTM_ID \
  --env GATEWAY_URL=$GATEWAY_URL \
  --env GATEWAY_ACCESS_TOKEN=$GATEWAY_ACCESS_TOKEN

# Test
agentcore invoke '{"prompt": "I want to plan an Umrah trip for 2 people from New York"}' \
  --agent umrah-orchestrator
```

### Deploy Flight Agent

```bash
cd agents/flight_agent

agentcore configure \
  --entrypoint flight_runtime.py \
  --name umrah-flight-agent \
  --runtime PYTHON_3_12 \
  --requirements-file requirements.txt \
  --protocol A2A \
  --non-interactive

agentcore launch \
  --agent umrah-flight-agent \
  --env GATEWAY_URL=$GATEWAY_URL \
  --env GATEWAY_ACCESS_TOKEN=$GATEWAY_ACCESS_TOKEN \
  --env OPENAI_API_KEY=$OPENAI_API_KEY

# Test
agentcore invoke '{"prompt": "Search flights from JFK to JED for March 15-25, 2026"}' \
  --agent umrah-flight-agent
```

### Deploy Hotel Agent

```bash
cd agents/hotel_agent

agentcore configure \
  --entrypoint hotel_runtime.py \
  --name umrah-hotel-agent \
  --runtime PYTHON_3_12 \
  --requirements-file requirements.txt \
  --protocol A2A \
  --non-interactive

agentcore launch \
  --agent umrah-hotel-agent \
  --env GATEWAY_URL=$GATEWAY_URL \
  --env GATEWAY_ACCESS_TOKEN=$GATEWAY_ACCESS_TOKEN

# Test
agentcore invoke '{"prompt": "Find 4-star hotels in Makkah within walking distance of Haram"}' \
  --agent umrah-hotel-agent
```

### Deploy Visa Agent

```bash
cd agents/visa_agent

agentcore configure \
  --entrypoint visa_runtime.py \
  --name umrah-visa-agent \
  --runtime PYTHON_3_12 \
  --requirements-file requirements.txt \
  --protocol A2A \
  --non-interactive

agentcore launch \
  --agent umrah-visa-agent \
  --env GATEWAY_URL=$GATEWAY_URL \
  --env GATEWAY_ACCESS_TOKEN=$GATEWAY_ACCESS_TOKEN \
  --env OPENAI_API_KEY=$OPENAI_API_KEY

# Test
agentcore invoke '{"prompt": "Check visa requirements for US citizens for Umrah"}' \
  --agent umrah-visa-agent
```

### Deploy Itinerary Agent

```bash
cd agents/itinerary_agent

agentcore configure \
  --entrypoint itinerary_runtime.py \
  --name umrah-itinerary-agent \
  --runtime PYTHON_3_12 \
  --requirements-file requirements.txt \
  --protocol A2A \
  --non-interactive

agentcore launch \
  --agent umrah-itinerary-agent

# Test
agentcore invoke '{"prompt": "Create a 10-day Umrah itinerary for first-time pilgrims"}' \
  --agent umrah-itinerary-agent
```

## Step 6: Update Frontend for Production

Update the Streamlit frontend to use deployed agents instead of mock data.

### Update `frontend/streamlit_app.py`

Replace the mock agent calls with real AgentCore Runtime invocations:

```python
import boto3
import json

# Initialize AgentCore Runtime client
agentcore_client = boto3.client('bedrock-agentcore-runtime', region_name='us-west-2')

def invoke_orchestrator(prompt, session_id, user_id):
    """Invoke orchestrator agent on AgentCore Runtime"""
    response = agentcore_client.invoke_agent(
        agentName='umrah-orchestrator',
        sessionId=session_id,
        userId=user_id,
        inputText=prompt
    )
    return response['output']

# Update step_review_generate() function
def step_review_generate():
    """Step 5: Review and generate trip plan"""
    st.markdown('<h2 class="step-header">📋 Step 5: Review & Generate Plan</h2>', unsafe_allow_html=True)
    
    # ... existing review code ...
    
    if st.button("🚀 Generate My Umrah Trip Plan", type="primary", use_container_width=True):
        with st.spinner("🤖 AI Agents are working on your perfect Umrah trip..."):
            
            # Get session and user info
            session_id = st.session_state.get('session_id', str(uuid.uuid4()))
            user_id = st.session_state.get('user_email', 'anonymous')
            
            # Prepare request
            user_requirements = json.dumps(st.session_state.user_data)
            prompt = f"Plan an Umrah trip with these requirements: {user_requirements}"
            
            # Invoke orchestrator agent
            try:
                result = invoke_orchestrator(prompt, session_id, user_id)
                st.session_state.trip_plan = json.loads(result)
                st.session_state.step = 6
                st.success("✅ Trip plan generated successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error generating trip plan: {e}")
```

## Step 7: Deploy Frontend to S3/CloudFront

### Create S3 Bucket and CloudFront Distribution

```bash
# Create S3 bucket for frontend
aws s3 mb s3://umrah-trip-creator-frontend-${AWS_ACCOUNT_ID}

# Enable static website hosting
aws s3 website s3://umrah-trip-creator-frontend-${AWS_ACCOUNT_ID} \
  --index-document index.html

# Create CloudFront distribution (optional, for HTTPS and CDN)
aws cloudfront create-distribution \
  --origin-domain-name umrah-trip-creator-frontend-${AWS_ACCOUNT_ID}.s3.amazonaws.com \
  --default-root-object index.html
```

### Package and Deploy Frontend

```bash
# Install Streamlit dependencies
cd frontend
pip install -r requirements.txt

# Deploy to S3
aws s3 sync . s3://umrah-trip-creator-frontend-${AWS_ACCOUNT_ID}/ \
  --exclude "*.pyc" \
  --exclude "__pycache__/*"
```

## Step 8: Monitor and Test

### Check Agent Status

```bash
# Check all agents
agentcore status --agent umrah-orchestrator --verbose
agentcore status --agent umrah-flight-agent --verbose
agentcore status --agent umrah-hotel-agent --verbose
agentcore status --agent umrah-visa-agent --verbose
agentcore status --agent umrah-itinerary-agent --verbose
```

### View Logs

```bash
# View orchestrator logs
aws logs tail /aws/bedrock-agentcore/umrah-orchestrator --follow

# View flight agent logs
aws logs tail /aws/bedrock-agentcore/umrah-flight-agent --follow
```

### Test End-to-End

```bash
# Test complete workflow
agentcore invoke '{
  "prompt": "Plan an Umrah trip for 2 people from New York, departing March 15, 2026, returning March 25, 2026. Budget $6000 total. Need 4-star hotels walking distance from Haram."
}' --agent umrah-orchestrator --session-id test-session-001
```

## Step 9: Clean Up (Optional)

To remove all resources:

```bash
# Destroy agents
agentcore destroy --agent umrah-orchestrator --force
agentcore destroy --agent umrah-flight-agent --force
agentcore destroy --agent umrah-hotel-agent --force
agentcore destroy --agent umrah-visa-agent --force
agentcore destroy --agent umrah-itinerary-agent --force

# Delete gateway
agentcore gateway delete-mcp-gateway --name <gateway-name> --force

# Delete memory resources
python -c "
from bedrock_agentcore.memory import MemoryClient
client = MemoryClient(region_name='us-west-2')
client.delete_memory(memory_id='<stm-id>')
client.delete_memory(memory_id='<ltm-id>')
"

# Delete S3 bucket
aws s3 rb s3://umrah-trip-creator-frontend-${AWS_ACCOUNT_ID} --force
```

## Architecture Benefits

### AgentCore Runtime
- ✅ Serverless deployment (no infrastructure management)
- ✅ Auto-scaling based on demand
- ✅ Built-in session management
- ✅ Secure execution environment

### AgentCore Memory
- ✅ Short-term memory for conversation context
- ✅ Long-term memory for user preferences
- ✅ Automatic extraction of facts and preferences
- ✅ Cross-session persistence

### AgentCore Identity
- ✅ Cognito OAuth 2.0 authentication
- ✅ Secure token management
- ✅ User session isolation
- ✅ Fine-grained access control

### AgentCore Gateway
- ✅ Centralized API management
- ✅ Secure credential handling
- ✅ Multiple API integrations (Amadeus, Booking.com)
- ✅ MCP protocol support

## Cost Optimization

- Use STM for active sessions, LTM for returning users
- Set appropriate memory expiry (7 days STM, 90 days LTM)
- Configure agent idle timeout (default 15 minutes)
- Use direct_code_deploy for faster deployments
- Monitor CloudWatch metrics for optimization

## Security Best Practices

1. **Never commit API keys** - Use AWS Secrets Manager or environment variables
2. **Enable VPC** for private API access (if needed)
3. **Use IAM roles** with least privilege
4. **Enable CloudWatch logging** for audit trails
5. **Rotate Cognito secrets** regularly
6. **Use HTTPS** for all frontend communication

## Troubleshooting

### Agent Not Responding
```bash
# Check agent status
agentcore status --agent <agent-name> --verbose

# View recent logs
aws logs tail /aws/bedrock-agentcore/<agent-name> --since 10m
```

### Gateway Connection Issues
```bash
# Test gateway connectivity
curl -H "Authorization: Bearer $GATEWAY_ACCESS_TOKEN" $GATEWAY_URL

# List gateway targets
agentcore gateway list-mcp-gateway-targets --name <gateway-name>
```

### Memory Not Persisting
```bash
# Check memory status
python -c "
from bedrock_agentcore.memory import MemoryClient
client = MemoryClient(region_name='us-west-2')
memory = client.get_memory(memory_id='<memory-id>')
print(memory)
"
```

## Next Steps

1. **Add more API integrations** - Weather, currency exchange, prayer times
2. **Implement payment processing** - Stripe/PayPal integration
3. **Add email notifications** - SES for booking confirmations
4. **Build mobile app** - React Native with AgentCore SDK
5. **Add analytics** - CloudWatch dashboards and metrics
6. **Implement A/B testing** - Test different agent prompts
7. **Add multi-language support** - Arabic, Urdu, Turkish, etc.

## Resources

- [AgentCore Documentation](https://aws.github.io/bedrock-agentcore-starter-toolkit/)
- [Strands Agents Documentation](https://docs.strands.ai/)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Amadeus API](https://developers.amadeus.com/)
- [Booking.com API](https://developers.booking.com/)

---

**May your Umrah Trip Creator help many pilgrims plan their blessed journey! 🕋**
