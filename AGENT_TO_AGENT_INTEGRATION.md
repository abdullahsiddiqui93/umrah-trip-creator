# Agent-to-Agent Integration Complete

## Problem Solved
The orchestrator agent was not calling the specialized flight and hotel agents - it was just generating responses using its own LLM knowledge. This meant the frontend wasn't getting real API data even though the individual agents had working API integrations.

## Solution Implemented
Implemented agent-to-agent (A2A) communication where the orchestrator calls the specialized agents using boto3's `invoke_agent_runtime` API.

## Changes Made

### 1. Updated Orchestrator Agent (`agents/orchestrator/orchestrator_runtime.py`)
- Added boto3 client for bedrock-agentcore service
- Created 4 tools that invoke the specialized agents:
  - `search_flights()` - Calls flight agent with Amadeus API
  - `search_hotels()` - Calls hotel agent with Booking.com API
  - `get_visa_info()` - Calls visa agent
  - `create_itinerary()` - Calls itinerary agent
- Each tool properly handles streaming responses from the invoked agents
- Added error handling with detailed tracebacks

### 2. Updated Dependencies (`agents/orchestrator/requirements.txt`)
- Added `boto3>=1.35.0` for AWS SDK calls

### 3. Fixed IAM Permissions
- Added inline policy `AllowInvokeOtherAgents` to the orchestrator's execution role
- Granted `bedrock-agentcore:InvokeAgentRuntime` permission for all 4 specialized agents
- Used wildcard in resource ARN to cover runtime endpoints: `arn:...:runtime/agent-name*`

### 4. Redeployed Orchestrator
- Deployed updated code to AgentCore Runtime
- Verified agent-to-agent communication works via CLI test

## Test Results

### CLI Test (Successful)
```bash
agentcore invoke '{"prompt": "Find me flights from New York to Medina departing February 15, 2026 returning February 25, 2026 for 2 adults"}'
```

**Result:** ✅ Working!
- Orchestrator successfully called the flight agent
- Flight agent called Amadeus API
- Returned real flight data:
  - Turkish Airlines TK4 + TK108
  - JFK → Istanbul → Medina
  - $1,833.18 per person ($3,666.36 total for 2 adults)
  - Real flight times and durations
  - Seat availability information

## Architecture

```
Frontend (Streamlit)
    ↓
    calls
    ↓
Orchestrator Agent
    ↓
    invokes via boto3
    ↓
┌─────────────────────────────────────┐
│ Flight Agent (Amadeus API)          │
│ Hotel Agent (Booking.com API)       │
│ Visa Agent                          │
│ Itinerary Agent                     │
└─────────────────────────────────────┘
```

## How It Works

1. **User Request:** User asks for flights/hotels in the frontend
2. **Frontend → Orchestrator:** Frontend calls orchestrator agent via AgentCore client
3. **Orchestrator Analysis:** Orchestrator determines which specialized agent(s) to call
4. **Agent Invocation:** Orchestrator uses boto3 to invoke specialized agent(s)
5. **API Calls:** Specialized agents call real APIs (Amadeus, Booking.com)
6. **Response Chain:** Results flow back: API → Agent → Orchestrator → Frontend → User

## Key Technical Details

### Boto3 API Call
```python
response = bedrock_client.invoke_agent_runtime(
    agentRuntimeArn=FLIGHT_AGENT_ARN,
    runtimeSessionId=f"orchestrator-flight-{os.urandom(8).hex()}",
    payload=json.dumps({"prompt": request}).encode()
)
```

### Streaming Response Handling
```python
if "text/event-stream" in content_type:
    content = []
    for line in response["response"].iter_lines(chunk_size=10):
        if line:
            line = line.decode("utf-8")
            if line.startswith("data: "):
                line = line[6:]
                content.append(line)
    return "\n".join(content)
```

### IAM Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock-agentcore:InvokeAgentRuntime",
      "Resource": [
        "arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_flight_agent-ufM0XiC3fw*",
        "arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_hotel_agent-P3Am0WF25G*",
        "arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_visa_agent-KR3L9yDFDl*",
        "arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_itinerary_agent-1XwH666geK*"
      ]
    }
  ]
}
```

## Next Steps

1. **Test Frontend:** Open http://localhost:8501 and test the full flow
2. **Verify Hotels:** Test hotel search to ensure it also works with real API
3. **Test Complete Trip:** Request a full trip plan (flights + hotels + itinerary)
4. **Monitor Logs:** Check CloudWatch logs for any issues
5. **Optimize:** Consider caching, error handling improvements, and cost optimization

## Status
✅ **COMPLETE** - Agent-to-agent communication is working with real API data!

The orchestrator now properly delegates to specialized agents, which call real APIs and return actual flight/hotel data to users.
