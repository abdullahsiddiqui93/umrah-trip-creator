# AWS AgentCore Deployment Guide

Complete guide to deploy Umrah Trip Creator on Amazon Bedrock AgentCore Runtime.

---

## 📋 Prerequisites

### 1. AWS Account Setup
- Active AWS account
- AWS CLI installed and configured
- Region: `us-west-2` (recommended)
- IAM permissions for:
  - Bedrock
  - AgentCore
  - S3
  - DynamoDB
  - CloudFormation
  - Lambda
  - API Gateway
  - Cognito

### 2. API Keys Required
```bash
# Get these API keys:
AMADEUS_API_KEY=...          # https://developers.amadeus.com
AMADEUS_API_SECRET=...
BOOKING_API_KEY=...          # https://developers.booking.com
OPENAI_API_KEY=...           # https://platform.openai.com
ANTHROPIC_API_KEY=...        # https://console.anthropic.com
```

### 3. Install Tools
```bash
# AWS CLI
brew install awscli  # macOS
# or: pip install awscli

# AWS SAM CLI (for deployment)
brew install aws-sam-cli

# Python dependencies
pip install boto3 bedrock-agentcore-runtime
```

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    User (Browser)                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              CloudFront + S3 (Frontend)                 │
│                  Streamlit Static                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  API Gateway                            │
│              (REST API Endpoints)                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│          Amazon Bedrock AgentCore Runtime               │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Orchestrator Agent (Strands)                    │  │
│  │  ├─ A2A Client                                   │  │
│  │  └─ Coordinates all agents                       │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │
│  │ Flight Agent │ │ Hotel Agent  │ │ Visa Agent   │  │
│  │  (OpenAI)    │ │  (Claude)    │ │  (OpenAI)    │  │
│  │  A2A Server  │ │  A2A Server  │ │  A2A Server  │  │
│  └──────────────┘ └──────────────┘ └──────────────┘  │
│                                                         │
│  ┌──────────────┐                                      │
│  │ Itinerary    │                                      │
│  │ Agent        │                                      │
│  │ (Claude)     │                                      │
│  │ A2A Server   │                                      │
│  └──────────────┘                                      │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌────────┐  ┌─────────┐  ┌─────────┐
   │   S3   │  │DynamoDB │  │ Cognito │
   │(Docs)  │  │(Data)   │  │(Auth)   │
   └────────┘  └─────────┘  └─────────┘
```

---

## 🚀 Deployment Steps

### Step 1: Prepare Environment

```bash
# Navigate to project
cd umrah-trip-creator

# Copy environment template
cp .env.example .env

# Edit .env with your values
nano .env
```

Add your credentials:
```bash
AWS_REGION=us-west-2
AWS_ACCOUNT_ID=123456789012

AMADEUS_API_KEY=your_key
AMADEUS_API_SECRET=your_secret
BOOKING_API_KEY=your_key
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

ORCHESTRATOR_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
FLIGHT_AGENT_MODEL=gpt-4o-2024-08-06
HOTEL_AGENT_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
VISA_AGENT_MODEL=gpt-4o-2024-08-06
ITINERARY_AGENT_MODEL=anthropic.claude-sonnet-4-5-20250929-v1:0
```

### Step 2: Create Infrastructure

Create `infrastructure/cloudformation/main.yaml`:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Umrah Trip Creator - AgentCore Deployment'

Parameters:
  ProjectName:
    Type: String
    Default: umrah-trip-creator
  
  OpenAIAPIKey:
    Type: String
    NoEcho: true
  
  AnthropicAPIKey:
    Type: String
    NoEcho: true

Resources:
  # S3 Bucket for documents
  DocumentBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${ProjectName}-documents-${AWS::AccountId}'
      VersioningConfiguration:
        Status: Enabled
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

  # DynamoDB for bookings
  BookingsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '${ProjectName}-bookings'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: booking_id
          AttributeType: S
        - AttributeName: user_email
          AttributeType: S
      KeySchema:
        - AttributeName: booking_id
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: user-email-index
          KeySchema:
            - AttributeName: user_email
              KeyType: HASH
          Projection:
            ProjectionType: ALL

  # Cognito User Pool
  UserPool:
    Type: AWS::Cognito::UserPool
    Properties:
      UserPoolName: !Sub '${ProjectName}-users'
      AutoVerifiedAttributes:
        - email
      Schema:
        - Name: email
          Required: true
          Mutable: false

  # AgentCore Runtime Configuration
  AgentCoreRuntime:
    Type: AWS::Bedrock::AgentCoreRuntime
    Properties:
      RuntimeName: !Sub '${ProjectName}-runtime'
      RuntimeConfiguration:
        Memory:
          Type: LONG_TERM
          Configuration:
            Provider: DYNAMODB
            TableName: !Ref BookingsTable
        Observability:
          Enabled: true
          CloudWatchLogGroup: !Ref AgentLogGroup
        Gateway:
          Enabled: true
          Configuration:
            Endpoints:
              - Name: amadeus
                Type: REST_API
                Url: https://api.amadeus.com
              - Name: booking
                Type: REST_API
                Url: https://api.booking.com

  # CloudWatch Log Group
  AgentLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/agentcore/${ProjectName}'
      RetentionInDays: 30

Outputs:
  RuntimeEndpoint:
    Value: !GetAtt AgentCoreRuntime.Endpoint
    Description: AgentCore Runtime Endpoint
  
  DocumentBucket:
    Value: !Ref DocumentBucket
    Description: S3 Bucket for documents
  
  BookingsTable:
    Value: !Ref BookingsTable
    Description: DynamoDB table for bookings
```

### Step 3: Deploy Infrastructure

```bash
# Deploy CloudFormation stack
aws cloudformation create-stack \
  --stack-name umrah-trip-creator \
  --template-body file://infrastructure/cloudformation/main.yaml \
  --parameters \
    ParameterKey=OpenAIAPIKey,ParameterValue=$OPENAI_API_KEY \
    ParameterKey=AnthropicAPIKey,ParameterValue=$ANTHROPIC_API_KEY \
  --capabilities CAPABILITY_IAM

# Wait for completion
aws cloudformation wait stack-create-complete \
  --stack-name umrah-trip-creator

# Get outputs
aws cloudformation describe-stacks \
  --stack-name umrah-trip-creator \
  --query 'Stacks[0].Outputs'
```

### Step 4: Deploy Agents to AgentCore

Create `deploy.py`:

```python
#!/usr/bin/env python3
"""
Deploy agents to Amazon Bedrock AgentCore Runtime
"""

import boto3
import os
from pathlib import Path

def deploy_agents():
    """Deploy all agents to AgentCore"""
    
    client = boto3.client('bedrock-agentcore-runtime', region_name='us-west-2')
    
    # Deploy Orchestrator Agent
    print("Deploying Orchestrator Agent...")
    orchestrator_response = client.create_agent(
        agentName='umrah-orchestrator',
        agentType='STRANDS',
        agentConfiguration={
            'model': os.getenv('ORCHESTRATOR_MODEL'),
            'role': 'Umrah Trip Coordinator',
            'goal': 'Coordinate specialized agents to plan Umrah trips',
            'a2aConfiguration': {
                'mode': 'CLIENT',
                'endpoints': [
                    'flight-agent',
                    'hotel-agent',
                    'visa-agent',
                    'itinerary-agent'
                ]
            }
        },
        sourceCode=Path('agents/orchestrator/orchestrator_agent.py').read_text()
    )
    
    # Deploy Flight Agent
    print("Deploying Flight Agent...")
    flight_response = client.create_agent(
        agentName='flight-agent',
        agentType='OPENAI',
        agentConfiguration={
            'model': os.getenv('FLIGHT_AGENT_MODEL'),
            'role': 'Flight Search Specialist',
            'a2aConfiguration': {
                'mode': 'SERVER',
                'authentication': {
                    'type': 'OAUTH2',
                    'cognitoUserPoolId': os.getenv('COGNITO_USER_POOL_ID')
                }
            },
            'tools': [
                {
                    'name': 'search_flights',
                    'description': 'Search for flights',
                    'apiEndpoint': 'amadeus'
                }
            ]
        },
        sourceCode=Path('agents/flight_agent/flight_agent.py').read_text()
    )
    
    # Deploy Hotel Agent
    print("Deploying Hotel Agent...")
    hotel_response = client.create_agent(
        agentName='hotel-agent',
        agentType='ANTHROPIC',
        agentConfiguration={
            'model': os.getenv('HOTEL_AGENT_MODEL'),
            'role': 'Hotel Booking Specialist',
            'a2aConfiguration': {
                'mode': 'SERVER',
                'authentication': {
                    'type': 'OAUTH2',
                    'cognitoUserPoolId': os.getenv('COGNITO_USER_POOL_ID')
                }
            },
            'tools': [
                {
                    'name': 'search_hotels',
                    'description': 'Search for hotels',
                    'apiEndpoint': 'booking'
                }
            ]
        },
        sourceCode=Path('agents/hotel_agent/hotel_agent.py').read_text()
    )
    
    # Deploy Visa Agent
    print("Deploying Visa Agent...")
    visa_response = client.create_agent(
        agentName='visa-agent',
        agentType='OPENAI',
        agentConfiguration={
            'model': os.getenv('VISA_AGENT_MODEL'),
            'role': 'Visa Processing Specialist',
            'a2aConfiguration': {
                'mode': 'SERVER'
            }
        },
        sourceCode=Path('agents/visa_agent/visa_agent.py').read_text()
    )
    
    # Deploy Itinerary Agent
    print("Deploying Itinerary Agent...")
    itinerary_response = client.create_agent(
        agentName='itinerary-agent',
        agentType='ANTHROPIC',
        agentConfiguration={
            'model': os.getenv('ITINERARY_AGENT_MODEL'),
            'role': 'Umrah Itinerary Specialist',
            'a2aConfiguration': {
                'mode': 'SERVER'
            }
        },
        sourceCode=Path('agents/itinerary_agent/itinerary_agent.py').read_text()
    )
    
    print("\n✅ All agents deployed successfully!")
    print(f"Orchestrator: {orchestrator_response['agentId']}")
    print(f"Flight Agent: {flight_response['agentId']}")
    print(f"Hotel Agent: {hotel_response['agentId']}")
    print(f"Visa Agent: {visa_response['agentId']}")
    print(f"Itinerary Agent: {itinerary_response['agentId']}")

if __name__ == '__main__':
    deploy_agents()
```

Run deployment:
```bash
python deploy.py
```

### Step 5: Deploy Frontend

```bash
# Build frontend for production
streamlit build frontend/streamlit_app.py

# Deploy to S3
aws s3 sync frontend/build s3://umrah-trip-creator-frontend-${AWS_ACCOUNT_ID}

# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name umrah-trip-creator-frontend-${AWS_ACCOUNT_ID}.s3.amazonaws.com \
  --default-root-object index.html
```

---

## 🧪 Testing Deployment

```bash
# Test orchestrator agent
python test/test_deployed_agents.py

# Test API endpoints
curl -X POST https://your-api-gateway-url/api/plan-trip \
  -H "Content-Type: application/json" \
  -d @test/sample_request.json
```

---

## 📊 Monitoring

### CloudWatch Dashboards
```bash
# Create monitoring dashboard
aws cloudwatch put-dashboard \
  --dashboard-name umrah-trip-creator \
  --dashboard-body file://infrastructure/monitoring/dashboard.json
```

### Key Metrics to Monitor:
- Agent invocation count
- Response times
- Error rates
- API Gateway requests
- DynamoDB read/write units
- S3 storage usage

---

## 💰 Cost Estimation

### Monthly Costs (1000 bookings/month):
- **AgentCore Runtime**: $100-200
- **Bedrock Models**: $50-150
- **DynamoDB**: $20-50
- **S3**: $10-20
- **API Gateway**: $15-30
- **CloudWatch**: $10-20
- **Data Transfer**: $20-40

**Total**: ~$225-510/month

---

## 🔒 Security Best Practices

1. **API Keys**: Store in AWS Secrets Manager
2. **Authentication**: Use Cognito for user auth
3. **Encryption**: Enable at rest and in transit
4. **IAM**: Least privilege access
5. **VPC**: Deploy agents in private subnets
6. **WAF**: Enable AWS WAF on API Gateway

---

## 🆘 Troubleshooting

### Agent Not Responding
```bash
# Check logs
aws logs tail /aws/agentcore/umrah-trip-creator --follow

# Check agent status
aws bedrock-agentcore-runtime describe-agent --agent-id <agent-id>
```

### High Costs
- Review CloudWatch metrics
- Optimize agent prompts
- Enable caching
- Use reserved capacity

---

## 📚 Next Steps

1. ✅ Deploy infrastructure
2. ✅ Deploy agents
3. ✅ Test end-to-end
4. ✅ Set up monitoring
5. ✅ Configure alerts
6. ✅ Go live!

---

**Your Umrah Trip Creator is now running on AWS AgentCore! 🚀**
