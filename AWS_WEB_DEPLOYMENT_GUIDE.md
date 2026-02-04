# AWS Web Deployment Guide - Umrah Trip Creator

## Overview

You want to convert the Streamlit app into a proper production website hosted on AWS. Here are your options:

---

## Option 1: Quick Deploy - Streamlit on AWS (Easiest)

**Pros:** Fastest to deploy, minimal changes needed
**Cons:** Still looks like Streamlit, limited customization

### Deployment Options:

#### A. AWS App Runner (Recommended for Streamlit)
```bash
# 1. Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "frontend/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
EOF

# 2. Build and push to ECR
aws ecr create-repository --repository-name umrah-trip-creator
docker build -t umrah-trip-creator .
docker tag umrah-trip-creator:latest <account-id>.dkr.ecr.us-west-2.amazonaws.com/umrah-trip-creator:latest
docker push <account-id>.dkr.ecr.us-west-2.amazonaws.com/umrah-trip-creator:latest

# 3. Deploy to App Runner via AWS Console
# - Go to App Runner
# - Create service from ECR
# - Configure port 8501
# - Add environment variables from .env
```

**Cost:** ~$25-50/month

#### B. AWS Elastic Beanstalk
```bash
# 1. Install EB CLI
pip install awsebcli

# 2. Initialize
eb init -p python-3.11 umrah-trip-creator --region us-west-2

# 3. Create environment
eb create umrah-prod --instance-type t3.medium

# 4. Deploy
eb deploy
```

**Cost:** ~$30-60/month

---

## Option 2: Convert to React + FastAPI (Professional Website)

**Pros:** Full control, professional look, modern tech stack
**Cons:** Requires significant development work

### Architecture:
```
Frontend (React)  →  Backend (FastAPI)  →  AgentCore Agents
     ↓                      ↓
  S3 + CloudFront      Lambda/ECS
```

### Implementation Steps:

### 1. Create FastAPI Backend

```python
# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3
import json

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TripRequest(BaseModel):
    departure_city: str
    departure_date: str
    return_date: str
    num_travelers: int
    budget: float
    # ... other fields

@app.post("/api/generate-trip")
async def generate_trip(request: TripRequest):
    """Generate trip plan using AgentCore orchestrator"""
    try:
        # Call AgentCore orchestrator
        client = boto3.client('bedrock-agent-runtime', region_name='us-west-2')
        
        response = client.invoke_agent(
            agentId='your-orchestrator-arn',
            sessionId=str(uuid.uuid4()),
            inputText=json.dumps(request.dict())
        )
        
        # Parse response
        result = parse_agent_response(response)
        return {"success": True, "data": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health():
    return {"status": "healthy"}
```

### 2. Create React Frontend

```bash
# Create React app
npx create-react-app umrah-frontend
cd umrah-frontend

# Install dependencies
npm install axios react-router-dom @mui/material @emotion/react @emotion/styled
```

```javascript
// src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import { Container, Stepper, Step, StepLabel, Button } from '@mui/material';

function App() {
  const [activeStep, setActiveStep] = useState(0);
  const [tripData, setTripData] = useState({});
  const [loading, setLoading] = useState(false);

  const steps = [
    'Travel Dates',
    'Traveler Details',
    'Hotel Preferences',
    'Budget',
    'Review',
    'Trip Options'
  ];

  const handleGenerateTrip = async () => {
    setLoading(true);
    try {
      const response = await axios.post(
        'https://api.yourdomain.com/api/generate-trip',
        tripData
      );
      // Handle response
      setActiveStep(5);
    } catch (error) {
      console.error('Error generating trip:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Stepper activeStep={activeStep}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      {/* Step components here */}
    </Container>
  );
}

export default App;
```

### 3. Deploy to AWS

#### Backend Deployment (Lambda + API Gateway):

```bash
# Install Serverless Framework
npm install -g serverless

# Create serverless.yml
cat > serverless.yml << 'EOF'
service: umrah-backend

provider:
  name: aws
  runtime: python3.11
  region: us-west-2
  environment:
    ORCHESTRATOR_ARN: ${env:ORCHESTRATOR_ARN}

functions:
  api:
    handler: main.handler
    events:
      - httpApi:
          path: /{proxy+}
          method: ANY
    timeout: 300
    memorySize: 1024

plugins:
  - serverless-python-requirements
EOF

# Deploy
serverless deploy
```

#### Frontend Deployment (S3 + CloudFront):

```bash
# Build React app
npm run build

# Create S3 bucket
aws s3 mb s3://umrah-trip-creator-frontend

# Enable static website hosting
aws s3 website s3://umrah-trip-creator-frontend \
  --index-document index.html \
  --error-document index.html

# Upload build files
aws s3 sync build/ s3://umrah-trip-creator-frontend

# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name umrah-trip-creator-frontend.s3.amazonaws.com \
  --default-root-object index.html
```

**Cost:** ~$20-40/month (Lambda + S3 + CloudFront)

---

## Option 3: Next.js Full-Stack (Modern & SEO-Friendly)

**Pros:** Server-side rendering, great SEO, modern framework
**Cons:** Learning curve if new to Next.js

### Setup:

```bash
# Create Next.js app
npx create-next-app@latest umrah-website --typescript --tailwind --app

cd umrah-website

# Install dependencies
npm install @aws-sdk/client-bedrock-agent-runtime
```

### API Routes:

```typescript
// app/api/generate-trip/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { BedrockAgentRuntimeClient, InvokeAgentCommand } from '@aws-sdk/client-bedrock-agent-runtime';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    const client = new BedrockAgentRuntimeClient({ region: 'us-west-2' });
    
    const command = new InvokeAgentCommand({
      agentId: process.env.ORCHESTRATOR_ARN,
      sessionId: crypto.randomUUID(),
      inputText: JSON.stringify(body)
    });
    
    const response = await client.send(command);
    
    return NextResponse.json({ success: true, data: response });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
```

### Deploy to Vercel (Easiest):

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

**Cost:** Free tier available, then ~$20/month

---

## Option 4: AWS Amplify (Full-Stack AWS Solution)

**Pros:** Integrated AWS services, CI/CD built-in, authentication
**Cons:** AWS-specific, some vendor lock-in

```bash
# Install Amplify CLI
npm install -g @aws-amplify/cli

# Initialize
amplify init

# Add hosting
amplify add hosting

# Add API
amplify add api

# Deploy
amplify publish
```

**Cost:** ~$15-30/month

---

## Recommended Approach for Your Project

Given your requirements, I recommend **Option 2 (React + FastAPI)** or **Option 3 (Next.js)** for these reasons:

### Why React + FastAPI or Next.js:

1. **Professional Look:** Complete control over UI/UX
2. **Performance:** Fast, responsive, modern
3. **Scalability:** Can handle high traffic
4. **SEO:** Good for marketing (especially Next.js)
5. **Cost-Effective:** ~$20-40/month
6. **Maintainability:** Standard tech stack

### Quick Start - Next.js Approach (Recommended):

I can help you create:
1. **Next.js frontend** with beautiful UI (similar to Booking.com)
2. **API routes** that call your AgentCore agents
3. **Deployment** to Vercel or AWS Amplify
4. **Custom domain** setup
5. **Authentication** with Cognito

Would you like me to:
1. Create a Next.js version of your app?
2. Set up the deployment infrastructure?
3. Create a React + FastAPI version?
4. Just deploy the Streamlit app quickly to AWS?

Let me know which option you prefer, and I'll help you implement it!

---

## Cost Comparison

| Option | Monthly Cost | Setup Time | Customization |
|--------|-------------|------------|---------------|
| Streamlit on App Runner | $25-50 | 1 hour | Low |
| React + FastAPI | $20-40 | 2-3 days | High |
| Next.js | $20-30 | 2-3 days | High |
| AWS Amplify | $15-30 | 1-2 days | Medium |

---

## Next Steps

1. **Choose your approach** (I recommend Next.js or React + FastAPI)
2. **I'll create the necessary files** for your chosen option
3. **Set up AWS infrastructure** (S3, CloudFront, Lambda, etc.)
4. **Deploy and test**
5. **Configure custom domain**
6. **Set up CI/CD** for automatic deployments

Let me know which option you'd like to pursue! 🚀
