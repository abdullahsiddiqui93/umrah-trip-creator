# Next.js + AWS Amplify Deployment Guide

## Step-by-Step Setup

### Prerequisites
- Node.js 18+ installed
- AWS CLI configured
- AWS Amplify CLI installed

### Step 1: Install Amplify CLI

```bash
npm install -g @aws-amplify/cli

# Configure Amplify with your AWS credentials
amplify configure
```

### Step 2: Create Next.js Project

```bash
# Create the Next.js app
npx create-next-app@latest umrah-website --typescript --tailwind --app --no-src-dir

cd umrah-website

# Install AWS SDK and Amplify libraries
npm install aws-amplify @aws-amplify/ui-react @aws-sdk/client-bedrock-agent-runtime
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material
```

### Step 3: Initialize Amplify

```bash
# Initialize Amplify in your project
amplify init

# Answer the prompts:
# - Enter a name for the project: umrahwebsite
# - Enter a name for the environment: prod
# - Choose your default editor: Visual Studio Code (or your preference)
# - Choose the type of app: javascript
# - What javascript framework: react
# - Source Directory Path: (press enter for default)
# - Distribution Directory Path: .next
# - Build Command: npm run build
# - Start Command: npm run start
# - Select the authentication method: AWS profile
# - Please choose the profile: default (or your AWS profile)
```

### Step 4: Add Amplify Hosting

```bash
# Add hosting with Amplify Console
amplify add hosting

# Choose:
# - Select the plugin module: Hosting with Amplify Console
# - Choose a type: Manual deployment
```

### Step 5: Add API (Optional - for backend functions)

```bash
# Add REST API
amplify add api

# Choose:
# - Select from REST or GraphQL: REST
# - Provide a friendly name: umrahapi
# - Provide a path: /api
# - Choose a Lambda source: Create a new Lambda function
# - Provide a friendly name: umrahFunction
# - Choose runtime: Python
# - Choose template: Hello World
```

### Step 6: Deploy

```bash
# Build and deploy everything
amplify push

# Publish the website
amplify publish
```

### Step 7: Configure Environment Variables

In AWS Amplify Console:
1. Go to your app
2. Click "Environment variables"
3. Add:
   - `ORCHESTRATOR_ARN`: Your orchestrator agent ARN
   - `FLIGHT_AGENT_ARN`: Your flight agent ARN
   - `HOTEL_AGENT_ARN`: Your hotel agent ARN
   - `AWS_REGION`: us-west-2

### Step 8: Set Up Custom Domain (Optional)

```bash
# In Amplify Console
# 1. Go to "Domain management"
# 2. Add domain
# 3. Follow DNS configuration steps
```

## Project Structure

```
umrah-website/
├── app/
│   ├── api/
│   │   ├── generate-trip/
│   │   │   └── route.ts          # API endpoint for trip generation
│   │   └── health/
│   │       └── route.ts          # Health check endpoint
│   ├── components/
│   │   ├── TravelDates.tsx       # Step 1 component
│   │   ├── TravelerDetails.tsx   # Step 2 component
│   │   ├── HotelPreferences.tsx  # Step 3 component
│   │   ├── BudgetForm.tsx        # Step 4 component
│   │   ├── ReviewStep.tsx        # Step 5 component
│   │   ├── TripOptions.tsx       # Step 6 component
│   │   ├── FlightCard.tsx        # Flight display component
│   │   ├── HotelCard.tsx         # Hotel display component
│   │   └── BookingForm.tsx       # Booking component
│   ├── layout.tsx                # Root layout
│   ├── page.tsx                  # Home page
│   └── globals.css               # Global styles
├── lib/
│   ├── agentcore.ts              # AgentCore client
│   └── types.ts                  # TypeScript types
├── public/
│   └── images/                   # Static images
├── amplify/
│   └── backend/                  # Amplify backend config
├── next.config.js
├── package.json
├── tsconfig.json
└── tailwind.config.js
```

## Continuous Deployment

Amplify automatically deploys when you push to your Git repository:

```bash
# Connect to GitHub
# In Amplify Console:
# 1. Go to your app
# 2. Click "Connect repository"
# 3. Choose GitHub
# 4. Select your repository
# 5. Configure build settings
# 6. Save and deploy

# Now every git push will trigger a deployment
git add .
git commit -m "Update website"
git push origin main
```

## Monitoring

- **Amplify Console**: View deployments, logs, and metrics
- **CloudWatch**: Detailed logs and metrics
- **X-Ray**: Trace requests through your application

## Cost Estimate

- **Amplify Hosting**: ~$0.01 per build minute + $0.15 per GB served
- **Lambda Functions**: Free tier covers most usage
- **API Gateway**: Free tier covers most usage
- **Estimated Total**: $15-30/month for moderate traffic

## Next Steps

1. I'll create all the Next.js files for you
2. You'll run the setup commands above
3. Deploy to Amplify
4. Configure your custom domain
5. Your website will be live!

Ready to proceed? 🚀
