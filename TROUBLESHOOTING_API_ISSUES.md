# Troubleshooting API Issues

## Common Issues and Solutions

### 1. Amadeus API Authentication Errors

**Symptoms:**
- "Failed to authenticate with Amadeus API"
- 401 Unauthorized errors

**Solutions:**

a) **Verify API Credentials:**
```bash
# Check if credentials are set
cat .env | grep AMADEUS
```

Expected output:
```
AMADEUS_API_KEY=2GPz8TnKFAbvAzBzaDyPQmCZEb4WP3Gv
AMADEUS_API_SECRET=rdAvLZyigXGwxJnH
```

b) **Test Authentication Directly:**
```bash
curl -X POST \
  https://test.api.amadeus.com/v1/security/oauth2/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=client_credentials&client_id=2GPz8TnKFAbvAzBzaDyPQmCZEb4WP3Gv&client_secret=rdAvLZyigXGwxJnH'
```

If this fails, your API credentials may be invalid or expired.

### 2. Rate Limiting Issues

**Symptoms:**
- "429 Too Many Requests"
- Intermittent failures

**Solutions:**
- Amadeus Test API has rate limits (typically 10 requests/second)
- Wait a few seconds between requests
- Consider upgrading to production API for higher limits

### 3. No Results Found

**Symptoms:**
- "No flights found"
- "No hotels found"
- Empty results

**Possible Causes:**

a) **Invalid Airport/City Codes:**
- Use 'JED' for Jeddah, 'MED' for Medina
- Use 'MEC' for Makkah hotels
- Check airport codes: https://www.iata.org/en/publications/directories/code-search/

b) **Date Issues:**
- Dates must be in YYYY-MM-DD format
- Dates must be in the future
- Check-out must be after check-in

c) **No Availability:**
- Try different dates
- Try broader search criteria (remove non-stop requirement)
- Try different star ratings

### 4. Timeout Errors

**Symptoms:**
- "Read timeout"
- "Connection timeout"

**Solutions:**
- Increase timeout in API calls (currently 30 seconds)
- Check internet connection
- Amadeus test API may be slow during peak hours

### 5. Agent Coordination Issues

**Symptoms:**
- Orchestrator takes too long
- Partial results only

**Solutions:**
- The orchestrator calls multiple agents sequentially (can take 2-3 minutes)
- Frontend timeout is set to 5 minutes
- Check CloudWatch logs for specific agent failures

## Checking Logs

### View Orchestrator Logs:
```bash
aws logs tail /aws/bedrock-agentcore/runtimes/umrah_orchestrator-DFFg1bHZKo-DEFAULT \
  --log-stream-name-prefix "2026/02/03/[runtime-logs" \
  --follow
```

### View Flight Agent Logs:
```bash
aws logs tail /aws/bedrock-agentcore/runtimes/umrah_flight_agent-ufM0XiC3fw-DEFAULT \
  --log-stream-name-prefix "2026/02/03/[runtime-logs" \
  --follow
```

### View Hotel Agent Logs:
```bash
aws logs tail /aws/bedrock-agentcore/runtimes/umrah_hotel_agent-P3Am0WF25G-DEFAULT \
  --log-stream-name-prefix "2026/02/03/[runtime-logs" \
  --follow
```

## Testing Individual Agents

### Test Flight Agent Directly:
```bash
cd agents/flight_agent
agentcore invoke '{"prompt": "Find flights from JFK to JED departing 2026-03-15 returning 2026-03-25 for 2 adults"}'
```

### Test Hotel Agent Directly:
```bash
cd agents/hotel_agent
agentcore invoke '{"prompt": "Find hotels in Makkah near Haram for March 15-20, 2026 for 2 adults, 4-5 star"}'
```

### Test Orchestrator Directly:
```bash
cd agents/orchestrator
agentcore invoke '{"prompt": "Plan an Umrah trip from New York to Jeddah, March 15-25, 2026, 2 adults, budget $6000"}'
```

## Fallback to Demo Mode

If API issues persist, you can temporarily switch to demo mode:

1. Open `frontend/streamlit_app.py`
2. Change line 18:
   ```python
   USE_AGENTCORE = False  # Set to False for demo mode
   ```
3. Restart the frontend

This will use mock data instead of real API calls for testing the UI.

## API Status Check

Check Amadeus API status:
- Test API: https://test.api.amadeus.com/v1/security/oauth2/token
- Status page: https://developers.amadeus.com/support

## Common Error Messages

### "Agent is already processing a request"
- **Cause:** Concurrent invocations (should be fixed)
- **Solution:** Wait for current request to complete, or restart frontend

### "Read timeout on endpoint URL"
- **Cause:** Orchestrator taking longer than timeout
- **Solution:** Already fixed with 5-minute timeout, but check if agents are stuck

### "No content in streaming response"
- **Cause:** Agent returned empty response
- **Solution:** Check agent logs for errors

### "Failed to parse flight/hotel data"
- **Cause:** Unexpected API response format
- **Solution:** Check API response in logs, may need to update parsing logic

## Getting Help

If issues persist:

1. **Check CloudWatch Logs** for detailed error messages
2. **Test API credentials** directly with curl
3. **Try different search parameters** (dates, cities, etc.)
4. **Check Amadeus API status** page
5. **Use demo mode** temporarily to test UI functionality

## Quick Diagnostic Script

Create a test script to diagnose issues:

```python
# test_api_connection.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("AMADEUS_API_KEY")
api_secret = os.getenv("AMADEUS_API_SECRET")

print(f"API Key: {api_key[:10]}..." if api_key else "API Key: NOT SET")
print(f"API Secret: {api_secret[:10]}..." if api_secret else "API Secret: NOT SET")

# Test authentication
url = "https://test.api.amadeus.com/v1/security/oauth2/token"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {
    "grant_type": "client_credentials",
    "client_id": api_key,
    "client_secret": api_secret
}

try:
    response = requests.post(url, headers=headers, data=data, timeout=10)
    response.raise_for_status()
    print("✅ Authentication successful!")
    print(f"Token: {response.json()['access_token'][:20]}...")
except Exception as e:
    print(f"❌ Authentication failed: {e}")
```

Run with:
```bash
python test_api_connection.py
```
