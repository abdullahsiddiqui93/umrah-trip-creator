# Umrah Trip Creator - AWS AgentCore Deployment

Complete multi-agent system for planning Umrah trips, deployed on AWS AgentCore with Runtime, Memory, Identity, and Gateway.

## 🚀 Quick Start

```bash
# 1. Get API keys (see API_KEYS_GUIDE.md)
# 2. Install dependencies
pip install bedrock-agentcore-starter-toolkit bedrock-agentcore strands-agents

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Set up infrastructure
python3 setup_memory.py      # Creates memory resources
python3 setup_gateway.py     # Creates gateway with APIs

# 5. Deploy agents
./deploy_to_agentcore.sh     # Deploys all 5 agents

# 6. Test
agentcore invoke '{"prompt": "Plan an Umrah trip"}' --agent umrah-orchestrator
```

**Total time: 1.5-2 hours** | **Cost: $20-70 to start**

## 📚 Documentation

Start here based on your needs:

### 🎯 New to the Project?
**[GETTING_STARTED.md](GETTING_STARTED.md)** - Complete walkthrough with checklist

### 🔑 Need API Keys?
**[API_KEYS_GUIDE.md](API_KEYS_GUIDE.md)** - How to get OpenAI, Anthropic, Amadeus, etc.

### ⚡ Want Quick Deployment?
**[AGENTCORE_QUICKSTART.md](AGENTCORE_QUICKSTART.md)** - 15-minute deployment guide

### 📖 Need Full Details?
**[AGENTCORE_DEPLOYMENT_GUIDE.md](AGENTCORE_DEPLOYMENT_GUIDE.md)** - Comprehensive reference

### 🏗️ Want Architecture Overview?
**[DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)** - System architecture and components

## 🎯 What You Get

### 5 AI Agents on AgentCore Runtime
- **Orchestrator**: Main coordinator with memory
- **Flight Agent**: Real flight searches (Amadeus API)
- **Hotel Agent**: Real hotel searches (Booking.com/RapidAPI)
- **Visa Agent**: Visa requirements processing
- **Itinerary Agent**: Umrah ritual planning

### AgentCore Memory
- **Short-Term Memory**: Conversation within sessions (7 days)
- **Long-Term Memory**: User preferences across sessions (90 days)
- **Automatic extraction**: Preferences and facts

### AgentCore Identity
- **Cognito OAuth 2.0**: Secure authentication
- **Session management**: User isolation
- **Access control**: Fine-grained permissions

### AgentCore Gateway
- **MCP protocol**: Centralized API management
- **Real APIs**: Amadeus, Booking.com, visa processing
- **Secure credentials**: OAuth 2.0 and API key handling

## 🏗️ Architecture

```
User → Frontend (Streamlit)
         ↓
    Cognito Auth
         ↓
    Orchestrator Agent (AgentCore Runtime + Memory)
         ↓
    Specialized Agents (Flight, Hotel, Visa, Itinerary)
         ↓
    Gateway (MCP) → Real-world APIs
```

## 📋 Prerequisites

### Required
- AWS account with CLI configured
- OpenAI API key ($5-20 credit)
- Anthropic API key ($5-20 credit)
- Python 3.10+

### Optional (for real data)
- Amadeus API (free test tier)
- Hotel API via RapidAPI (free tier)

## 🛠️ Setup Scripts

### `setup_memory.py`
Creates AgentCore Memory resources (STM + LTM)
```bash
python3 setup_memory.py
# Outputs memory IDs to add to .env
```

### `setup_gateway.py`
Creates Gateway with API targets and Cognito auth
```bash
python3 setup_gateway.py
# Outputs gateway config to add to .env
```

### `deploy_to_agentcore.sh`
Deploys all 5 agents to AgentCore Runtime
```bash
./deploy_to_agentcore.sh
# Takes 30-50 minutes
```

### `cleanup_agentcore.sh`
Removes all deployed resources
```bash
./cleanup_agentcore.sh
# Cleans up everything
```

## 🧪 Testing

### Basic Test
```bash
agentcore invoke '{"prompt": "Hello"}' --agent umrah-orchestrator
```

### Memory Test
```bash
# First message
agentcore invoke '{"prompt": "I prefer budget hotels"}' \
  --agent umrah-orchestrator --session-id test-123

# Wait for extraction
sleep 10

# Second message (should remember)
agentcore invoke '{"prompt": "What are my preferences?"}' \
  --agent umrah-orchestrator --session-id test-123
```

### Full Workflow Test
```bash
agentcore invoke '{
  "prompt": "Plan Umrah for 2 people from NYC, March 15-25, 2026, $6000 budget"
}' --agent umrah-orchestrator
```

## 📊 Monitoring

### Check Status
```bash
agentcore status --agent umrah-orchestrator --verbose
```

### View Logs
```bash
aws logs tail /aws/bedrock-agentcore/umrah-orchestrator --follow
```

### Check Memory
```bash
python3 -c "
from bedrock_agentcore.memory import MemoryClient
import os
client = MemoryClient(region_name='us-west-2')
print(client.get_memory(memory_id=os.getenv('MEMORY_LTM_ID')))
"
```

### Check Gateway
```bash
agentcore gateway list-mcp-gateway-targets --id $GATEWAY_ID
```

## 💰 Costs

### Initial Setup
- OpenAI: $5-20
- Anthropic: $5-20
- AWS: $10-30
- **Total: $20-70**

### Monthly (Development)
- AgentCore Runtime: $10-30
- Memory: $5-10
- Gateway: $5-15
- **Total: $25-60/month**

### Monthly (Production)
- AgentCore Runtime: $50-200
- Memory: $10-50
- Gateway: $20-100
- **Total: $85-420/month**

## 🔧 Troubleshooting

### Agent deployment fails
```bash
agentcore status --agent <name> --verbose
aws logs tail /aws/bedrock-agentcore/<name> --since 10m
```

### Memory not persisting
```bash
echo $MEMORY_LTM_ID  # Verify ID is set
# Wait 10 seconds after messages for extraction
```

### Gateway connection fails
```bash
curl -H "Authorization: Bearer $GATEWAY_ACCESS_TOKEN" $GATEWAY_URL
agentcore gateway list-mcp-gateway-targets --id $GATEWAY_ID
```

### API keys invalid
```bash
cat .env | grep API_KEY  # Check for spaces/quotes
# Regenerate keys if needed
```

## 📁 Project Structure

```
umrah-trip-creator/
├── agents/
│   ├── orchestrator/
│   │   ├── orchestrator_agent.py      # Original agent
│   │   ├── orchestrator_runtime.py    # AgentCore wrapper
│   │   └── requirements.txt
│   ├── flight_agent/
│   ├── hotel_agent/
│   ├── visa_agent/
│   └── itinerary_agent/
├── frontend/
│   └── streamlit_app.py
├── setup_memory.py                     # Memory setup script
├── setup_gateway.py                    # Gateway setup script
├── deploy_to_agentcore.sh             # Deployment script
├── cleanup_agentcore.sh               # Cleanup script
├── .env.example                        # Environment template
├── GETTING_STARTED.md                 # Start here!
├── API_KEYS_GUIDE.md                  # Get API keys
├── AGENTCORE_QUICKSTART.md            # Quick deployment
├── AGENTCORE_DEPLOYMENT_GUIDE.md      # Full reference
└── DEPLOYMENT_SUMMARY.md              # Architecture overview
```

## 🎯 Success Criteria

Your deployment is successful when:

✅ All 5 agents show "ACTIVE" status  
✅ Test invocations return responses  
✅ Memory persists across sessions  
✅ Gateway connects to APIs  
✅ Logs appear in CloudWatch  

## 🧹 Cleanup

Remove all resources:
```bash
./cleanup_agentcore.sh
```

## 📞 Support

- **AgentCore Docs**: https://aws.github.io/bedrock-agentcore-starter-toolkit/
- **Strands Docs**: https://docs.strands.ai/
- **AWS Support**: https://console.aws.amazon.com/support/

## 🎓 Learning Path

1. **Start**: [GETTING_STARTED.md](GETTING_STARTED.md)
2. **API Keys**: [API_KEYS_GUIDE.md](API_KEYS_GUIDE.md)
3. **Deploy**: [AGENTCORE_QUICKSTART.md](AGENTCORE_QUICKSTART.md)
4. **Deep Dive**: [AGENTCORE_DEPLOYMENT_GUIDE.md](AGENTCORE_DEPLOYMENT_GUIDE.md)

## 🚀 Next Steps

After deployment:

1. Update frontend to use deployed agents
2. Deploy frontend to S3/CloudFront
3. Add payment processing (Stripe/PayPal)
4. Implement email notifications (SES)
5. Add multi-language support
6. Build mobile app

## ✨ Features

- ✅ Serverless deployment (no infrastructure management)
- ✅ Auto-scaling (handles traffic spikes)
- ✅ Memory persistence (conversation context)
- ✅ Real-world APIs (live flight/hotel data)
- ✅ Secure authentication (Cognito OAuth 2.0)
- ✅ Multi-agent coordination (A2A protocol)
- ✅ Production-ready (monitoring, logging, error handling)

## 📜 License

MIT License - See LICENSE file for details

---

**Ready to deploy? Start with [GETTING_STARTED.md](GETTING_STARTED.md)!**

**May this system help many pilgrims plan their blessed journey! 🕋**
