# Complete Setup Guide: GitHub + AWS AgentCore

This guide covers both GitHub setup and AWS AgentCore deployment.

---

## Part 1: GitHub Setup (10 minutes)

### Step 1: Initialize Git Repository

```bash
cd umrah-trip-creator

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Multi-agent Umrah trip creator

- 5 specialized AI agents (Orchestrator, Flight, Hotel, Visa, Itinerary)
- Streamlit frontend with 6-step wizard
- Complete documentation
- Demo mode with mock data
- Ready for AWS AgentCore deployment"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `umrah-trip-creator`
3. Description: `Multi-agent AI system for planning Umrah trips using Amazon Bedrock AgentCore`
4. Choose **Public** (recommended for portfolio)
5. **Don't** initialize with README (we have one)
6. Click "Create repository"

### Step 3: Push to GitHub

```bash
# Add GitHub as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/umrah-trip-creator.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Enhance Your Repository

#### Add Topics/Tags
On GitHub, click "⚙️ Settings" → "About" → Add topics:
- `ai-agents`
- `multi-agent-system`
- `amazon-bedrock`
- `agentcore`
- `streamlit`
- `umrah`
- `travel-planning`
- `a2a-protocol`
- `python`
- `aws`

#### Add Description
```
🕋 Multi-agent AI system for planning Umrah trips. Features 5 specialized agents coordinating via A2A protocol, beautiful Streamlit UI, and deployment on Amazon Bedrock AgentCore.
```

#### Create First Release
1. Go to "Releases" → "Create a new release"
2. Tag: `v0.1.0`
3. Title: `Initial Release - Demo Mode`
4. Description:
```markdown
## 🎉 First Release!

### Features
- ✅ 5 specialized AI agents
- ✅ Beautiful Streamlit frontend
- ✅ 6-step wizard interface
- ✅ Demo mode with mock data
- ✅ Complete documentation
- ✅ AWS AgentCore deployment ready

### Demo Mode
This release includes a fully functional demo with mock data.
Perfect for testing and development!

### Next Steps
- Add real API integrations
- Deploy to AWS AgentCore
- Enable production features

See DEPLOYMENT_GUIDE.md for production deployment.
```

---

## Part 2: AWS AgentCore Deployment (30-60 minutes)

### Prerequisites Checklist

- [ ] AWS Account with admin access
- [ ] AWS CLI installed and configured
- [ ] Python 3.10+ installed
- [ ] API Keys obtained:
  - [ ] OpenAI API key
  - [ ] Anthropic API key
  - [ ] Amadeus API key (optional for demo)
  - [ ] Booking.com API key (optional for demo)

### Step 1: Configure AWS CLI

```bash
# Configure AWS credentials
aws configure

# Enter:
# AWS Access Key ID: YOUR_ACCESS_KEY
# AWS Secret Access Key: YOUR_SECRET_KEY
# Default region: us-west-2
# Default output format: json

# Verify configuration
aws sts get-caller-identity
```

### Step 2: Set Up Environment

```bash
cd umrah-trip-creator

# Copy environment template
cp .env.example .env

# Edit .env file
nano .env
```

Add your credentials:
```bash
# AWS Configuration
AWS_REGION=us-west-2
AWS_ACCOUNT_ID=123456789012  # Your AWS account ID

# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
AMADEUS_API_KEY=your_key  # Optional for demo
AMADEUS_API_SECRET=your_secret  # Optional for demo
BOOKING_API_KEY=your_key  # Optional for demo

# Agent Models
ORCHESTRATOR_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
FLIGHT_AGENT_MODEL=gpt-4o-2024-08-06
HOTEL_AGENT_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
VISA_AGENT_MODEL=gpt-4o-2024-08-06
ITINERARY_AGENT_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
```

### Step 3: Install Dependencies

```bash
# Install Python dependencies
pip install boto3 python-dotenv

# Or use requirements file
pip install -r requirements.txt
```

### Step 4: Deploy Infrastructure

```bash
# Run deployment script
python deploy.py
```

This will:
1. ✅ Check prerequisites
2. ✅ Create S3 bucket for documents
3. ✅ Create DynamoDB table for bookings
4. ✅ Set up CloudWatch logging
5. ✅ Configure IAM roles
6. ✅ Deploy CloudFormation stack

**Expected time**: 5-10 minutes

### Step 5: Deploy Agents (Manual for now)

Since AgentCore is still in preview, manual deployment:

```bash
# Package agent code
zip -r orchestrator.zip agents/orchestrator/
zip -r flight_agent.zip agents/flight_agent/
zip -r hotel_agent.zip agents/hotel_agent/
zip -r visa_agent.zip agents/visa_agent/
zip -r itinerary_agent.zip agents/itinerary_agent/

# Upload to S3
aws s3 cp orchestrator.zip s3://umrah-trip-creator-agents-${AWS_ACCOUNT_ID}/
aws s3 cp flight_agent.zip s3://umrah-trip-creator-agents-${AWS_ACCOUNT_ID}/
aws s3 cp hotel_agent.zip s3://umrah-trip-creator-agents-${AWS_ACCOUNT_ID}/
aws s3 cp visa_agent.zip s3://umrah-trip-creator-agents-${AWS_ACCOUNT_ID}/
aws s3 cp itinerary_agent.zip s3://umrah-trip-creator-agents-${AWS_ACCOUNT_ID}/
```

### Step 6: Test Deployment

```bash
# Test infrastructure
python test_local.py

# Check CloudFormation stack
aws cloudformation describe-stacks \
  --stack-name umrah-trip-creator-stack

# View logs
aws logs tail /aws/agentcore/umrah-trip-creator --follow
```

### Step 7: Deploy Frontend (Optional)

```bash
# Create S3 bucket for frontend
aws s3 mb s3://umrah-trip-creator-frontend-${AWS_ACCOUNT_ID}

# Enable static website hosting
aws s3 website s3://umrah-trip-creator-frontend-${AWS_ACCOUNT_ID} \
  --index-document index.html

# Upload frontend files
aws s3 sync frontend/ s3://umrah-trip-creator-frontend-${AWS_ACCOUNT_ID}/

# Get website URL
echo "http://umrah-trip-creator-frontend-${AWS_ACCOUNT_ID}.s3-website-us-west-2.amazonaws.com"
```

---

## Part 3: Verification & Testing

### Verify GitHub

```bash
# Check remote
git remote -v

# View on GitHub
open https://github.com/YOUR_USERNAME/umrah-trip-creator
```

### Verify AWS Deployment

```bash
# List S3 buckets
aws s3 ls | grep umrah-trip-creator

# Check DynamoDB tables
aws dynamodb list-tables | grep umrah-trip-creator

# View CloudFormation stacks
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE
```

### Test End-to-End

1. **Local Demo**:
   ```bash
   streamlit run frontend/streamlit_app.py
   ```
   Open http://localhost:8501

2. **AWS Deployment**:
   - Test API endpoints
   - Verify agent responses
   - Check CloudWatch logs

---

## Part 4: Monitoring & Maintenance

### Set Up CloudWatch Alarms

```bash
# Create alarm for errors
aws cloudwatch put-metric-alarm \
  --alarm-name umrah-trip-creator-errors \
  --alarm-description "Alert on agent errors" \
  --metric-name Errors \
  --namespace AWS/AgentCore \
  --statistic Sum \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold
```

### Regular Maintenance

- **Weekly**: Review CloudWatch logs
- **Monthly**: Check costs and optimize
- **Quarterly**: Update dependencies
- **As needed**: Scale resources

---

## Part 5: Going to Production

### Production Checklist

- [ ] Add real API integrations (Amadeus, Booking.com)
- [ ] Enable payment processing (Stripe/PayPal)
- [ ] Set up email notifications (SES/SendGrid)
- [ ] Configure custom domain
- [ ] Enable SSL/TLS certificates
- [ ] Set up CI/CD pipeline
- [ ] Add comprehensive testing
- [ ] Implement rate limiting
- [ ] Enable WAF protection
- [ ] Set up backup and disaster recovery
- [ ] Create runbook for operations
- [ ] Train support team

### Production Deployment

```bash
# Update environment to production
export ENVIRONMENT=production

# Deploy with production settings
python deploy.py --environment production

# Run production tests
python test/test_production.py

# Monitor for 24 hours before full launch
```

---

## Troubleshooting

### GitHub Issues

**Problem**: Push rejected
```bash
# Solution: Pull first
git pull origin main --rebase
git push origin main
```

**Problem**: Large files
```bash
# Solution: Use Git LFS
git lfs install
git lfs track "*.zip"
git add .gitattributes
```

### AWS Issues

**Problem**: Stack creation failed
```bash
# Solution: Check logs
aws cloudformation describe-stack-events \
  --stack-name umrah-trip-creator-stack

# Delete and retry
aws cloudformation delete-stack \
  --stack-name umrah-trip-creator-stack
```

**Problem**: Permission denied
```bash
# Solution: Check IAM permissions
aws iam get-user
aws iam list-attached-user-policies --user-name YOUR_USERNAME
```

---

## Cost Management

### Estimated Costs

**Development/Demo**:
- S3: $1-5/month
- DynamoDB: $1-5/month
- CloudWatch: $1-3/month
- **Total**: ~$3-13/month

**Production (1000 bookings/month)**:
- AgentCore: $100-200/month
- Bedrock Models: $50-150/month
- S3: $10-20/month
- DynamoDB: $20-50/month
- API Gateway: $15-30/month
- **Total**: ~$195-450/month

### Cost Optimization

1. Use reserved capacity for predictable workloads
2. Enable S3 lifecycle policies
3. Use DynamoDB on-demand for variable traffic
4. Implement caching to reduce API calls
5. Monitor and set billing alarms

---

## Next Steps

### Immediate (This Week)
1. ✅ Push to GitHub
2. ✅ Deploy basic infrastructure
3. ✅ Test demo mode
4. ✅ Share with team

### Short Term (This Month)
1. Add real API integrations
2. Deploy agents to AgentCore
3. Set up monitoring
4. Beta testing with users

### Long Term (Next Quarter)
1. Production launch
2. Marketing and user acquisition
3. Feature enhancements
4. Scale infrastructure

---

## Support & Resources

### Documentation
- [README.md](README.md) - Main documentation
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Detailed deployment
- [DEMO_VS_PRODUCTION.md](DEMO_VS_PRODUCTION.md) - Feature comparison

### AWS Resources
- [AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [AWS Support](https://console.aws.amazon.com/support/)
- [AWS Forums](https://forums.aws.amazon.com/)

### Community
- GitHub Issues for bugs
- GitHub Discussions for questions
- Twitter/X for updates

---

**Congratulations! Your Umrah Trip Creator is now on GitHub and ready for AWS deployment! 🎉**
