# Using Amazon Bedrock Models

This guide explains how to use Amazon Bedrock models instead of direct API calls to OpenAI/Anthropic.

## Why Use Bedrock?

### ✅ Advantages

1. **Single AWS Bill** - Everything in one place
2. **No Separate API Keys** - Just AWS credentials
3. **Better Integration** - Native AWS service with AgentCore
4. **Enterprise Features** - VPC, CloudWatch, IAM, encryption
5. **Cost-Effective** - Often 20-40% cheaper than direct APIs
6. **Model Choice** - Access to multiple providers (Anthropic, Meta, Amazon, Mistral, Cohere)
7. **Compliance** - AWS compliance certifications
8. **Data Privacy** - Data stays in your AWS account

### ❌ When to Use Direct APIs

- You already have credits with OpenAI/Anthropic
- You need features not yet in Bedrock
- You're developing outside AWS

## Available Bedrock Models

### Anthropic Claude (Recommended)

**Claude 3.7 Sonnet** (Latest, most capable)
- Model ID: `us.anthropic.claude-3-7-sonnet-20250219-v1:0`
- Best for: Complex reasoning, orchestration
- Input: $3/M tokens | Output: $15/M tokens
- Context: 200K tokens

**Claude 3.5 Sonnet v2** (Fast, capable)
- Model ID: `us.anthropic.claude-3-5-sonnet-20241022-v2:0`
- Best for: General tasks, good balance
- Input: $3/M tokens | Output: $15/M tokens
- Context: 200K tokens

**Claude 3 Haiku** (Fastest, cheapest)
- Model ID: `us.anthropic.claude-3-haiku-20240307-v1:0`
- Best for: Simple tasks, high volume
- Input: $0.25/M tokens | Output: $1.25/M tokens
- Context: 200K tokens

### Meta Llama (Open Source)

**Llama 3.3 70B Instruct** (Cost-effective)
- Model ID: `us.meta.llama3-3-70b-instruct-v1:0`
- Best for: General tasks, budget-conscious
- Input: $0.99/M tokens | Output: $0.99/M tokens
- Context: 128K tokens

**Llama 3.1 405B Instruct** (Most capable Llama)
- Model ID: `us.meta.llama3-1-405b-instruct-v1:0`
- Best for: Complex reasoning
- Input: $5.32/M tokens | Output: $16/M tokens
- Context: 128K tokens

### Amazon Nova (AWS Native)

**Nova Pro** (Multimodal)
- Model ID: `us.amazon.nova-pro-v1:0`
- Best for: Text and image understanding
- Input: $0.80/M tokens | Output: $3.20/M tokens
- Context: 300K tokens

**Nova Lite** (Fast, cheap)
- Model ID: `us.amazon.nova-lite-v1:0`
- Best for: Simple tasks, high throughput
- Input: $0.06/M tokens | Output: $0.24/M tokens
- Context: 300K tokens

### Mistral AI

**Mistral Large 2** (Multilingual)
- Model ID: `mistral.mistral-large-2407-v1:0`
- Best for: Multilingual tasks
- Input: $3/M tokens | Output: $9/M tokens
- Context: 128K tokens

## Recommended Configuration

### Option 1: All Claude 3.7 Sonnet (Best Quality)

```bash
ORCHESTRATOR_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
FLIGHT_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
HOTEL_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
VISA_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
ITINERARY_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
```

**Cost per 1000 invocations**: ~$30-50  
**Best for**: Production, high quality

### Option 2: Mixed (Best Value)

```bash
# Complex reasoning - use Claude 3.7 Sonnet
ORCHESTRATOR_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
ITINERARY_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0

# Structured tasks - use Claude 3.5 Sonnet
FLIGHT_AGENT_MODEL=us.anthropic.claude-3-5-sonnet-20241022-v2:0
HOTEL_AGENT_MODEL=us.anthropic.claude-3-5-sonnet-20241022-v2:0

# Simple tasks - use Claude 3 Haiku
VISA_AGENT_MODEL=us.anthropic.claude-3-haiku-20240307-v1:0
```

**Cost per 1000 invocations**: ~$20-35  
**Best for**: Production, cost-conscious

### Option 3: Budget (Lowest Cost)

```bash
# Orchestrator needs good reasoning
ORCHESTRATOR_MODEL=us.anthropic.claude-3-5-sonnet-20241022-v2:0

# All others use Llama 3.3 (open source, cheap)
FLIGHT_AGENT_MODEL=us.meta.llama3-3-70b-instruct-v1:0
HOTEL_AGENT_MODEL=us.meta.llama3-3-70b-instruct-v1:0
VISA_AGENT_MODEL=us.meta.llama3-3-70b-instruct-v1:0
ITINERARY_AGENT_MODEL=us.meta.llama3-3-70b-instruct-v1:0
```

**Cost per 1000 invocations**: ~$10-20  
**Best for**: Development, testing

### Option 4: AWS Native (Amazon Nova)

```bash
# Use Amazon's own models
ORCHESTRATOR_MODEL=us.amazon.nova-pro-v1:0
FLIGHT_AGENT_MODEL=us.amazon.nova-pro-v1:0
HOTEL_AGENT_MODEL=us.amazon.nova-pro-v1:0
VISA_AGENT_MODEL=us.amazon.nova-lite-v1:0
ITINERARY_AGENT_MODEL=us.amazon.nova-pro-v1:0
```

**Cost per 1000 invocations**: ~$8-15  
**Best for**: AWS-first strategy, multimodal needs

## Setup: Enable Bedrock Models

### Step 1: Enable Model Access

1. Go to AWS Console: https://console.aws.amazon.com/bedrock/
2. Navigate to **"Model access"** in left sidebar
3. Click **"Manage model access"**
4. Select models you want to use:
   - ✅ Anthropic Claude 3.7 Sonnet
   - ✅ Anthropic Claude 3.5 Sonnet
   - ✅ Anthropic Claude 3 Haiku
   - ✅ Meta Llama 3.3 70B
   - ✅ Amazon Nova Pro
   - ✅ Amazon Nova Lite
5. Click **"Request model access"**
6. Wait for approval (usually instant for most models)

### Step 2: Verify Access

```bash
# List available models
aws bedrock list-foundation-models --region us-west-2

# Test a specific model
aws bedrock-runtime invoke-model \
  --model-id us.anthropic.claude-3-7-sonnet-20250219-v1:0 \
  --body '{"anthropic_version":"bedrock-2023-05-31","messages":[{"role":"user","content":"Hello"}],"max_tokens":100}' \
  --region us-west-2 \
  output.json

cat output.json
```

### Step 3: Update Agent Code

The agent code already uses Bedrock! Just ensure you're using the Strands framework with Bedrock model IDs:

```python
from strands import Agent

agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",  # Bedrock model ID
    system_prompt="You are a helpful assistant",
)

# Strands automatically uses Bedrock when it sees the model ID format
response = agent("Hello!")
```

### Step 4: No API Keys Needed!

Remove these from your `.env`:
```bash
# ❌ NOT NEEDED with Bedrock
# OPENAI_API_KEY=...
# ANTHROPIC_API_KEY=...
```

Keep only:
```bash
# ✅ NEEDED
AWS_REGION=us-west-2
AWS_ACCOUNT_ID=123456789012

# Model IDs (Bedrock)
ORCHESTRATOR_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
FLIGHT_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
# ... etc
```

## Cost Comparison

### Example: 1000 Agent Invocations

Assuming average of 2000 input tokens + 500 output tokens per invocation:

**All Claude 3.7 Sonnet (Bedrock)**
- Input: 2M tokens × $3 = $6
- Output: 0.5M tokens × $15 = $7.50
- **Total: $13.50**

**All GPT-4o (OpenAI Direct)**
- Input: 2M tokens × $2.50 = $5
- Output: 0.5M tokens × $10 = $5
- **Total: $10**

**Mixed (Claude 3.7 + Haiku)**
- Orchestrator (20%): $2.70
- Other agents (80%): $2.00 (using Haiku)
- **Total: $4.70**

**All Llama 3.3 (Bedrock)**
- Input: 2M tokens × $0.99 = $1.98
- Output: 0.5M tokens × $0.99 = $0.50
- **Total: $2.48**

### Monthly Cost Estimates

**Development (100 invocations/day)**
- Claude 3.7: ~$40/month
- Mixed: ~$15/month
- Llama 3.3: ~$7/month

**Production (1000 invocations/day)**
- Claude 3.7: ~$400/month
- Mixed: ~$150/month
- Llama 3.3: ~$75/month

## Model Selection Guide

### By Agent Type

**Orchestrator Agent** (Complex reasoning)
- Best: Claude 3.7 Sonnet
- Good: Claude 3.5 Sonnet
- Budget: Llama 3.3 70B

**Flight Agent** (Structured API calls)
- Best: Claude 3.5 Sonnet
- Good: Claude 3 Haiku
- Budget: Llama 3.3 70B

**Hotel Agent** (Structured API calls)
- Best: Claude 3.5 Sonnet
- Good: Claude 3 Haiku
- Budget: Nova Pro

**Visa Agent** (Simple lookups)
- Best: Claude 3 Haiku
- Good: Nova Lite
- Budget: Llama 3.3 70B

**Itinerary Agent** (Creative planning)
- Best: Claude 3.7 Sonnet
- Good: Claude 3.5 Sonnet
- Budget: Llama 3.3 70B

## Regional Availability

### US Regions (Recommended)
- `us-west-2` (Oregon) - All models
- `us-east-1` (Virginia) - All models

### Other Regions
- `eu-west-1` (Ireland) - Most models
- `ap-southeast-1` (Singapore) - Most models
- `ap-northeast-1` (Tokyo) - Most models

**Note:** Model availability varies by region. Check: https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html

## Switching from Direct APIs to Bedrock

### If You're Currently Using OpenAI

**Before:**
```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)
```

**After (with Strands + Bedrock):**
```python
from strands import Agent

agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0"
)
response = agent("Hello")
```

### If You're Currently Using Anthropic

**Before:**
```python
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    messages=[{"role": "user", "content": "Hello"}]
)
```

**After (with Strands + Bedrock):**
```python
from strands import Agent

agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0"  # Note the "us." prefix
)
response = agent("Hello")
```

## Testing Different Models

```bash
# Test Claude 3.7 Sonnet
agentcore invoke '{"prompt": "Hello"}' --agent umrah-orchestrator

# Update .env to use Llama
# ORCHESTRATOR_MODEL=us.meta.llama3-3-70b-instruct-v1:0

# Redeploy
agentcore launch --agent umrah-orchestrator --auto-update-on-conflict

# Test again
agentcore invoke '{"prompt": "Hello"}' --agent umrah-orchestrator
```

## Best Practices

### 1. Start with Claude 3.7 Sonnet
- Highest quality
- Test and validate functionality
- Optimize later if needed

### 2. Profile Your Usage
- Monitor CloudWatch metrics
- Track token usage per agent
- Identify optimization opportunities

### 3. Use Appropriate Models
- Complex reasoning → Claude 3.7/3.5 Sonnet
- Structured tasks → Claude 3 Haiku
- High volume → Llama 3.3 or Nova Lite

### 4. Set Up Monitoring
```bash
# View Bedrock metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Bedrock \
  --metric-name Invocations \
  --dimensions Name=ModelId,Value=us.anthropic.claude-3-7-sonnet-20250219-v1:0 \
  --start-time 2026-02-01T00:00:00Z \
  --end-time 2026-02-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

### 5. Enable Cost Allocation Tags
```bash
# Tag your Bedrock usage
aws bedrock tag-resource \
  --resource-arn arn:aws:bedrock:us-west-2:123456789012:model/us.anthropic.claude-3-7-sonnet-20250219-v1:0 \
  --tags Key=Project,Value=UmrahTripCreator
```

## Troubleshooting

### "Model not found" Error
```bash
# Check model access
aws bedrock list-foundation-models --region us-west-2 | grep claude-3-7

# Request access in console
# https://console.aws.amazon.com/bedrock/ → Model access
```

### "Throttling" Error
```bash
# Check service quotas
aws service-quotas get-service-quota \
  --service-code bedrock \
  --quota-code L-1234567890

# Request quota increase if needed
```

### "Access Denied" Error
```bash
# Verify IAM permissions
aws iam get-user-policy \
  --user-name agentcore-deployer \
  --policy-name BedrockAccess

# Add Bedrock permissions if missing
```

## Summary

### ✅ Use Bedrock When:
- Deploying on AWS
- Want single billing
- Need enterprise features
- Cost optimization matters
- Data privacy is critical

### ❌ Use Direct APIs When:
- Already have API credits
- Developing locally (not on AWS)
- Need features not in Bedrock yet
- Working across multiple clouds

## Updated API Keys Guide

With Bedrock, you only need:

**Required:**
- ✅ AWS credentials (IAM user)

**Optional (for real data):**
- ✅ Amadeus API (flights)
- ✅ RapidAPI (hotels)

**NOT Needed:**
- ❌ OpenAI API key
- ❌ Anthropic API key

**Total cost to start: $0-20** (just API credits for Amadeus/Hotels if you want real data)

---

**Recommendation: Use Bedrock exclusively for the best AWS integration and cost optimization!**
