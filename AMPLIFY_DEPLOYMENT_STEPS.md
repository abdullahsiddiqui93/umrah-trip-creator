# AWS Amplify Deployment - Step by Step Guide

## ✅ What I've Created

I've created a complete Next.js website in the `umrah-website/` folder with:

- ✅ Next.js 15 with TypeScript
- ✅ Tailwind CSS for styling
- ✅ API route that calls your AgentCore orchestrator
- ✅ Multi-step trip planning interface
- ✅ AWS SDK integration
- ✅ Amplify-ready configuration

## 🚀 Deployment Steps

### Step 1: Navigate to the Project

```bash
cd umrah-website
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Install Amplify CLI (if not already installed)

```bash
npm install -g @aws-amplify/cli
```

### Step 4: Configure Amplify

```bash
amplify configure
```

This will:
1. Open AWS Console in your browser
2. Ask you to create an IAM user
3. Configure AWS credentials

### Step 5: Initialize Amplify

```bash
amplify init
```

Answer the prompts:
- **Project name**: `umrahwebsite`
- **Environment**: `prod`
- **Default editor**: (your choice)
- **App type**: `javascript`
- **Framework**: `react`
- **Source directory**: (press Enter for default)
- **Distribution directory**: `.next`
- **Build command**: `npm run build`
- **Start command**: `npm run start`
- **AWS profile**: `default` (or your profile name)

### Step 6: Add Hosting

```bash
amplify add hosting
```

Choose:
- **Select the plugin module**: `Hosting with Amplify Console`
- **Choose a type**: `Manual deployment`

### Step 7: Create Environment File

Create `.env.local`:

```bash
cat > .env.local << 'EOF'
ORCHESTRATOR_ARN=arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo
AWS_REGION=us-west-2
EOF
```

### Step 8: Test Locally (Optional)

```bash
npm run dev
```

Open http://localhost:3000 to test.

### Step 9: Deploy to Amplify

```bash
amplify publish
```

This will:
1. Build your Next.js app
2. Upload to AWS
3. Deploy to Amplify hosting
4. Give you a URL like: `https://prod.xxxxx.amplifyapp.com`

### Step 10: Configure Environment Variables in Amplify Console

1. Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify)
2. Click on your app
3. Go to "Environment variables" in the left menu
4. Click "Manage variables"
5. Add these variables:
   - **Key**: `ORCHESTRATOR_ARN`
   - **Value**: `arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo`
   
   - **Key**: `AWS_REGION`
   - **Value**: `us-west-2`

6. Click "Save"

### Step 11: Redeploy

After adding environment variables, redeploy:

```bash
amplify publish
```

Or click "Redeploy this version" in Amplify Console.

## 🎉 Your Website is Live!

Your website will be available at: `https://prod.xxxxx.amplifyapp.com`

## 📱 Connect to GitHub for Continuous Deployment

### Option A: Via Amplify Console (Recommended)

1. Go to Amplify Console
2. Click your app
3. Click "Connect repository"
4. Choose GitHub
5. Authorize AWS Amplify
6. Select your repository
7. Choose branch (main/master)
8. Configure build settings (auto-detected)
9. Save and deploy

Now every `git push` will automatically deploy!

### Option B: Via CLI

```bash
# Initialize git if not already
git init
git add .
git commit -m "Initial commit"

# Create GitHub repo and push
gh repo create umrah-website --public --source=. --remote=origin --push
```

Then connect in Amplify Console as above.

## 🔧 Advanced Configuration

### Add Custom Domain

1. Go to Amplify Console
2. Click "Domain management"
3. Click "Add domain"
4. Enter your domain (e.g., `umrahtrips.com`)
5. Follow DNS configuration steps
6. Wait for SSL certificate (automatic)

### Add Authentication (Cognito)

```bash
amplify add auth

# Choose:
# - Default configuration
# - Username
# - No advanced settings

amplify push
```

### Add Database (DynamoDB)

```bash
amplify add storage

# Choose:
# - NoSQL Database
# - Provide table name
# - Add columns as needed

amplify push
```

## 📊 Monitoring

### View Logs

```bash
# Amplify logs
amplify console

# CloudWatch logs
aws logs tail /aws/lambda/umrah-api --follow
```

### View Metrics

- Go to Amplify Console
- Click "Monitoring"
- View requests, errors, latency

## 💰 Cost Breakdown

### Amplify Hosting
- **Build minutes**: $0.01/minute
- **Data served**: $0.15/GB
- **Estimate**: ~$15-20/month

### API Calls
- **Lambda**: Free tier (1M requests/month)
- **AgentCore**: Pay per invocation (~$0.002/request)
- **Estimate**: ~$10-15/month

### Total: ~$25-35/month for moderate traffic

## 🐛 Troubleshooting

### Build Fails

```bash
# Check build logs in Amplify Console
# Common fixes:
# 1. Check Node version (should be 18+)
# 2. Clear cache and rebuild
# 3. Check environment variables
```

### API Returns 500 Error

```bash
# Check CloudWatch logs
aws logs tail /aws/lambda/umrah-api --follow

# Common issues:
# 1. Missing ORCHESTRATOR_ARN environment variable
# 2. IAM permissions for Bedrock
# 3. Agent not deployed
```

### Environment Variables Not Working

1. Ensure variables are set in Amplify Console (not just .env.local)
2. Redeploy after adding variables
3. Check variable names match exactly

## 🔄 Update and Redeploy

### Manual Update

```bash
# Make changes to code
git add .
git commit -m "Update feature"
git push

# If not connected to GitHub:
amplify publish
```

### Automatic Updates

If connected to GitHub, just push:

```bash
git push origin main
```

Amplify will automatically build and deploy!

## 📚 Next Steps

1. ✅ Website deployed to Amplify
2. 🔄 Add full UI components (enhance the forms)
3. 🔄 Add authentication
4. 🔄 Add payment integration (Stripe)
5. 🔄 Add email notifications (SES)
6. 🔄 Add analytics (Google Analytics)
7. 🔄 Add SEO optimization

## 🆘 Need Help?

- **Amplify Docs**: https://docs.amplify.aws/
- **Next.js Docs**: https://nextjs.org/docs
- **AgentCore Docs**: Check your AgentCore documentation

## 🎯 Quick Commands Reference

```bash
# Local development
npm run dev

# Build locally
npm run build

# Deploy to Amplify
amplify publish

# View Amplify console
amplify console

# Check status
amplify status

# Pull latest backend config
amplify pull

# Delete everything
amplify delete
```

---

**Your website is now live on AWS Amplify! 🎉**

Share the URL with others and start planning Umrah trips!
