# Frontend Setup Guide - Umrah Trip Creator

## Overview

The frontend has been updated to connect to your deployed AWS Bedrock AgentCore agents! You can now use real AI-powered trip planning.

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
pip3 install -r requirements.txt
```

### 2. Configure AWS Credentials

Make sure your AWS credentials are configured:

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region: us-west-2
```

### 3. Run the Frontend

```bash
# From the frontend directory
streamlit run streamlit_app.py

# Or from the project root
streamlit run frontend/streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## Configuration

### Toggle Between Demo and Production Mode

In `frontend/streamlit_app.py`, line 18:

```python
# Set to True to use deployed AgentCore agents
USE_AGENTCORE = True

# Set to False to use demo mode with mock data
USE_AGENTCORE = False
```

### Update Agent ARNs (if needed)

If you redeploy agents and get new ARNs, update them in `frontend/agentcore_client.py`:

```python
AGENT_ARNS = {
    'orchestrator': 'arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo',
    'flight': 'arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_flight_agent-ufM0XiC3fw',
    'hotel': 'arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_hotel_agent-P3Am0WF25G',
    'visa': 'arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_visa_agent-KR3L9yDFDl',
    'itinerary': 'arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_itinerary_agent-1XwH666geK'
}
```

## Features

### Production Mode (USE_AGENTCORE = True)

When enabled, the frontend will:

1. **Collect User Requirements** - Through the multi-step form
2. **Invoke Orchestrator Agent** - Sends all requirements to the main coordinator
3. **Call Specialized Agents** - Invokes flight, hotel, visa, and itinerary agents
4. **Display AI Insights** - Shows detailed recommendations from each agent
5. **Present Options** - Displays structured trip options with AI-generated content

### Demo Mode (USE_AGENTCORE = False)

- Uses mock data for testing
- No AWS calls made
- Faster for UI development
- Good for testing the interface

## How It Works

### AgentCore Client (`frontend/agentcore_client.py`)

The client handles all communication with deployed agents:

```python
from frontend.agentcore_client import get_agentcore_client

# Get client instance
client = get_agentcore_client()

# Invoke orchestrator with user requirements
response = client.invoke_orchestrator(user_requirements)

# Invoke specific agents
flight_response = client.invoke_flight_agent("Find flights from NYC to Jeddah")
hotel_response = client.invoke_hotel_agent("Find 5-star hotels in Makkah")
visa_response = client.invoke_visa_agent("Visa requirements for US citizens")
itinerary_response = client.invoke_itinerary_agent("Create 7-day Umrah itinerary")
```

### Response Handling

The client automatically:
- Formats user requirements into natural language prompts
- Invokes the appropriate AgentCore agent via boto3
- Parses the response and extracts text
- Handles errors gracefully

### Session Management

Each user session gets a unique session ID for conversation continuity:

```python
client = AgentCoreClient()
# Automatically generates session_id = str(uuid.uuid4())

# All subsequent calls use the same session
response1 = client.invoke_agent('orchestrator', 'Hello')
response2 = client.invoke_agent('orchestrator', 'Tell me more')
# Both use the same session for context
```

## User Flow

1. **Step 1: Travel Dates** - Select departure city, dates, duration
2. **Step 2: Traveler Details** - Add traveler information
3. **Step 3: Hotel Preferences** - Choose hotel preferences for Makkah & Madinah
4. **Step 4: Budget & Requirements** - Set budget and special requirements
5. **Step 5: Review & Generate** - Review and trigger AI agent processing
6. **Step 6: Trip Options** - View AI-generated recommendations and book

## Authentication

The frontend includes authentication via `frontend/auth.py`:

- Demo mode: Simple username/password (demo/demo)
- Production: Can be integrated with Cognito (already configured in .env)

To enable Cognito authentication, update `frontend/auth.py` to use the Cognito credentials from `.env`.

## Troubleshooting

### "No module named 'frontend.agentcore_client'"

Make sure you're running from the correct directory:

```bash
# From project root
cd umrah-trip-creator
streamlit run frontend/streamlit_app.py
```

### "Error invoking agent"

Check:
1. AWS credentials are configured: `aws sts get-caller-identity`
2. Agent ARNs are correct in `agentcore_client.py`
3. Agents are deployed and running: `agentcore status --agent umrah_orchestrator`

### "AccessDeniedException"

Your AWS user needs permissions to invoke AgentCore agents:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:InvokeAgentRuntime"
      ],
      "Resource": "arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/*"
    }
  ]
}
```

### Slow Response Times

AgentCore agents can take 5-30 seconds to respond depending on:
- Model complexity (Claude 3.5 Sonnet)
- Cold start (first invocation)
- Query complexity

The frontend shows a progress bar during processing.

## Development Tips

### Testing Individual Agents

You can test agents directly from Python:

```python
from frontend.agentcore_client import get_agentcore_client

client = get_agentcore_client()

# Test orchestrator
response = client.invoke_orchestrator({
    'travel_dates': {'departure': '2026-03-15', 'return': '2026-03-22'},
    'travelers': [{'name': 'John Doe', 'nationality': 'United States'}],
    'budget': {'total': 5000, 'currency': 'USD'}
})

print(client.extract_text_from_response(response))
```

### Adding New Features

To add new agent capabilities:

1. Update the agent runtime file (e.g., `agents/orchestrator/orchestrator_runtime.py`)
2. Redeploy: `agentcore deploy --agent umrah_orchestrator --auto-update-on-conflict`
3. Test the new functionality
4. Update frontend to use the new features

### Monitoring

View agent logs in real-time:

```bash
# Orchestrator logs
aws logs tail /aws/bedrock-agentcore/runtimes/umrah_orchestrator-DFFg1bHZKo-DEFAULT --follow

# All agents
for agent_id in DFFg1bHZKo ufM0XiC3fw P3Am0WF25G KR3L9yDFDl 1XwH666geK; do
    aws logs tail /aws/bedrock-agentcore/runtimes/*-${agent_id}-DEFAULT --since 5m
done
```

## Production Deployment

### Option 1: Streamlit Cloud

1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Add AWS credentials as secrets
4. Deploy!

### Option 2: AWS EC2

```bash
# Install dependencies
sudo yum install python3-pip
pip3 install -r frontend/requirements.txt

# Run with nohup
nohup streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 &
```

### Option 3: Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY frontend/ /app/frontend/
COPY .env /app/

RUN pip install -r frontend/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "frontend/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Cost Considerations

### Per User Session (Typical)

- 5 agent invocations (orchestrator + 4 specialists)
- ~2K input tokens + 1K output tokens per agent
- Claude 3.5 Sonnet: ~$0.003/1K input, ~$0.015/1K output
- **Cost per session: ~$0.10-0.15**

### Monthly Estimates

- 100 users/month: ~$10-15
- 1,000 users/month: ~$100-150
- 10,000 users/month: ~$1,000-1,500

*Plus AgentCore Runtime costs (~$0.0001 per invocation)*

## Next Steps

1. ✅ Test the frontend with deployed agents
2. ✅ Customize the UI/UX as needed
3. ✅ Add real API integrations (Amadeus, Booking.com)
4. ✅ Implement proper authentication
5. ✅ Add payment processing
6. ✅ Deploy to production

## Support

- **AgentCore Docs**: https://aws.github.io/bedrock-agentcore-starter-toolkit/
- **Streamlit Docs**: https://docs.streamlit.io/
- **AWS Bedrock**: https://docs.aws.amazon.com/bedrock/

---

**Last Updated**: February 3, 2026
**Status**: ✅ Ready for Testing
