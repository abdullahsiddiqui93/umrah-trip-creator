# 🚀 Manual Deployment Steps

Your website is ready to deploy! Follow these steps:

## ✅ Prerequisites Complete

- ✅ Node.js installed (v20.20.0)
- ✅ npm installed (v10.8.2)
- ✅ Dependencies installed
- ✅ Build tested successfully
- ✅ AWS CLI configured
- ✅ Amplify CLI installed (v14.2.5)

## 📝 Deployment Steps

### Option 1: Deploy via Amplify Console (Recommended - Easiest)

This is the easiest way to deploy without CLI issues.

1. **Push code to GitHub:**
   ```bash
   cd /Users/abdlsidd/Desktop/Agentic\ AI/Project/umrah-trip-creator
   git add umrah-website/
   git commit -m "Add Next.js website"
   git push origin main
   ```

2. **Go to AWS Amplify Console:**
   - Open: https://us-west-2.console.aws.amazon.com/amplify/home?region=us-west-2
   - Click "New app" → "Host web app"
   - Choose "GitHub"
   - Authorize AWS Amplify
   - Select your repository
   - Choose branch (main/master)

3. **Configure build settings:**
   - App name: `umrah-website`
   - Environment: `prod`
   - Build settings (auto-detected):
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

4. **Deploy:**
   - Click "Save and deploy"
   - Wait 3-5 minutes
   - Get your URL: `https://main.xxxxx.amplifyapp.com`

5. **Configure environment variables:**
   - In Amplify Console, click "Environment variables"
   - Add:
     - `ORCHESTRATOR_ARN` = `arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo`
     - `AWS_REGION` = `us-west-2`
   - Click "Save"
   - Redeploy (click "Redeploy this version")

6. **Test your website!**

---

### Option 2: Deploy via Amplify CLI (Manual)

If you prefer CLI deployment:

1. **Initialize Amplify (interactive):**
   ```bash
   cd umrah-website
   export PATH="/opt/homebrew/opt/node@20/bin:$PATH"
   amplify init
   ```

   Answer the prompts:
   - Project name: `umrahwebsite`
   - Environment: `prod`
   - Default editor: (press Enter)
   - App type: `javascript`
   - Framework: `react`
   - Source directory: (press Enter)
   - Distribution directory: `.next`
   - Build command: `npm run build`
   - Start command: `npm run start`
   - AWS profile: `default`

2. **Add hosting:**
   ```bash
   amplify add hosting
   ```

   Choose:
   - Plugin: `Hosting with Amplify Console`
   - Type: `Manual deployment`

3. **Deploy:**
   ```bash
   amplify publish
   ```

4. **Configure environment variables:**
   - Go to Amplify Console
   - Add environment variables (see Option 1, step 5)
   - Redeploy: `amplify publish`

---

### Option 3: Quick Test with Vercel (Alternative)

If you want to test quickly on Vercel instead:

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   cd umrah-website
   vercel
   ```

3. **Configure environment variables:**
   ```bash
   vercel env add ORCHESTRATOR_ARN
   # Paste: arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo
   
   vercel env add AWS_REGION
   # Paste: us-west-2
   ```

4. **Redeploy:**
   ```bash
   vercel --prod
   ```

---

## 🎯 Recommended: Option 1 (Amplify Console)

**Why?**
- ✅ No CLI issues
- ✅ Visual interface
- ✅ Automatic deployments on git push
- ✅ Easy to manage
- ✅ Built-in CI/CD

---

## 📊 What Happens Next

After deployment:
1. Your website will be live at a URL
2. You can access it from anywhere
3. It will auto-scale
4. HTTPS is automatic
5. Global CDN is enabled

---

## 🐛 If You Encounter Issues

### Build Fails
- Check Node version in build settings (should be 18+)
- Review build logs
- Ensure all dependencies are in package.json

### API Errors
- Verify environment variables are set
- Check orchestrator ARN is correct
- Review CloudWatch logs

### Website Not Loading
- Wait 2-3 minutes after deployment
- Clear browser cache
- Check deployment status in console

---

## 🆘 Need Help?

Run these commands to get your current status:

```bash
# Check Node version
export PATH="/opt/homebrew/opt/node@20/bin:$PATH"
node --version

# Check npm version
npm --version

# Check Amplify version
amplify --version

# Check AWS configuration
aws configure list

# Test build locally
cd umrah-website
npm run build
```

---

## ✨ Next Steps After Deployment

1. Test the website
2. Share the URL
3. Add custom domain (optional)
4. Set up monitoring
5. Enhance features

---

**Ready to deploy? I recommend Option 1 (Amplify Console) for the easiest experience!**
