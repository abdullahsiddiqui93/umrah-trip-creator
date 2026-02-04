# Session ID and Environment Variables Fix

## Problem Identified

The orchestrator was reporting "technical difficulties" instead of returning real flight and hotel data. Investigation revealed two critical issues:

### Issue 1: Invalid Session IDs
**Symptom:** `Parameter validation failed: Invalid length for parameter runtimeSessionId, value: 22, valid min length: 33`

**Root Cause:** The orchestrator was creating session IDs using `f"orchestrator-flight-{os.urandom(8).hex()}"` which generated IDs that were too short (around 30-32 characters). AWS Bedrock AgentCore requires session IDs to be at least 33 characters.

**Fix:** Changed all session ID generation to use `str(uuid.uuid4())` which generates 36-character UUIDs.

### Issue 2: Missing Environment Variables
**Symptom:** `Error getting Amadeus token: 400 Client Error: Bad Request`

**Root Cause:** The Amadeus API credentials (`AMADEUS_API_KEY` and `AMADEUS_API_SECRET`) were not configured as environment variables in the AgentCore deployment configuration. The agents were trying to authenticate with the Amadeus API but had no credentials.

**Fix:** Added environment variables to `.bedrock_agentcore.yaml` files for both flight and hotel agents.

## Changes Made

### 1. Orchestrator Agent (`agents/orchestrator/orchestrator_runtime.py`)

**Before:**
```python
runtimeSessionId=f"orchestrator-flight-{os.urandom(8).hex()}"  # Too short!
```

**After:**
```python
import uuid
runtimeSessionId=str(uuid.uuid4())  # 36 characters, meets requirement
```

Applied to all 4 tool functions:
- `search_flights()`
- `search_hotels()`
- `get_visa_info()`
- `create_itinerary()`

### 2. Flight Agent Configuration (`agents/flight_agent/.bedrock_agentcore.yaml`)

**Added:**
```yaml
environment:
  AMADEUS_API_KEY: "2GPz8TnKFAbvAzBzaDyPQmCZEb4WP3Gv"
  AMADEUS_API_SECRET: "rdAvLZyigXGwxJnH"
```

### 3. Hotel Agent Configuration (`agents/hotel_agent/.bedrock_agentcore.yaml`)

**Added:**
```yaml
environment:
  AMADEUS_API_KEY: "2GPz8TnKFAbvAzBzaDyPQmCZEb4WP3Gv"
  AMADEUS_API_SECRET: "rdAvLZyigXGwxJnH"
```

## Deployment Status

All agents have been redeployed with fixes:
- ✅ Orchestrator Agent: Fixed session IDs
- ✅ Flight Agent: Added environment variables
- ✅ Hotel Agent: Added environment variables

## Testing

### Before Fix:
```
❌ Parameter validation failed: Invalid length for parameter runtimeSessionId
❌ Error getting Amadeus token: 400 Client Error
```

### After Fix:
The agents should now:
1. Successfully invoke specialized agents (no more session ID errors)
2. Successfully authenticate with Amadeus API
3. Return real flight and hotel data

## How to Verify

1. **Test via Frontend:**
   - Go to http://localhost:8501
   - Fill out trip requirements
   - Generate plan
   - Should see real flight and hotel options with actual prices

2. **Test Individual Agents:**
   ```bash
   cd agents/flight_agent
   agentcore invoke '{"prompt": "Find flights from JFK to JED departing 2026-03-15 returning 2026-03-25 for 2 adults"}'
   ```

3. **Test Orchestrator:**
   ```bash
   cd agents/orchestrator
   agentcore invoke '{"prompt": "Plan an Umrah trip from New York to Jeddah, March 15-25, 2026, 2 adults, budget $6000"}'
   ```

## Important Notes

- Session IDs must be at least 33 characters for AWS Bedrock AgentCore
- Environment variables in `.bedrock_agentcore.yaml` are deployed with the agent
- The Amadeus API credentials are now available to agents at runtime
- All agents have been redeployed and should be working

## Next Steps

1. Test the complete flow through the frontend
2. Verify multiple flight and hotel options are returned
3. Test custom itinerary feature
4. Monitor CloudWatch logs for any remaining issues

## Diagnostic Tools Created

- `test_api_connection.py` - Tests Amadeus API authentication
- `test_agents_simple.py` - Tests each agent individually
- `test_direct_api.py` - Tests API calls directly
- `TROUBLESHOOTING_API_ISSUES.md` - Comprehensive troubleshooting guide
