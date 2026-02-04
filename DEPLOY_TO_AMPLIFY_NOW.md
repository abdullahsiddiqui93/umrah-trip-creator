# 🚀 Deploy Your Website to AWS Amplify NOW

## ✅ Everything is Ready!

Your website is built and tested. Let's deploy it!

## 🎯 Easiest Method: Amplify Console (Recommended)

### Step 1: Push Code to GitHub

```bash
# Add all files
git add .

# Commit
git commit -m "Add Next.js Umrah website"

# Push to GitHub
git push origin main
```

### Step 2: Deploy via Amplify Console

1. **Open AWS Amplify Console:**
   - Go to: https://us-west-2.console.aws.amazon.com/amplify/home?region=us-west-2
   - Click "Create new app" or "New app" → "Host web app"

2. **Connect Repository:**
   - Choose "GitHub"
   - Click "Continue"
   - Authorize AWS Amplify (if first time)
   - Select your repository: `umrah-trip-creator`
   - Select branch: `main`
   - Click "Next"

3. **Configure Build Settings:**
   - App name: `umrah-website`
   - Environment: `prod`
   
   **IMPORTANT**: Update the build settings to:
   ```yaml
   version: 1
   frontend:
     phases:
       preBuild:
         commands:
           - cd umrah-website
           - npm ci
       build:
         commands:
           - npm run build
     artifacts:
       baseDirectory: umrah-website/.next
       files:
         - '**/*'
     cache:
       paths:
         - umrah-website/node_modules/**/*
   ```
   
   - Click "Next"

4. **Review and Deploy:**
   - Review settings
   - Click "Save and deploy"
   - Wait 3-5 minutes for deployment

5. **Get Your URL:**
   - After deployment completes, you'll see: `https://main.xxxxx.amplifyapp.com`
   - Copy this URL

### Step 3: Configure Environment Variables

1. **In Amplify Console:**
   - Click on your app
   - Go to "Environment variables" in left menu
   - Click "Manage variables"

2. **Add Variables:**
   - Click "Add variable"
   - Key: `ORCHESTRATOR_ARN`
   - Value: `arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo`
   
   - Click "Add variable" again
   - Key: `AWS_REGION`
   - Value: `us-west-2`
   
   - Click "Save"

3. **Redeploy:**
   - Go back to your app
   - Click "Redeploy this version"
   - Wait 2-3 minutes

### Step 4: Test Your Website!

1. Open your Amplify URL
2. Navigate through the steps
3. Click "Generate My Umrah Trip Plan"
4. Wait 30-60 seconds for AI response
5. Verify flight and hotel options display

## 🎉 Success!

Your website is now live and accessible worldwide!

---

## 🔄 Automatic Deployments

Now every time you push to GitHub, Amplify will automatically deploy:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Amplify automatically deploys!
```

---

## 📱 Add Custom Domain (Optional)

1. In Amplify Console, click "Domain management"
2. Click "Add domain"
3. Enter your domain (e.g., `umrahtrips.com`)
4. Follow DNS configuration steps
5. Wait for SSL certificate (automatic)

---

## 📊 Monitor Your Website

### View Logs:
- Amplify Console → Click your app → "Monitoring"
- View build logs, access logs, errors

### CloudWatch Logs:
```bash
# API logs
aws logs tail /aws/lambda/umrah-api --follow

# AgentCore logs
aws logs tail /aws/bedrock-agentcore/runtimes/umrah_orchestrator-DFFg1bHZKo-DEFAULT --follow
```

---

## 🐛 Troubleshooting

### Build Fails:
1. Check build logs in Amplify Console
2. Verify build settings point to `umrah-website/` folder
3. Ensure Node 18+ is used

### API Errors:
1. Verify environment variables are set
2. Check orchestrator ARN is correct
3. Review CloudWatch logs

### Website Not Loading:
1. Wait 2-3 minutes after deployment
2. Clear browser cache
3. Try incognito mode

---

## 💰 Cost

Your website will cost approximately:
- **Amplify Hosting**: ~$15-20/month
- **AgentCore**: ~$10-15/month
- **Total**: ~$25-35/month

---

## ✨ What You Get

- ✅ Professional website live on AWS
- ✅ Automatic HTTPS
- ✅ Global CDN (CloudFront)
- ✅ Auto-scaling
- ✅ Automatic deployments on git push
- ✅ Mobile-friendly
- ✅ SEO-optimized

---

## 🎯 Next Steps

1. ✅ Deploy to Amplify (you're doing this now!)
2. Test the website thoroughly
3. Share the URL with users
4. Add custom domain (optional)
5. Enhance features (authentication, payment, etc.)

---

## 📞 Need Help?

Check these files:
- `umrah-website/MANUAL_DEPLOYMENT.md` - Alternative deployment methods
- `umrah-website/TROUBLESHOOTING.md` - Fix common issues
- `umrah-website/README.md` - Project overview

---

**Ready? Let's deploy!**

Run these commands now:

```bash
git add .
git commit -m "Add Next.js Umrah website"
git push origin main
```

Then follow Step 2 above to deploy via Amplify Console!

🚀 **Your website will be live in 5 minutes!**
