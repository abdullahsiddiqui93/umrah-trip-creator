# Next Steps - Quick Reference

Your `.env` file is configured correctly! Here's exactly what to do next.

## ✅ What's Already Done

- ✅ AWS credentials configured
- ✅ `.env` file created with API keys
- ✅ Amadeus API configured
- ✅ RapidAPI (hotels) configured
- ✅ Latest Bedrock models selected
- ✅ Agent runtime files created

## 🚀 Step-by-Step Deployment

### Step 1: Install AgentCore CLI (5 minutes)

```bash
# Activate virtual environment (if not already)
source .venv/bin/activate

# Install AgentCore toolkit
pip install bedrock-agentcore-starter-toolkit bedrock-agentcore strands-agents

# Verify installation
agentcore --version
```

Expected output: `agentcore, version X.X.X`

### Step 2: Enable Bedrock Models (2 minutes)

**Important:** You must enable model access in AWS Console first!

1. Open: https://console.aws.amazon.com/bedrock/
2. Click **"Model access"** (left sidebar)
3. Click **"Manage model access"** (orange button)
4. Check these boxes:
   - ✅ **Anthropic Claude Sonnet 4.5**
   - ✅ **Anthropic Claude Haiku 4.5**
   - ✅ **Anthropic Claude Opus 4.5** (optional)
5. Click **"Request model access"** (bottom right)
6. Wait 10-30 seconds for approval

**Verify access:**
```bash
aws bedrock list-foundation-models --region us-west-2 --query "modelSummaries[?contains(modelId, 'claude-sonnet-4-5')]" --output table
```

Should show Claude Sonnet 4.5 model.

### Step 3: Set Up Memory (2 minutes)

```bash
# Create AgentCore Memory resources
python3 setup_memory.py
```

**Expected output:**
```
Creating memory resources for Umrah Trip Creator...
✅ STM Memory Created: mem-abc123xyz
✅ LTM Memory Created: mem-def456uvw

Add these to your .env file:
MEMORY_STM_ID=mem-abc123xyz
MEMORY_LTM_ID=mem-def456uvw
```

**Action required:**
1. Copy the memory IDs from the output
2. Edit `.env` file:
   ```bash
   nano .env
   ```
3. Replace these lines:
   ```bash
   MEMORY_STM_ID=mem-abc123xyz  # ← Paste your actual ID
   MEMORY_LTM_ID=mem-def456uvw  # ← Paste your actual ID
   ```
4. Save and close (Ctrl+X, Y, Enter)

### Step 4: Set Up Gateway (3 minutes)

```bash
# Create AgentCore Gateway with API targets
python3 setup_gateway.py
```

**Expected output:**
```
Creating AgentCore Gateway for Umrah Trip Creator
✅ Authorization server created
✅ Gateway created: https://gateway-xyz.execute-api.us-west-2.amazonaws.com
✅ IAM permissions configured
✅ Access token obtained
✅ Amadeus Flight API target added
✅ RapidAPI Hotel target added
✅ Visa Processing Lambda target added

Add these to your .env file:
GATEWAY_URL=https://gateway-xyz.execute-api.us-west-2.amazonaws.com
GATEWAY_ID=gateway-xyz
GATEWAY_ACCESS_TOKEN=eyJhbGc...
COGNITO_USER_POOL_ID=us-west-2_abc123
COGNITO_CLIENT_ID=client-xyz
COGNITO_CLIENT_SECRET=secret-abc
```

**Action required:**
1. Copy ALL the values from the output
2. Edit `.env` file:
   ```bash
   nano .env
   ```
3. Replace these lines with your actual values:
   ```bash
   GATEWAY_URL=https://gateway-xyz...  # ← Paste actual URL
   GATEWAY_ID=gateway-xyz  # ← Paste actual ID
   GATEWAY_ACCESS_TOKEN=eyJhbGc...  # ← Paste actual token
   COGNITO_USER_POOL_ID=us-west-2_abc123  # ← Paste actual pool ID
   COGNITO_CLIENT_ID=client-xyz  # ← Paste actual client ID
   COGNITO_CLIENT_SECRET=secret-abc  # ← Paste actual secret
   ```
4. Save and close

### Step 5: Deploy All Agents (30-50 minutes)

```bash
# Run automated deployment
./deploy_to_agentcore.sh
```

**What happens:**
1. Validates prerequisites (1 min)
2. Deploys orchestrator agent (5-10 min)
3. Deploys flight agent (5-10 min)
4. Deploys hotel agent (5-10 min)
5. Deploys visa agent (5-10 min)
6. Deploys itinerary agent (5-10 min)
7. Tests deployment (1 min)

**Expected output:**
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

... (continues for all agents)

==========================================
✅ Deployment Complete!
==========================================
```

**Note:** This takes 30-50 minutes because AWS builds container images in the cloud.

### Step 6: Test Your Deployment (5 minutes)

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

# Wait for memory extraction
sleep 10

agentcore invoke '{"prompt": "What are my preferences?"}' \
  --agent umrah-orchestrator --session-id test-123
```

**Expected:** Agent responds with helpful information about planning Umrah trips.

## 🎯 Quick Command Reference

### Check Agent Status
```bash
agentcore status --agent umrah-orchestrator --verbose
```

### View Logs
```bash
aws logs tail /aws/bedrock-agentcore/umrah-orchestrator --follow
```

### Redeploy After Changes
```bash
agentcore launch --agent umrah-orchestrator --auto-update-on-conflict
```

### Stop a Session
```bash
agentcore stop-session --agent umrah-orchestrator --session-id <session-id>
```

### List All Agents
```bash
agentcore configure list
```

## ⚠️ Common Issues

### Issue: "Model not found"
**Solution:** Enable model access in Bedrock console (Step 2)

### Issue: "Access Denied"
**Solution:** Check IAM permissions
```bash
aws sts get-caller-identity
```

### Issue: "Gateway connection failed"
**Solution:** Verify gateway config in `.env`
```bash
echo $GATEWAY_URL
```

### Issue: "Memory not persisting"
**Solution:** Wait 10 seconds after messages for extraction

## 📊 Monitoring

### CloudWatch Logs
```bash
# View orchestrator logs
aws logs tail /aws/bedrock-agentcore/umrah-orchestrator --follow

# View flight agent logs
aws logs tail /aws/bedrock-agentcore/umrah-flight-agent --follow
```

### Check Memory Usage
```bash
python3 << EOF
from bedrock_agentcore.memory import MemoryClient
import os

client = MemoryClient(region_name='us-west-2')
memory_id = os.getenv('MEMORY_LTM_ID')

memory = client.get_memory(memory_id=memory_id)
print(f"Memory: {memory['name']}")
print(f"Status: {memory['status']}")
EOF
```

### Check Gateway
```bash
agentcore gateway list-mcp-gateway-targets --id $GATEWAY_ID
```

## 🎉 Success Criteria

Your deployment is successful when:

✅ All 5 agents show "ACTIVE" status  
✅ Test invocations return responses  
✅ Memory persists across sessions  
✅ Gateway connects to APIs  
✅ Logs appear in CloudWatch  
✅ No error messages  

## 📞 Need Help?

If you get stuck:

1. Check this guide
2. Review error messages in logs
3. Verify all environment variables are set
4. Check AWS credentials are valid
5. Ensure Bedrock models are enabled

## 🧹 Clean Up (Optional)

To remove all resources:

```bash
./cleanup_agentcore.sh
```

---

**You're ready to deploy! Start with Step 1 above.** 🚀
