# Latest Bedrock Models (2025)

This guide covers the newest and most powerful models available in Amazon Bedrock as of February 2025.

## 🚀 Latest Claude Models (Anthropic)

### Claude Sonnet 4.5 (Recommended)
**Model ID:** `anthropic.claude-sonnet-4-5-20250929-v1:0`

**Released:** September 2025  
**Best for:** Production use, complex reasoning, general tasks  
**Context:** 200K tokens  
**Modalities:** Text + Image input, Text output  

**Capabilities:**
- ✅ Advanced reasoning and analysis
- ✅ Multimodal (text + images)
- ✅ Extended thinking mode
- ✅ Tool use and function calling
- ✅ Streaming support

**Pricing:** ~$3/M input tokens, ~$15/M output tokens

**Use for:**
- Orchestrator agent (complex coordination)
- Flight agent (structured API calls)
- Hotel agent (search and recommendations)
- Itinerary agent (creative planning)

### Claude Opus 4.5 (Most Capable)
**Model ID:** `anthropic.claude-opus-4-5-20251101-v1:0`

**Released:** November 2025  
**Best for:** Most complex tasks, highest quality  
**Context:** 200K tokens  
**Modalities:** Text + Image input, Text output  

**Capabilities:**
- ✅ Highest reasoning capability
- ✅ Best for complex analysis
- ✅ Superior code generation
- ✅ Advanced multimodal understanding

**Pricing:** ~$15/M input tokens, ~$75/M output tokens (5x Sonnet)

**Use for:**
- Orchestrator agent (when quality is critical)
- Complex itinerary planning
- Advanced reasoning tasks

### Claude Haiku 4.5 (Fast & Efficient)
**Model ID:** `anthropic.claude-haiku-4-5-20251001-v1:0`

**Released:** October 2025  
**Best for:** High-volume, simple tasks, cost optimization  
**Context:** 200K tokens  
**Modalities:** Text + Image input, Text output  

**Capabilities:**
- ✅ Fastest response times
- ✅ Most cost-effective
- ✅ Still very capable
- ✅ Multimodal support

**Pricing:** ~$0.25/M input tokens, ~$1.25/M output tokens (12x cheaper than Sonnet)

**Use for:**
- Visa agent (simple lookups)
- High-volume API calls
- Simple structured tasks

### Claude Opus 4.1
**Model ID:** `anthropic.claude-opus-4-1-20250805-v1:0`

**Released:** August 2025  
**Best for:** Alternative to Opus 4.5, slightly older  
**Context:** 200K tokens  

**Pricing:** ~$15/M input tokens, ~$75/M output tokens

### Claude Sonnet 4
**Model ID:** `anthropic.claude-sonnet-4-20250514-v1:0`

**Released:** May 2025  
**Best for:** Alternative to Sonnet 4.5, slightly older  
**Context:** 200K tokens  

**Pricing:** ~$3/M input tokens, ~$15/M output tokens

---

## 🆕 Amazon Nova 2 (Latest AWS Native)

### Nova 2 Lite (Multimodal)
**Model ID:** `amazon.nova-2-lite-v1:0`

**Released:** 2025  
**Best for:** Fast multimodal tasks, cost-effective  
**Context:** 300K tokens  
**Modalities:** Text + Image + Video input, Text output  

**Capabilities:**
- ✅ Video understanding
- ✅ Image analysis
- ✅ Fast inference
- ✅ Cost-effective

**Pricing:** ~$0.06/M input tokens, ~$0.24/M output tokens (25x cheaper than Claude!)

**Use for:**
- High-volume tasks
- Budget-conscious deployments
- Multimodal needs

### Nova Premier (Most Capable Nova)
**Model ID:** `amazon.nova-premier-v1:0`

**Released:** 2025  
**Best for:** Complex multimodal tasks  
**Context:** 300K tokens  
**Modalities:** Text + Image + Video input, Text output  

**Capabilities:**
- ✅ Advanced reasoning
- ✅ Video understanding
- ✅ Complex analysis
- ✅ AWS-optimized

**Pricing:** ~$2/M input tokens, ~$8/M output tokens

**Use for:**
- Orchestrator agent (AWS-first strategy)
- Multimodal applications
- Video/image analysis

### Nova 2 Sonic (Speech)
**Model ID:** `amazon.nova-2-sonic-v1:0`

**Released:** 2025  
**Best for:** Speech-to-speech applications  
**Modalities:** Speech input, Speech + Text output  

**Use for:**
- Voice interfaces
- Speech translation
- Audio processing

---

## 🧠 DeepSeek Models (Reasoning)

### DeepSeek-R1 (Reasoning Model)
**Model ID:** `deepseek.r1-v1:0`

**Released:** 2025  
**Best for:** Complex reasoning, mathematical problems  
**Context:** 128K tokens  
**Modalities:** Text input, Text output  

**Capabilities:**
- ✅ Advanced reasoning
- ✅ Mathematical problem solving
- ✅ Step-by-step thinking
- ✅ Code generation

**Pricing:** ~$0.55/M input tokens, ~$2.19/M output tokens

**Use for:**
- Complex problem solving
- Mathematical calculations
- Logical reasoning tasks

### DeepSeek-V3.1
**Model ID:** `deepseek.v3-v1:0`

**Released:** 2025  
**Best for:** General tasks, cost-effective  
**Context:** 128K tokens  

**Pricing:** ~$0.27/M input tokens, ~$1.10/M output tokens

---

## 🦙 Meta Llama (Open Source)

### Llama 3.3 70B Instruct
**Model ID:** `meta.llama3-3-70b-instruct-v1:0`

**Best for:** Cost-effective general tasks  
**Context:** 128K tokens  
**Modalities:** Text input, Text output  

**Pricing:** ~$0.99/M input tokens, ~$0.99/M output tokens

**Use for:**
- Budget deployments
- High-volume tasks
- Open-source preference

### Llama 3.1 405B Instruct
**Model ID:** `meta.llama3-1-405b-instruct-v1:0`

**Best for:** Most capable Llama model  
**Context:** 128K tokens  

**Pricing:** ~$5.32/M input tokens, ~$16/M output tokens

---

## 📊 Model Comparison

### By Capability (Best to Good)

**Most Capable:**
1. Claude Opus 4.5
2. Claude Opus 4.1
3. Claude Sonnet 4.5
4. Nova Premier
5. Llama 3.1 405B

**Best Balance (Quality/Cost):**
1. Claude Sonnet 4.5 ⭐ **Recommended**
2. Claude Sonnet 4
3. Nova Premier
4. DeepSeek-R1

**Most Cost-Effective:**
1. Nova 2 Lite ($0.06/M)
2. DeepSeek-V3.1 ($0.27/M)
3. Llama 3.3 70B ($0.99/M)
4. Claude Haiku 4.5 ($0.25/M)

### By Speed (Fastest to Slowest)

1. Claude Haiku 4.5
2. Nova 2 Lite
3. Claude Sonnet 4.5
4. Nova Premier
5. Claude Opus 4.5

### By Context Window

1. Nova models: 300K tokens
2. Claude models: 200K tokens
3. Llama/DeepSeek: 128K tokens

---

## 🎯 Recommended Configurations

### Option 1: Latest & Greatest (Best Quality)

```bash
# All Claude Sonnet 4.5
ORCHESTRATOR_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
FLIGHT_AGENT_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
HOTEL_AGENT_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
VISA_AGENT_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
ITINERARY_AGENT_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
```

**Cost per 1000 invocations:** ~$30-50  
**Best for:** Production, high quality, latest features

### Option 2: Mixed (Best Value)

```bash
# Complex reasoning - Sonnet 4.5
ORCHESTRATOR_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
ITINERARY_AGENT_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0

# Structured tasks - Sonnet 4.5
FLIGHT_AGENT_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
HOTEL_AGENT_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0

# Simple tasks - Haiku 4.5
VISA_AGENT_MODEL=anthropic.claude-haiku-4-5-20251001-v1:0
```

**Cost per 1000 invocations:** ~$25-40  
**Best for:** Production, cost-conscious

### Option 3: AWS Native (Nova 2)

```bash
# Use latest Amazon Nova models
ORCHESTRATOR_MODEL=amazon.nova-premier-v1:0
FLIGHT_AGENT_MODEL=amazon.nova-premier-v1:0
HOTEL_AGENT_MODEL=amazon.nova-premier-v1:0
VISA_AGENT_MODEL=amazon.nova-2-lite-v1:0
ITINERARY_AGENT_MODEL=amazon.nova-premier-v1:0
```

**Cost per 1000 invocations:** ~$15-25  
**Best for:** AWS-first strategy, multimodal needs, cost optimization

### Option 4: Maximum Performance

```bash
# Use Opus 4.5 for everything (expensive!)
ORCHESTRATOR_MODEL=anthropic.claude-opus-4-5-20251101-v1:0
FLIGHT_AGENT_MODEL=anthropic.claude-opus-4-5-20251101-v1:0
HOTEL_AGENT_MODEL=anthropic.claude-opus-4-5-20251101-v1:0
VISA_AGENT_MODEL=anthropic.claude-opus-4-5-20251101-v1:0
ITINERARY_AGENT_MODEL=anthropic.claude-opus-4-5-20251101-v1:0
```

**Cost per 1000 invocations:** ~$150-250  
**Best for:** Maximum quality, research, demos

### Option 5: Budget (Lowest Cost)

```bash
# Use Nova 2 Lite for everything
ORCHESTRATOR_MODEL=amazon.nova-2-lite-v1:0
FLIGHT_AGENT_MODEL=amazon.nova-2-lite-v1:0
HOTEL_AGENT_MODEL=amazon.nova-2-lite-v1:0
VISA_AGENT_MODEL=amazon.nova-2-lite-v1:0
ITINERARY_AGENT_MODEL=amazon.nova-2-lite-v1:0
```

**Cost per 1000 invocations:** ~$2-5  
**Best for:** Development, testing, high-volume

---

## 🆚 Why Use Latest Models?

### Claude Sonnet 4.5 vs 3.7 Sonnet

**Improvements:**
- ✅ Better reasoning capabilities
- ✅ Improved multimodal understanding
- ✅ Extended thinking mode
- ✅ Better tool use
- ✅ More accurate responses
- ✅ Same pricing!

**Migration:** Just update model ID, no code changes needed

### Nova 2 vs Nova 1

**Improvements:**
- ✅ Video understanding (new!)
- ✅ Better image analysis
- ✅ Faster inference
- ✅ Larger context (300K vs 200K)
- ✅ Lower cost

---

## 🔄 Migration Guide

### From Claude 3.7 to Sonnet 4.5

**Before:**
```bash
ORCHESTRATOR_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
```

**After:**
```bash
ORCHESTRATOR_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
```

**Changes needed:** None! Just update the model ID.

### From Nova 1 to Nova 2

**Before:**
```bash
HOTEL_AGENT_MODEL=amazon.nova-pro-v1:0
```

**After:**
```bash
HOTEL_AGENT_MODEL=amazon.nova-premier-v1:0
```

**Changes needed:** None! API is compatible.

---

## 📍 Regional Availability

### Claude Sonnet 4.5
Available in: **30+ regions** including:
- us-east-1, us-east-2, us-west-1, us-west-2
- eu-central-1, eu-west-1, eu-west-2, eu-west-3
- ap-northeast-1, ap-southeast-1, ap-southeast-2
- ca-central-1, sa-east-1, me-central-1

### Nova 2 Lite
Available via **cross-region inference** in 25+ regions

### DeepSeek R1
Available in: us-east-1, us-east-2, us-west-2

---

## 🎓 Best Practices

### 1. Start with Sonnet 4.5
- Latest features
- Best balance of quality/cost
- Widely available
- Production-ready

### 2. Use Haiku 4.5 for Simple Tasks
- Visa lookups
- Simple API calls
- High-volume operations
- 12x cheaper than Sonnet

### 3. Consider Nova 2 for Multimodal
- If you need video/image understanding
- AWS-first strategy
- Cost optimization
- Larger context window

### 4. Reserve Opus 4.5 for Critical Tasks
- Only when quality is paramount
- Complex reasoning required
- Budget allows 5x cost

### 5. Test Before Deploying
```bash
# Test Sonnet 4.5
agentcore invoke '{"prompt": "Hello"}' --agent umrah-orchestrator

# Compare with Haiku 4.5
# Update .env: ORCHESTRATOR_MODEL=anthropic.claude-haiku-4-5-20251001-v1:0
agentcore launch --agent umrah-orchestrator --auto-update-on-conflict
agentcore invoke '{"prompt": "Hello"}' --agent umrah-orchestrator
```

---

## 💰 Cost Comparison (1000 Invocations)

Assuming 2000 input + 500 output tokens per invocation:

| Configuration | Input Cost | Output Cost | Total |
|--------------|------------|-------------|-------|
| All Opus 4.5 | $30 | $37.50 | **$67.50** |
| All Sonnet 4.5 | $6 | $7.50 | **$13.50** |
| Mixed (Sonnet + Haiku) | $5 | $6 | **$11** |
| All Haiku 4.5 | $0.50 | $0.63 | **$1.13** |
| All Nova Premier | $4 | $4 | **$8** |
| All Nova 2 Lite | $0.12 | $0.12 | **$0.24** |
| All DeepSeek R1 | $1.10 | $1.10 | **$2.20** |

---

## 🚀 Quick Update Command

```bash
# Update .env with latest models
cat > .env << 'EOF'
AWS_REGION=us-west-2
AWS_ACCOUNT_ID=your-account-id

# Latest Claude Sonnet 4.5 (Recommended)
ORCHESTRATOR_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
FLIGHT_AGENT_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
HOTEL_AGENT_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
VISA_AGENT_MODEL=anthropic.claude-haiku-4-5-20251001-v1:0
ITINERARY_AGENT_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
EOF

# Redeploy all agents
./deploy_to_agentcore.sh
```

---

## ✅ Summary

**Use Claude Sonnet 4.5 for:**
- ✅ Production deployments
- ✅ Best quality/cost balance
- ✅ Latest features
- ✅ General recommendation

**Use Claude Haiku 4.5 for:**
- ✅ Simple tasks
- ✅ High-volume operations
- ✅ Cost optimization
- ✅ Fast responses

**Use Nova 2 for:**
- ✅ Multimodal needs
- ✅ AWS-first strategy
- ✅ Maximum cost savings
- ✅ Large context windows

**Use Opus 4.5 for:**
- ✅ Maximum quality
- ✅ Complex reasoning
- ✅ Critical applications
- ✅ When budget allows

---

**Recommendation: Start with Claude Sonnet 4.5 for all agents, then optimize based on your specific needs and budget!**
