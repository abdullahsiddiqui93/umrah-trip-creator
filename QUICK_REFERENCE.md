# Quick Reference - Umrah Trip Creator on AgentCore

## Agent ARNs (Copy-Paste Ready)

```bash
# Orchestrator
arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo

# Flight Agent
arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_flight_agent-ufM0XiC3fw

# Hotel Agent
arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_hotel_agent-P3Am0WF25G

# Visa Agent
arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_visa_agent-KR3L9yDFDl

# Itinerary Agent
arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_itinerary_agent-1XwH666geK
```

## Common Commands

### Test an Agent
```bash
cd agents/<agent_directory>
source ../../.venv/bin/activate
agentcore invoke '{"prompt": "Your question here"}' --agent <agent_name>
```

### Check Status
```bash
agentcore status --agent <agent_name>
```

### View Logs
```bash
aws logs tail /aws/bedrock-agentcore/runtimes/<agent-id>-DEFAULT --since 5m
```

### Redeploy After Changes
```bash
cd agents/<agent_directory>
source ../../.venv/bin/activate
agentcore deploy --agent <agent_name> --auto-update-on-conflict
```

### Destroy an Agent
```bash
cd agents/<agent_directory>
source ../../.venv/bin/activate
agentcore destroy --agent <agent_name>
```

## Environment Variables (.env)

```bash
# AWS
AWS_REGION=us-west-2
AWS_ACCOUNT_ID=985444479029

# Models (Claude 3.5)
ORCHESTRATOR_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
FLIGHT_AGENT_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
HOTEL_AGENT_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
VISA_AGENT_MODEL=anthropic.claude-3-5-haiku-20241022-v1:0
ITINERARY_AGENT_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0

# Memory
MEMORY_STM_ID=UmrahTrip_STM_904e3a89-42bqoi6aBl
MEMORY_LTM_ID=UmrahTrip_LTM_22d963c0-n4uMLy61a6

# Gateway
GATEWAY_URL=https://umrahtrip-gateway-95c76ff1-zlwkpbuhif.gateway.bedrock-agentcore.us-west-2.amazonaws.com/mcp
GATEWAY_ID=umrahtrip-gateway-95c76ff1-zlwkpbuhif

# Cognito
COGNITO_USER_POOL_ID=us-west-2_AAvuQJ0g6
COGNITO_CLIENT_ID=63dp8fgl22r9h2rmdhpdtajvni
```

## Test Prompts

### Orchestrator
```json
{"prompt": "Hello, I want to plan an Umrah trip for 2 people from New York in March 2026"}
```

### Flight Agent
```json
{"prompt": "Find me round-trip flights from New York to Jeddah for 2 passengers, departing March 15, 2026"}
```

### Hotel Agent
```json
{"prompt": "Find hotels in Makkah within 500m of Masjid al-Haram for 7 nights starting March 15"}
```

### Visa Agent
```json
{"prompt": "What are the Umrah visa requirements for US citizens? What documents do I need?"}
```

### Itinerary Agent
```json
{"prompt": "Create a detailed 7-day Umrah itinerary including all rituals and recommended activities"}
```

## Useful AWS Console Links

- **AgentCore Console**: https://console.aws.amazon.com/bedrock-agentcore/
- **CloudWatch Logs**: https://console.aws.amazon.com/cloudwatch/home?region=us-west-2#logsV2:log-groups
- **GenAI Dashboard**: https://console.aws.amazon.com/cloudwatch/home?region=us-west-2#gen-ai-observability/agent-core
- **IAM Roles**: https://console.aws.amazon.com/iam/home?region=us-west-2#/roles
- **S3 Buckets**: https://s3.console.aws.amazon.com/s3/buckets?region=us-west-2

## File Structure

```
umrah-trip-creator/
├── .env                          # Environment variables
├── agents/
│   ├── orchestrator/
│   │   ├── orchestrator_runtime.py
│   │   ├── requirements.txt
│   │   └── .bedrock_agentcore.yaml
│   ├── flight_agent/
│   │   ├── flight_runtime.py
│   │   ├── requirements.txt
│   │   └── .bedrock_agentcore.yaml
│   ├── hotel_agent/
│   │   ├── hotel_runtime.py
│   │   ├── requirements.txt
│   │   └── .bedrock_agentcore.yaml
│   ├── visa_agent/
│   │   ├── visa_runtime.py
│   │   ├── requirements.txt
│   │   └── .bedrock_agentcore.yaml
│   └── itinerary_agent/
│       ├── itinerary_runtime.py
│       ├── requirements.txt
│       └── .bedrock_agentcore.yaml
├── frontend/
│   └── streamlit_app.py          # Needs update to use deployed agents
├── DEPLOYMENT_COMPLETE.md        # Full deployment documentation
├── DEPLOYMENT_STATUS.md          # Troubleshooting guide
└── QUICK_REFERENCE.md            # This file
```

## Emergency Commands

### Stop All Agents
```bash
for agent in umrah_orchestrator umrah_flight_agent umrah_hotel_agent umrah_visa_agent umrah_itinerary_agent; do
    echo "Destroying $agent..."
    cd agents/$(echo $agent | sed 's/umrah_//' | sed 's/_agent//')
    echo "y" | agentcore destroy --agent $agent
    cd ../..
done
```

### Check All Agent Status
```bash
for agent in umrah_orchestrator umrah_flight_agent umrah_hotel_agent umrah_visa_agent umrah_itinerary_agent; do
    echo "=== $agent ==="
    agentcore status --agent $agent 2>&1 | grep -E "Ready|Error|Agent ARN"
    echo ""
done
```

### View All Recent Logs
```bash
for agent_id in DFFg1bHZKo ufM0XiC3fw P3Am0WF25G KR3L9yDFDl 1XwH666geK; do
    echo "=== Logs for $agent_id ==="
    aws logs tail /aws/bedrock-agentcore/runtimes/*-${agent_id}-DEFAULT --since 5m 2>&1 | tail -20
    echo ""
done
```

## Pricing Calculator

### Per Invocation Cost Estimate
- Runtime: ~$0.0001 per invocation
- Bedrock (Claude 3.5 Sonnet): ~$0.003 per 1K input tokens, ~$0.015 per 1K output tokens
- Average conversation: ~2K input + 1K output = ~$0.021

### Monthly Cost Examples
- **100 conversations/month**: ~$2-5
- **1,000 conversations/month**: ~$20-50
- **10,000 conversations/month**: ~$200-500

*Plus CloudWatch logs (~$0.50/GB) and S3 storage (minimal)*
