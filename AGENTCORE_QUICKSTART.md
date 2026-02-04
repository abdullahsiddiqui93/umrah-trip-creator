# AgentCore Deployment - Quick Start Guide

Deploy your Umrah Trip Creator to AWS AgentCore in 15 minutes!

## What You'll Get

✅ **5 AI Agents** deployed to AgentCore Runtime (serverless, auto-scaling)  
✅ **Memory** for conversation persistence and user preferences  
✅ **Identity** with Cognito OAuth 2.0 authentication  
✅ **Gateway** for real-world API integration (Amadeus, Booking.com)  
✅ **Production-ready** infrastructure with monitoring and logging  

## Prerequisites

Before starting, ensure you have:

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured: `aws configure`
3. **Python 3.10+** installed
4. **API Keys**:
   - OpenAI API key (required)
   - Anthropic API key (required)
   - Amadeus API credentials (optional, for real flight data)
   - Booking.com API key (optional, for real hotel data)

## Step 1: Install Dependencies

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install AgentCore toolkit
pip install bedrock-agentcore-starter-toolkit bedrock-agentcore strands-agents

# Verify installation
agentcore --version
```

## Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your credentials
nano .env  # or use your preferred editor
```

**Required variables:**
```bash
AWS_REGION=us-west-2
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
```

**Optional (for real API integration):**
```bash
AMADEUS_API_KEY=your-amadeus-key
AMADEUS_API_SECRET=your-amadeus-secret
BOOKING_API_KEY=your-booking-key
```

## Step 3: Set Up Memory

```bash
# Create memory resources
python3 setup_memory.py
```

This creates:
- **Short-Term Memory (STM)**: Conversation within sessions (7-day retention)
- **Long-Term Memory (LTM)**: User preferences across sessions (90-day retention)

**Copy the memory IDs to your .env file:**
```bash
MEMORY_STM_ID=<stm-id-from-output>
MEMORY_LTM_ID=<ltm-id-from-output>
```

## Step 4: Set Up Gateway

```bash
# Create gateway with API targets
python3 setup_gateway.py
```

This creates:
- **Gateway** with OAuth 2.0 authentication
- **Amadeus target** for flight searches (if credentials provided)
- **Booking.com target** for hotel searches (if credentials provided)
- **Lambda target** for visa processing

**Copy the gateway configuration to your .env file:**
```bash
GATEWAY_URL=<gateway-url-from-output>
GATEWAY_ID=<gateway-id-from-output>
GATEWAY_ACCESS_TOKEN=<token-from-output>
COGNITO_USER_POOL_ID=<pool-id-from-output>
COGNITO_CLIENT_ID=<client-id-from-output>
COGNITO_CLIENT_SECRET=<secret-from-output>
```

## Step 5: Deploy All Agents

```bash
# Run automated deployment script
./deploy_to_agentcore.sh
```

This script:
1. ✅ Validates prerequisites
2. ✅ Deploys orchestrator agent (main coordinator)
3. ✅ Deploys flight agent (flight search)
4. ✅ Deploys hotel agent (hotel search)
5. ✅ Deploys visa agent (visa requirements)
6. ✅ Deploys itinerary agent (trip planning)
7. ✅ Tests deployment

**Deployment takes 5-10 minutes per agent.**

## Step 6: Test Your Deployment

### Test Individual Agents

```bash
# Test orchestrator
agentcore invoke '{"prompt": "I want to plan an Umrah trip for 2 people"}' \
  --agent umrah-orchestrator

# Test flight agent
agentcore invoke '{"prompt": "Search flights from New York to Jeddah for March 15-25"}' \
  --agent umrah-flight-agent

# Test hotel agent
agentcore invoke '{"prompt": "Find 4-star hotels in Makkah near Haram"}' \
  --agent umrah-hotel-agent

# Test visa agent
agentcore invoke '{"prompt": "Check visa requirements for US citizens"}' \
  --agent umrah-visa-agent

# Test itinerary agent
agentcore invoke '{"prompt": "Create a 10-day Umrah itinerary"}' \
  --agent umrah-itinerary-agent
```

### Test with Session Memory

```bash
# First message - introduce yourself
agentcore invoke '{"prompt": "My name is Ahmed and I prefer budget-friendly options"}' \
  --agent umrah-orchestrator \
  --session-id test-session-123

# Wait 10 seconds for memory extraction
sleep 10

# Second message - agent should remember your preferences
agentcore invoke '{"prompt": "What are my preferences?"}' \
  --agent umrah-orchestrator \
  --session-id test-session-123
```

### Test Gateway Tools

```bash
# Test with real API calls (if configured)
agentcore invoke '{"prompt": "Search flights from JFK to JED departing March 15, 2026"}' \
  --agent umrah-flight-agent
```

## Step 7: Monitor Your Agents

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
# View orchestrator logs (real-time)
aws logs tail /aws/bedrock-agentcore/umrah-orchestrator --follow

# View flight agent logs
aws logs tail /aws/bedrock-agentcore/umrah-flight-agent --follow

# View last 10 minutes of logs
aws logs tail /aws/bedrock-agentcore/umrah-orchestrator --since 10m
```

### Check Memory Usage

```bash
python3 << EOF
from bedrock_agentcore.memory import MemoryClient
import os

client = MemoryClient(region_name='us-west-2')
memory_id = os.getenv('MEMORY_LTM_ID')

# Get memory details
memory = client.get_memory(memory_id=memory_id)
print(f"Memory: {memory['name']}")
print(f"Status: {memory['status']}")

# Get recent events
events = client.list_events(memory_id=memory_id, max_results=5)
print(f"Recent events: {len(events)}")
EOF
```

### Check Gateway Status

```bash
# List gateway targets
agentcore gateway list-mcp-gateway-targets --id $GATEWAY_ID

# Get gateway details
agentcore gateway get-mcp-gateway --id $GATEWAY_ID
```

## Common Issues & Solutions

### Issue: Agent deployment fails

**Solution:**
```bash
# Check AWS credentials
aws sts get-caller-identity

# Check region
echo $AWS_REGION

# Try deploying with verbose output
agentcore launch --agent umrah-orchestrator --verbose
```

### Issue: Memory not persisting

**Solution:**
```bash
# Verify memory ID is set
echo $MEMORY_LTM_ID

# Check memory status
python3 -c "from bedrock_agentcore.memory import MemoryClient; client = MemoryClient(region_name='us-west-2'); print(client.get_memory(memory_id='$MEMORY_LTM_ID'))"

# Wait 10 seconds after each message for extraction
```

### Issue: Gateway connection fails

**Solution:**
```bash
# Test gateway connectivity
curl -H "Authorization: Bearer $GATEWAY_ACCESS_TOKEN" $GATEWAY_URL

# Check gateway targets
agentcore gateway list-mcp-gateway-targets --id $GATEWAY_ID

# Regenerate access token
python3 setup_gateway.py
```

### Issue: API calls not working

**Solution:**
```bash
# Verify API credentials in .env
cat .env | grep API_KEY

# Check gateway target configuration
agentcore gateway get-mcp-gateway-target --id $GATEWAY_ID --target-name AmadeusFlightAPI

# Test API directly
curl -X POST https://test.api.amadeus.com/v1/security/oauth2/token \
  -d "grant_type=client_credentials&client_id=$AMADEUS_API_KEY&client_secret=$AMADEUS_API_SECRET"
```

## Clean Up Resources

To remove all deployed resources:

```bash
# Run cleanup script
./cleanup_agentcore.sh
```

This removes:
- All deployed agents
- Gateway and targets
- Memory resources
- Local configuration files

**Note:** CloudWatch logs, IAM roles, and Cognito resources may require manual cleanup.

## Next Steps

### 1. Update Frontend

Modify `frontend/streamlit_app.py` to use deployed agents:

```python
import boto3

agentcore_client = boto3.client('bedrock-agentcore-runtime', region_name='us-west-2')

def invoke_orchestrator(prompt, session_id, user_id):
    response = agentcore_client.invoke_agent(
        agentName='umrah-orchestrator',
        sessionId=session_id,
        userId=user_id,
        inputText=prompt
    )
    return response['output']
```

### 2. Deploy Frontend

```bash
# Deploy to S3
aws s3 mb s3://umrah-trip-creator-frontend-${AWS_ACCOUNT_ID}
aws s3 sync frontend/ s3://umrah-trip-creator-frontend-${AWS_ACCOUNT_ID}/

# Enable static website hosting
aws s3 website s3://umrah-trip-creator-frontend-${AWS_ACCOUNT_ID} \
  --index-document index.html
```

### 3. Add More Features

- **Payment processing**: Integrate Stripe/PayPal
- **Email notifications**: Use AWS SES
- **Multi-language**: Add Arabic, Urdu, Turkish
- **Mobile app**: Build with React Native
- **Analytics**: CloudWatch dashboards

### 4. Production Optimization

- Enable VPC for private API access
- Set up CloudWatch alarms
- Configure auto-scaling policies
- Implement rate limiting
- Add caching layer

## Architecture Overview

```
User → Streamlit Frontend (S3/CloudFront)
         ↓
    Cognito Authentication
         ↓
    Orchestrator Agent (AgentCore Runtime)
         ↓
    Memory (STM + LTM) + Gateway
         ↓
    Specialized Agents (Flight, Hotel, Visa, Itinerary)
         ↓
    Real-world APIs (Amadeus, Booking.com, etc.)
```

## Cost Estimate

**Monthly costs (estimated for moderate usage):**

- AgentCore Runtime: $50-200 (based on invocations)
- AgentCore Memory: $10-50 (based on storage and queries)
- AgentCore Gateway: $20-100 (based on API calls)
- Cognito: $0-50 (first 50,000 MAUs free)
- CloudWatch Logs: $5-20
- S3 + CloudFront: $5-20

**Total: ~$90-440/month**

**Cost optimization tips:**
- Use STM for active sessions only
- Set appropriate memory expiry
- Configure agent idle timeout
- Use CloudWatch metrics to optimize

## Support & Resources

- **AgentCore Documentation**: https://aws.github.io/bedrock-agentcore-starter-toolkit/
- **Strands Agents**: https://docs.strands.ai/
- **MCP Protocol**: https://modelcontextprotocol.io/
- **AWS Support**: https://console.aws.amazon.com/support/

## Troubleshooting Commands

```bash
# Check agent configuration
cat .bedrock_agentcore.yaml

# List all deployed agents
agentcore configure list

# View agent endpoint
agentcore status --agent umrah-orchestrator --verbose | grep endpoint

# Test agent locally before deploying
agentcore launch --agent umrah-orchestrator --local

# Update agent without redeploying
agentcore launch --agent umrah-orchestrator --auto-update-on-conflict

# Stop a specific session
agentcore stop-session --agent umrah-orchestrator --session-id <session-id>
```

---

**Congratulations! Your Umrah Trip Creator is now running on AWS AgentCore! 🕋**

May this system help many pilgrims plan their blessed journey!
