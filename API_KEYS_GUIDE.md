# API Keys Setup Guide (Bedrock Edition)

This guide shows you how to get the credentials needed for your Umrah Trip Creator using Amazon Bedrock.

## 🎯 Recommended Approach: Use Bedrock (Simplest!)

**Good news: You only need AWS credentials!**

The agents use **Amazon Bedrock** models by default, which means:
- ✅ **No OpenAI API key needed**
- ✅ **No Anthropic API key needed**
- ✅ Everything on your AWS bill
- ✅ Better AWS integration
- ✅ Often 20-40% cheaper

## Required vs Optional Keys

### ✅ Required (for basic deployment)
- **AWS Credentials** - For Bedrock models and AgentCore (FREE to set up)

### 🔧 Optional (for real-world data)
- **Amadeus API** - For real flight searches (FREE test tier)
- **Hotel API** - For real hotel searches (FREE tier available)

**Total cost to start: $0** (with free tiers!)

---

## 1. AWS Credentials (Required)

### Create AWS Account

1. Go to: https://aws.amazon.com/
2. Click **"Create an AWS Account"**
3. Fill in:
   - Email address
   - Password
   - AWS account name
4. Provide payment method (credit card - won't be charged for free tier)
5. Verify phone number
6. Choose support plan: **Basic (Free)**

### Create IAM User

1. Go to: https://console.aws.amazon.com/iam/
2. Click **"Users"** → **"Create user"**
3. Username: `agentcore-deployer`
4. Click **"Next"**
5. Attach policies:
   - `AdministratorAccess` (easiest for getting started)
   - Or custom policy with: `bedrock:*`, `iam:*`, `lambda:*`, `logs:*`, `s3:*`, `cognito-idp:*`
6. Click **"Create user"**

### Create Access Keys

1. Click on the user you just created
2. Go to **"Security credentials"** tab
3. Scroll to **"Access keys"**
4. Click **"Create access key"**
5. Choose **"Command Line Interface (CLI)"**
6. Check the confirmation box
7. Click **"Create access key"**
8. **Save both values**:
   - Access key ID (starts with `AKIA...`)
   - Secret access key (only shown once!)

### Configure AWS CLI

```bash
# Install AWS CLI if needed
# macOS: brew install awscli
# Windows: https://aws.amazon.com/cli/
# Linux: sudo apt install awscli

# Configure credentials
aws configure
```

Enter when prompted:
- AWS Access Key ID: `AKIA...`
- AWS Secret Access Key: `your-secret-key`
- Default region: `us-west-2`
- Default output format: `json`

### Verify Configuration

```bash
aws sts get-caller-identity
```

Should show your account ID and user ARN.

### Enable Bedrock Models

1. Go to: https://console.aws.amazon.com/bedrock/
2. Click **"Model access"** in left sidebar
3. Click **"Manage model access"**
4. Select these models (all free to enable):
   - ✅ **Anthropic Claude 3.7 Sonnet** (recommended)
   - ✅ **Anthropic Claude 3.5 Sonnet** (good balance)
   - ✅ **Anthropic Claude 3 Haiku** (fast & cheap)
   - ✅ **Meta Llama 3.3 70B** (open source, cheap)
   - ✅ **Amazon Nova Pro** (AWS native)
5. Click **"Request model access"**
6. Wait for approval (usually instant for these models)

### Add to .env

```bash
AWS_REGION=us-west-2
AWS_ACCOUNT_ID=123456789012  # From get-caller-identity output

# Model configuration (using Bedrock)
ORCHESTRATOR_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
FLIGHT_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
HOTEL_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
VISA_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
ITINERARY_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
```

**That's it! No LLM API keys needed.**

See **[BEDROCK_MODELS_GUIDE.md](BEDROCK_MODELS_GUIDE.md)** for:
- Model selection guide
- Cost optimization
- Alternative models (Llama, Nova, etc.)

---

## 2. Amadeus API (Optional - for real flight data)

### Sign Up (Free)

1. Go to: https://developers.amadeus.com/register
2. Click **"Register"**
3. Fill in:
   - Email
   - Company name (can use "Personal Project")
   - Country
4. Verify email

### Create App

1. Go to: https://developers.amadeus.com/my-apps
2. Click **"Create new app"**
3. Fill in:
   - App name: `Umrah Trip Creator`
   - Description: `Multi-agent system for Umrah trip planning`
4. Click **"Create"**

### Get API Credentials

1. In your app dashboard, you'll see:
   - **API Key** (Client ID)
   - **API Secret** (Client Secret)
2. Copy both values

### Test vs Production

**Test API** (Recommended to start)
- Base URL: `https://test.api.amadeus.com`
- **FREE**: 2,000 API calls/month
- Limited flight data (good for testing)

**Production API** (When ready for real users)
- Base URL: `https://api.amadeus.com`
- Requires billing setup
- Full flight inventory

### Add to .env

```bash
AMADEUS_API_KEY=your_api_key_here
AMADEUS_API_SECRET=your_api_secret_here
```

### Pricing (Production)
- Free tier: 2,000 calls/month
- Pay-as-you-go: $0.01-0.05 per API call
- Estimated: $10-50/month for moderate usage

---

## 3. Hotel API (Optional - for real hotel data)

### Option A: RapidAPI (Recommended - Easiest)

1. Go to: https://rapidapi.com/
2. Sign up (free account)
3. Search for "booking" or "hotels"
4. Popular options:
   - **Booking.com API**: https://rapidapi.com/apidojo/api/booking
   - **Hotels.com API**: https://rapidapi.com/apidojo/api/hotels4
   - **Priceline API**: https://rapidapi.com/davidtaoweiji/api/priceline-com-provider
5. Subscribe to an API:
   - **Free tier**: 100-500 calls/month
   - **Basic**: $10-50/month
   - **Pro**: $50-200/month
6. Copy your **RapidAPI Key**

### Add to .env

```bash
RAPIDAPI_KEY=your_rapidapi_key_here
HOTEL_API_ENDPOINT=https://booking-com.p.rapidapi.com
```

### Option B: Amadeus Hotel API (If you have Amadeus)

If you already have Amadeus credentials, you can use their hotel API too:

```bash
# Same credentials as flight API
AMADEUS_API_KEY=your_api_key_here
AMADEUS_API_SECRET=your_api_secret_here
```

No additional setup needed!

### Option C: Booking.com Direct (Hardest)

**Note:** Booking.com API requires:
- Business verification
- Partnership agreement
- Minimum booking volume

**Not recommended for getting started.** Use RapidAPI instead.

---

## Complete .env File Example

### Minimum (Bedrock only - $0 to start!)

```bash
# AWS Configuration (Required)
AWS_REGION=us-west-2
AWS_ACCOUNT_ID=123456789012

# Bedrock Models (No API keys needed!)
ORCHESTRATOR_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
FLIGHT_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
HOTEL_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
VISA_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
ITINERARY_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0

# Demo Mode (agents work without real APIs)
DEMO_MODE=true

# These will be filled by setup scripts
MEMORY_STM_ID=
MEMORY_LTM_ID=
GATEWAY_URL=
GATEWAY_ID=
GATEWAY_ACCESS_TOKEN=
COGNITO_USER_POOL_ID=
COGNITO_CLIENT_ID=
COGNITO_CLIENT_SECRET=
```

### With Real APIs (Optional)

```bash
# AWS Configuration
AWS_REGION=us-west-2
AWS_ACCOUNT_ID=123456789012

# Bedrock Models
ORCHESTRATOR_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
FLIGHT_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
HOTEL_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
VISA_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0
ITINERARY_AGENT_MODEL=us.anthropic.claude-3-7-sonnet-20250219-v1:0

# Real-world APIs (Optional)
AMADEUS_API_KEY=your_amadeus_key
AMADEUS_API_SECRET=your_amadeus_secret
RAPIDAPI_KEY=your_rapidapi_key
HOTEL_API_ENDPOINT=https://booking-com.p.rapidapi.com

# Demo Mode (set to false when APIs configured)
DEMO_MODE=false

# These will be filled by setup scripts
MEMORY_STM_ID=
MEMORY_LTM_ID=
GATEWAY_URL=
GATEWAY_ID=
GATEWAY_ACCESS_TOKEN=
COGNITO_USER_POOL_ID=
COGNITO_CLIENT_ID=
COGNITO_CLIENT_SECRET=
```

---

## Cost Summary

### Setup Costs

**Minimum (Bedrock only)**
- AWS account: **$0** (free tier)
- Bedrock model access: **$0** (free to enable)
- **Total: $0 to start!**

**With Real APIs**
- AWS account: **$0** (free tier)
- Amadeus test API: **$0** (2,000 calls/month free)
- RapidAPI hotels: **$0** (100-500 calls/month free)
- **Total: $0 to start!**

### Monthly Costs (After Free Tier)

**Development (100 invocations/day)**
- Bedrock (Claude 3.7): ~$40/month
- Bedrock (mixed models): ~$15/month
- Bedrock (Llama 3.3): ~$7/month
- AgentCore Runtime: ~$10-30/month
- **Total: $17-70/month**

**Production (1000 invocations/day)**
- Bedrock (Claude 3.7): ~$400/month
- Bedrock (mixed models): ~$150/month
- AgentCore Runtime: ~$50-200/month
- Amadeus (production): ~$10-50/month
- RapidAPI hotels: ~$10-50/month
- **Total: $220-700/month**

---

## Alternative: Direct API Access (Not Recommended)

If you really want to use OpenAI/Anthropic APIs directly instead of Bedrock:

### OpenAI API

1. Go to: https://platform.openai.com/api-keys
2. Create API key
3. Add $5-20 credit
4. Add to .env: `OPENAI_API_KEY=sk-proj-...`

### Anthropic API

1. Go to: https://console.anthropic.com/settings/keys
2. Create API key
3. Add $5-20 credit
4. Add to .env: `ANTHROPIC_API_KEY=sk-ant-...`

**Why not recommended:**
- ❌ Separate billing
- ❌ Additional API keys to manage
- ❌ Often more expensive
- ❌ Less AWS integration

**Use Bedrock instead!**

---

## Quick Start Checklist

### Phase 1: Minimum Viable ($0 to start!)
- [ ] Create AWS account
- [ ] Create IAM user
- [ ] Configure AWS CLI
- [ ] Enable Bedrock models
- [ ] Add AWS config to .env

**You can now deploy and test!** Agents will work with Bedrock models.

### Phase 2: Real Data (Optional, still $0 with free tiers!)
- [ ] Sign up for Amadeus (free test API)
- [ ] Get Amadeus credentials
- [ ] Sign up for RapidAPI (free tier)
- [ ] Subscribe to hotel API
- [ ] Add API keys to .env

---

## Testing Without Optional APIs

You can fully deploy and test without Amadeus/RapidAPI:

**What works:**
✅ All 5 agents deploy and run  
✅ Memory persistence  
✅ User authentication  
✅ Agent coordination  
✅ Conversation flow  
✅ Itinerary generation  

**What requires real APIs:**
❌ Live flight prices  
❌ Real-time hotel availability  
❌ Actual booking capabilities  

---

## Security Best Practices

### Never Commit Credentials

```bash
# Make sure .env is in .gitignore
echo ".env" >> .gitignore
```

### Use Environment Variables

```python
# ✅ Good
api_key = os.getenv("AMADEUS_API_KEY")

# ❌ Bad
api_key = "abc123..."
```

### Rotate Credentials

- Rotate AWS keys every 90 days
- Rotate immediately if exposed
- Use different keys for dev/prod

---

## Troubleshooting

### "Model not found" Error
```bash
# Check Bedrock model access
aws bedrock list-foundation-models --region us-west-2 | grep claude

# Request access in console if needed
```

### "Access Denied" Error
```bash
# Verify AWS credentials
aws sts get-caller-identity

# Check IAM permissions
aws iam get-user-policy --user-name agentcore-deployer --policy-name BedrockAccess
```

### "Invalid API Key" Error
```bash
# Check .env file
cat .env | grep API_KEY

# Verify no extra spaces or quotes
# Regenerate key if needed
```

---

## Next Steps

Once you have your credentials:

1. Add them to `.env` file
2. Run `python3 setup_memory.py`
3. Run `python3 setup_gateway.py`
4. Run `./deploy_to_agentcore.sh`
5. Test your deployment!

---

## Support Resources

- **Bedrock**: https://docs.aws.amazon.com/bedrock/
- **AgentCore**: https://aws.github.io/bedrock-agentcore-starter-toolkit/
- **Amadeus**: https://developers.amadeus.com/support
- **AWS Support**: https://console.aws.amazon.com/support/

---

**You're ready to deploy with just AWS credentials! 🚀**

**See [BEDROCK_MODELS_GUIDE.md](BEDROCK_MODELS_GUIDE.md) for model selection and optimization.**
