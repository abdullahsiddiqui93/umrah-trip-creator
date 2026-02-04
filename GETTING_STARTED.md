# Getting Started - Complete Walkthrough

This is your step-by-step guide to deploy the Umrah Trip Creator to AWS AgentCore.

## 🎯 Goal

Deploy a production-ready multi-agent system with:
- 5 AI agents working together
- Memory for conversation persistence
- Real-world API integration
- Secure authentication

## ⏱️ Time Required

- **Minimum setup**: 30 minutes (required APIs only)
- **Full setup**: 60 minutes (with optional APIs)
- **First deployment**: 45-60 minutes
- **Total**: 1.5-2 hours

## 📋 Prerequisites Checklist

Before you start, you need:

- [ ] Computer with internet connection
- [ ] Credit card (for AWS and API services)
- [ ] Email address
- [ ] Phone number (for AWS verification)
- [ ] ~$20-40 for initial credits

## 🚀 Step-by-Step Guide

### Step 1: Get API Keys (30-60 minutes)

Follow the detailed guide: **[API_KEYS_GUIDE.md](API_KEYS_GUIDE.md)**

#### Quick Summary:

**Required (30 minutes):**
1. **OpenAI** → https://platform.openai.com/api-keys
   - Sign up → Create API key → Add $5-20 credit
   - Copy key (starts with `sk-proj-...`)

2. **Anthropic** → https://console.anthropic.com/settings/keys
   - Sign up → Create API key → Add $5-20 credit
   - Copy key (starts with `sk-ant-...`)

3. **AWS** → https://console.aws.amazon.com/iam/
   - Create account → Create IAM user → Create access keys
   - Run `aws configure` with your keys

**Optional (30 minutes):**
4. **Amadeus** → https://developers.amadeus.com/register
   - Sign up → Create app → Copy API key + secret
   - Use test API (free, 2000 calls/month)

5. **Hotels** → https://rapidapi.com/
   - Sign up → Subscribe to hotel API → Copy RapidAPI key
   - Free tier available (100-500 calls/month)

### Step 2: Install Dependencies (5 minutes)

```bash
# Navigate to your project
cd umrah-trip-creator

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install AgentCore toolkit
pip install bedrock-agentcore-starter-toolkit bedrock-agentcore strands-agents

# Verify installation
agentcore --version
```

### Step 3: Configure Environment (5 minutes)

```bash
# Copy environment template
cp .env.example .env

# Edit .env file
nano .env  # or use VS Code, vim, etc.
```

**Add your API keys:**
```bash
# Required
OPENAI_API_KEY=sk-proj-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
AWS_REGION=us-west-2
AWS_ACCOUNT_ID=your-account-id

# Optional (for real data)
AMADEUS_API_KEY=your-amadeus-key
AMADEUS_API_SECRET=your-amadeus-secret
RAPIDAPI_KEY=your-rapidapi-key
```

**Save and close** the file.

### Step 4: Set Up Memory (2 minutes)

```bash
# Create AgentCore Memory resources
python3 setup_memory.py
```

**Output will show:**
```
Creating memory resources for Umrah Trip Creator...
✅ STM Memory Created: mem-abc123xyz
✅ LTM Memory Created: mem-def456uvw

Add these to your .env file:
MEMORY_STM_ID=mem-abc123xyz
MEMORY_LTM_ID=mem-def456uvw
```

**Copy the IDs to your .env file:**
```bash
nano .env
# Add:
MEMORY_STM_ID=mem-abc123xyz
MEMORY_LTM_ID=mem-def456uvw
```

### Step 5: Set Up Gateway (3 minutes)

```bash
# Create AgentCore Gateway with API targets
python3 setup_gateway.py
```

**Output will show:**
```
Creating AgentCore Gateway for Umrah Trip Creator
✅ Authorization server created
✅ Gateway created: https://gateway-xyz.execute-api.us-west-2.amazonaws.com
✅ IAM permissions configured
✅ Access token obtained
✅ Amadeus Flight API target added
✅ Booking.com Hotel API target added
✅ Visa Processing Lambda target added

Add these to your .env file:
GATEWAY_URL=https://gateway-xyz.execute-api.us-west-2.amazonaws.com
GATEWAY_ID=gateway-xyz
GATEWAY_ACCESS_TOKEN=eyJhbGc...
COGNITO_USER_POOL_ID=us-west-2_abc123
COGNITO_CLIENT_ID=client-xyz
COGNITO_CLIENT_SECRET=secret-abc
```

**Copy all values to your .env file:**
```bash
nano .env
# Add all the gateway configuration
```

### Step 6: Create Agent Runtime Files (10 minutes)

You need to create the runtime wrapper files for each agent. These files are in the deployment guide.

**Quick way - Copy from templates:**

```bash
# Create orchestrator runtime
cat > agents/orchestrator/orchestrator_runtime.py << 'EOF'
# Copy the code from AGENTCORE_DEPLOYMENT_GUIDE.md
# Section: "Update Orchestrator Agent"
EOF

# Create requirements.txt
cat > agents/orchestrator/requirements.txt << 'EOF'
bedrock-agentcore
strands-agents
mcp
EOF

# Repeat for other agents:
# - agents/flight_agent/flight_runtime.py
# - agents/hotel_agent/hotel_runtime.py
# - agents/visa_agent/visa_runtime.py
# - agents/itinerary_agent/itinerary_runtime.py
```

**Or manually:** Open `AGENTCORE_DEPLOYMENT_GUIDE.md` and copy the code for each agent.

### Step 7: Deploy All Agents (30-50 minutes)

```bash
# Run automated deployment
./deploy_to_agentcore.sh
```

**This will:**
1. ✅ Validate prerequisites (1 min)
2. ✅ Deploy orchestrator agent (5-10 min)
3. ✅ Deploy flight agent (5-10 min)
4. ✅ Deploy hotel agent (5-10 min)
5. ✅ Deploy visa agent (5-10 min)
6. ✅ Deploy itinerary agent (5-10 min)
7. ✅ Test deployment (1 min)

**Total: 30-50 minutes** (AWS builds containers in the cloud)

**You'll see output like:**
```
==========================================
Umrah Trip Creator - AgentCore Deployment
==========================================

Checking prerequisites...
✅ AWS CLI found
✅ Python 3 found
✅ .env file found
✅ Environment variables configured
✅ AgentCore CLI ready

==========================================
Step 3: Deploying Agents to AgentCore Runtime
==========================================

Deploying umrah-orchestrator...
⏳ Building container image...
⏳ Deploying to AgentCore Runtime...
✅ umrah-orchestrator deployed successfully

Deploying umrah-flight-agent...
⏳ Building container image...
⏳ Deploying to AgentCore Runtime...
✅ umrah-flight-agent deployed successfully

... (continues for all agents)

==========================================
✅ Deployment Complete!
==========================================
```

### Step 8: Test Your Deployment (5 minutes)

```bash
# Test basic functionality
agentcore invoke '{"prompt": "Hello, I want to plan an Umrah trip"}' \
  --agent umrah-orchestrator

# Test with details
agentcore invoke '{
  "prompt": "Plan an Umrah trip for 2 people from New York, departing March 15, 2026, returning March 25, 2026. Budget $6000 total."
}' --agent umrah-orchestrator

# Test memory (two messages)
agentcore invoke '{"prompt": "My name is Ahmed and I prefer budget hotels"}' \
  --agent umrah-orchestrator --session-id test-123

sleep 10  # Wait for memory extraction

agentcore invoke '{"prompt": "What are my preferences?"}' \
  --agent umrah-orchestrator --session-id test-123
```

**Expected output:**
```json
{
  "result": "Hello Ahmed! I'd be happy to help you plan your Umrah trip. Based on your preferences for budget-friendly options, I'll coordinate with our specialized agents to find the best deals for flights, hotels, and create a comprehensive itinerary...",
  "session_id": "test-123",
  "user_id": "anonymous"
}
```

### Step 9: Monitor Your Agents (Ongoing)

```bash
# Check agent status
agentcore status --agent umrah-orchestrator --verbose

# View logs in real-time
aws logs tail /aws/bedrock-agentcore/umrah-orchestrator --follow

# Check memory usage
python3 -c "
from bedrock_agentcore.memory import MemoryClient
import os
client = MemoryClient(region_name='us-west-2')
memory = client.get_memory(memory_id=os.getenv('MEMORY_LTM_ID'))
print(f'Memory: {memory[\"name\"]} - Status: {memory[\"status\"]}')
"

# Check gateway
agentcore gateway list-mcp-gateway-targets --id $GATEWAY_ID
```

## 🎉 Success Criteria

Your deployment is successful when:

✅ All 5 agents show status "ACTIVE"  
✅ Test invocations return responses  
✅ Memory persists across sessions  
✅ Gateway connects to APIs  
✅ Logs appear in CloudWatch  
✅ No error messages in deployment  

## 🔧 Troubleshooting

### Problem: "AWS credentials not configured"
```bash
# Solution: Configure AWS CLI
aws configure
# Enter your access key, secret key, region (us-west-2)
```

### Problem: "Invalid API key"
```bash
# Solution: Check .env file
cat .env | grep API_KEY
# Verify no extra spaces, quotes, or newlines
# Regenerate key if needed
```

### Problem: "Agent deployment failed"
```bash
# Solution: Check logs
agentcore status --agent umrah-orchestrator --verbose
aws logs tail /aws/bedrock-agentcore/umrah-orchestrator --since 10m

# Try redeploying
agentcore launch --agent umrah-orchestrator --auto-update-on-conflict
```

### Problem: "Memory not persisting"
```bash
# Solution: Verify memory ID
echo $MEMORY_LTM_ID

# Check memory status
python3 -c "
from bedrock_agentcore.memory import MemoryClient
client = MemoryClient(region_name='us-west-2')
print(client.get_memory(memory_id='$MEMORY_LTM_ID'))
"

# Wait 10 seconds after messages for extraction
```

### Problem: "Gateway connection failed"
```bash
# Solution: Test gateway
curl -H "Authorization: Bearer $GATEWAY_ACCESS_TOKEN" $GATEWAY_URL

# Regenerate token
python3 setup_gateway.py
```

## 📚 Documentation Reference

- **API Keys**: [API_KEYS_GUIDE.md](API_KEYS_GUIDE.md) - How to get all API keys
- **Quick Start**: [AGENTCORE_QUICKSTART.md](AGENTCORE_QUICKSTART.md) - 15-minute guide
- **Full Guide**: [AGENTCORE_DEPLOYMENT_GUIDE.md](AGENTCORE_DEPLOYMENT_GUIDE.md) - Complete reference
- **Summary**: [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) - Architecture overview

## 💰 Cost Breakdown

### Initial Setup
- OpenAI credits: $5-20
- Anthropic credits: $5-20
- AWS (first month): $10-30
- **Total: $20-70**

### Monthly Costs
- Development: $25-60/month
- Production (moderate): $85-420/month
- High traffic: $420-1950/month

### Free Tiers
- AWS: 12 months free tier
- Amadeus: 2,000 calls/month free
- RapidAPI: 100-500 calls/month free

## 🧹 Clean Up

To remove all resources:

```bash
./cleanup_agentcore.sh
```

This removes:
- All deployed agents
- Gateway and API targets
- Memory resources
- Local configuration files

**Note:** Some resources (CloudWatch logs, IAM roles) may require manual cleanup.

## 🎯 Next Steps

After successful deployment:

1. **Update Frontend** - Connect Streamlit to deployed agents
2. **Deploy Frontend** - Host on S3/CloudFront
3. **Add Features** - Payment processing, email notifications
4. **Monitor** - Set up CloudWatch dashboards
5. **Optimize** - Tune agent prompts and memory settings

## 📞 Getting Help

If you get stuck:

1. Check the troubleshooting section above
2. Review the detailed guides in the documentation
3. Check AWS CloudWatch logs
4. Verify all environment variables are set
5. Try the cleanup script and redeploy

## ✅ Deployment Checklist

Print this and check off as you go:

- [ ] Got OpenAI API key
- [ ] Got Anthropic API key
- [ ] Configured AWS CLI
- [ ] Got optional API keys (Amadeus, Hotels)
- [ ] Installed dependencies
- [ ] Created .env file with all keys
- [ ] Ran setup_memory.py
- [ ] Added memory IDs to .env
- [ ] Ran setup_gateway.py
- [ ] Added gateway config to .env
- [ ] Created agent runtime files
- [ ] Ran deploy_to_agentcore.sh
- [ ] Tested deployment
- [ ] Verified all agents are ACTIVE
- [ ] Tested memory persistence
- [ ] Tested gateway connectivity

## 🎊 Congratulations!

Once all checkboxes are complete, you have a fully deployed, production-ready multi-agent system running on AWS AgentCore!

Your Umrah Trip Creator can now:
- Handle multiple users simultaneously
- Remember user preferences across sessions
- Search real flight and hotel data
- Coordinate multiple AI agents
- Scale automatically with demand

**May this system help many pilgrims plan their blessed journey! 🕋**

---

**Ready to start? Begin with [API_KEYS_GUIDE.md](API_KEYS_GUIDE.md)!**
