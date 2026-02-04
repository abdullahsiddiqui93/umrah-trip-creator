# Umrah Trip Creator - Next.js Website

A professional web application for planning Umrah trips, powered by AWS Bedrock AgentCore agents.

## Features

- 🕋 AI-powered trip planning
- ✈️ Real-time flight search via Amadeus API
- 🏨 Hotel recommendations near Haram
- 📅 Detailed itinerary generation
- 💳 Booking flow
- 🔐 AWS Cognito authentication (via Amplify)
- 🚀 Deployed on AWS Amplify

## Tech Stack

- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Backend**: Next.js API Routes, AWS SDK
- **AI Agents**: AWS Bedrock AgentCore
- **Deployment**: AWS Amplify
- **Authentication**: AWS Cognito (via Amplify)

## Prerequisites

- Node.js 18+ installed
- AWS CLI configured
- AWS Amplify CLI installed
- AWS Account with Bedrock AgentCore access

## Setup Instructions

### 1. Install Dependencies

```bash
cd umrah-website
npm install
```

### 2. Install Amplify CLI

```bash
npm install -g @aws-amplify/cli

# Configure Amplify
amplify configure
```

### 3. Initialize Amplify

```bash
amplify init

# Answer the prompts:
# - Project name: umrahwebsite
# - Environment: prod
# - Default editor: (your choice)
# - App type: javascript
# - Framework: react
# - Source directory: (press enter)
# - Distribution directory: .next
# - Build command: npm run build
# - Start command: npm run start
# - AWS profile: default
```

### 4. Add Hosting

```bash
amplify add hosting

# Choose:
# - Hosting with Amplify Console
# - Manual deployment
```

### 5. Configure Environment Variables

Create a `.env.local` file:

```bash
# AgentCore Configuration
ORCHESTRATOR_ARN=arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo
AWS_REGION=us-west-2

# Optional: For local development
NEXT_PUBLIC_API_URL=http://localhost:3000
```

### 6. Deploy to Amplify

```bash
# Push backend configuration
amplify push

# Publish the website
amplify publish
```

## Local Development

```bash
# Run development server
npm run dev

# Open http://localhost:3000
```

## Amplify Console Configuration

After deployment, configure in AWS Amplify Console:

1. Go to your app in Amplify Console
2. Click "Environment variables"
3. Add:
   - `ORCHESTRATOR_ARN`: Your orchestrator agent ARN
   - `AWS_REGION`: us-west-2
4. Redeploy

## Project Structure

```
umrah-website/
├── app/
│   ├── api/
│   │   └── generate-trip/
│   │       └── route.ts          # API endpoint
│   ├── components/               # React components (future)
│   ├── layout.tsx                # Root layout
│   ├── page.tsx                  # Main page
│   └── globals.css               # Global styles
├── lib/
│   ├── agentcore.ts              # AgentCore client
│   └── types.ts                  # TypeScript types
├── public/                       # Static assets
├── amplify/                      # Amplify configuration
├── next.config.ts                # Next.js config
├── tailwind.config.ts            # Tailwind config
└── package.json
```

## Deployment Options

### Option 1: Amplify Console (Recommended)

1. Push code to GitHub
2. Connect repository in Amplify Console
3. Configure build settings
4. Automatic deployments on push

### Option 2: Manual Deployment

```bash
amplify publish
```

### Option 3: CI/CD Pipeline

Set up GitHub Actions or AWS CodePipeline for automated deployments.

## Custom Domain

1. Go to Amplify Console
2. Click "Domain management"
3. Add your domain
4. Follow DNS configuration steps
5. SSL certificate automatically provisioned

## Monitoring

- **Amplify Console**: View deployments and logs
- **CloudWatch**: Detailed application logs
- **X-Ray**: Request tracing

## Cost Estimate

- **Amplify Hosting**: ~$0.01/build minute + $0.15/GB served
- **API Gateway**: Free tier covers most usage
- **Lambda**: Free tier covers most usage
- **AgentCore**: Pay per invocation
- **Total**: ~$15-30/month for moderate traffic

## Troubleshooting

### Build Fails

```bash
# Check build logs in Amplify Console
# Common issues:
# - Missing environment variables
# - Node version mismatch
# - Dependency conflicts
```

### API Errors

```bash
# Check CloudWatch logs
aws logs tail /aws/lambda/umrah-api --follow

# Check AgentCore agent logs
aws logs tail /aws/bedrock-agentcore/runtimes/umrah_orchestrator-DFFg1bHZKo-DEFAULT --follow
```

### Environment Variables Not Working

- Ensure variables are set in Amplify Console
- Redeploy after adding variables
- Check variable names match code

## Next Steps

1. ✅ Basic Next.js app created
2. ✅ API route for AgentCore integration
3. ✅ Deployment configuration
4. 🔄 Add full UI components (in progress)
5. 🔄 Add authentication with Cognito
6. 🔄 Add payment integration
7. 🔄 Add booking confirmation emails

## Support

For issues or questions:
- Check AWS Amplify documentation
- Check Next.js documentation
- Review AgentCore logs in CloudWatch

## License

Private - All rights reserved
