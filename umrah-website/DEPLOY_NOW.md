# 🚀 Deploy Your Umrah Website NOW

## ✅ Everything is Ready!

Your Next.js website is fully configured and ready to deploy to AWS Amplify.

## 🎯 Quick Deploy (5 Minutes)

### Step 1: Navigate to Project
```bash
cd umrah-website
```

### Step 2: Install Dependencies
```bash
npm install
```

### Step 3: Test Locally (Optional)
```bash
npm run dev
```
Open http://localhost:3000 to preview.

Press `Ctrl+C` to stop when done.

### Step 4: Install Amplify CLI
```bash
npm install -g @aws-amplify/cli
```

### Step 5: Initialize Amplify
```bash
amplify init
```

**Answer the prompts:**
- Project name: `umrahwebsite`
- Environment: `prod`
- Default editor: (your choice - just press Enter)
- App type: `javascript`
- Framework: `react`
- Source directory: (press Enter)
- Distribution directory: `.next`
- Build command: `npm run build`
- Start command: `npm run start`
- AWS profile: `default`

### Step 6: Add Hosting
```bash
amplify add hosting
```

**Choose:**
- Plugin: `Hosting with Amplify Console`
- Type: `Manual deployment`

### Step 7: Deploy!
```bash
amplify publish
```

This will:
1. Build your Next.js app
2. Upload to AWS
3. Deploy to Amplify
4. Give you a live URL

**Your website will be live at:** `https://prod.xxxxx.amplifyapp.com`

### Step 8: Configure Environment Variables

1. Go to [AWS Amplify Console](https://us-west-2.console.aws.amazon.com/amplify/home?region=us-west-2)
2. Click on your app (`umrahwebsite`)
3. Click "Environment variables" in left menu
4. Click "Manage variables"
5. Add these variables:

```
ORCHESTRATOR_ARN = arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo
AWS_REGION = us-west-2
```

6. Click "Save"

### Step 9: Redeploy with Environment Variables
```bash
amplify publish
```

## 🎉 Done! Your Website is Live!

Visit your Amplify URL to see your website in action.

## 🔗 Connect to GitHub (Optional but Recommended)

For automatic deployments on every `git push`:

### Option 1: Via Amplify Console
1. Go to Amplify Console
2. Click your app
3. Click "App settings" → "General"
4. Click "Connect repository"
5. Choose GitHub
6. Authorize AWS Amplify
7. Select your repository
8. Choose branch (main/master)
9. Save

Now every `git push` will automatically deploy!

### Option 2: Via GitHub CLI
```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# Create GitHub repo
gh repo create umrah-website --public --source=. --remote=origin --push
```

Then connect in Amplify Console as above.

## 📱 Add Custom Domain (Optional)

1. Go to Amplify Console
2. Click "Domain management"
3. Click "Add domain"
4. Enter your domain (e.g., `umrahtrips.com`)
5. Follow DNS configuration steps
6. Wait for SSL certificate (automatic)

## 🐛 Troubleshooting

### Build Fails
```bash
# Check logs in Amplify Console
# Common fixes:
# 1. Ensure Node 18+ is selected in build settings
# 2. Clear cache and rebuild
# 3. Check environment variables are set
```

### API Returns Error
```bash
# Check CloudWatch logs
aws logs tail /aws/lambda/umrah-api --follow

# Common issues:
# 1. ORCHESTRATOR_ARN not set in Amplify Console
# 2. IAM permissions missing
# 3. Agent not deployed
```

### Environment Variables Not Working
1. Ensure variables are set in **Amplify Console** (not just .env.local)
2. Redeploy after adding variables: `amplify publish`
3. Check variable names match exactly

## 💰 Cost Estimate

**~$25-35/month** for moderate traffic

- Amplify Hosting: ~$15-20/month
- Lambda/API Gateway: Free tier
- AgentCore: ~$10-15/month

## 📊 Monitor Your Website

### View Logs
```bash
# Amplify console
amplify console

# CloudWatch logs
aws logs tail /aws/lambda/umrah-api --follow
```

### View Metrics
- Go to Amplify Console
- Click "Monitoring"
- View requests, errors, latency

## 🔄 Update Your Website

### If Connected to GitHub
```bash
# Make changes
git add .
git commit -m "Update feature"
git push

# Amplify will automatically deploy!
```

### If Not Connected to GitHub
```bash
# Make changes
amplify publish
```

## 📚 Next Steps

### Immediate:
- ✅ Deploy to Amplify (you're doing this now!)
- ✅ Test the website
- ✅ Share the URL

### Short-term:
- Add full form fields for all steps
- Add authentication with Cognito
- Add payment integration (Stripe)
- Add booking confirmation emails

### Long-term:
- Add user dashboard
- Add booking history
- Add reviews and ratings
- Add multi-language support

## 🆘 Need Help?

1. Check `AMPLIFY_DEPLOYMENT_STEPS.md` for detailed guide
2. Check `README.md` for project overview
3. Check AWS Amplify docs: https://docs.amplify.aws/
4. Check CloudWatch logs for errors

## ✨ What You're Getting

Your website will have:
- ✅ Professional, modern design
- ✅ AI-powered trip planning
- ✅ Real-time flight and hotel search
- ✅ Mobile-friendly interface
- ✅ Fast loading (Next.js optimization)
- ✅ Automatic HTTPS
- ✅ Global CDN (CloudFront)
- ✅ Auto-scaling
- ✅ SEO-friendly

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

# Delete everything
amplify delete
```

---

## 🚀 Ready? Let's Deploy!

Run these commands now:

```bash
cd umrah-website
npm install
amplify init
amplify add hosting
amplify publish
```

**Your website will be live in ~5 minutes!** 🎉

---

**Questions?** Check the documentation files or ask for help.

**Happy deploying!** 🎊
