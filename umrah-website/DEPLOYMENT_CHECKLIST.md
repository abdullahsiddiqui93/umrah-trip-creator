# ✅ Deployment Checklist

Use this checklist to track your deployment progress.

## Pre-Deployment

- [ ] Node.js 18+ installed (`node --version`)
- [ ] AWS CLI configured (`aws configure list`)
- [ ] AWS credentials have Amplify permissions
- [ ] You're in the `umrah-website` folder

## Installation

- [ ] Run `npm install`
- [ ] No errors during installation
- [ ] Run `npm run build` to test build
- [ ] Build completes successfully

## Local Testing (Optional)

- [ ] Run `npm run dev`
- [ ] Website opens at http://localhost:3000
- [ ] Can navigate through steps
- [ ] No console errors
- [ ] Stop server with `Ctrl+C`

## Amplify CLI Setup

- [ ] Install Amplify CLI: `npm install -g @aws-amplify/cli`
- [ ] Run `amplify configure` (if first time)
- [ ] AWS credentials configured

## Amplify Initialization

- [ ] Run `amplify init`
- [ ] Project name: `umrahwebsite`
- [ ] Environment: `prod`
- [ ] Distribution directory: `.next`
- [ ] Build command: `npm run build`
- [ ] Start command: `npm run start`
- [ ] Initialization completes successfully

## Add Hosting

- [ ] Run `amplify add hosting`
- [ ] Choose: `Hosting with Amplify Console`
- [ ] Choose: `Manual deployment`
- [ ] Hosting added successfully

## First Deployment

- [ ] Run `amplify publish`
- [ ] Build starts
- [ ] Build completes (may take 3-5 minutes)
- [ ] Deployment completes
- [ ] You receive a URL: `https://prod.xxxxx.amplifyapp.com`
- [ ] Copy and save this URL

## Test Deployed Website

- [ ] Open the Amplify URL in browser
- [ ] Website loads successfully
- [ ] Can navigate through steps
- [ ] Click "Generate My Umrah Trip Plan"
- [ ] **Expected**: API error (environment variables not set yet)

## Configure Environment Variables

- [ ] Go to [AWS Amplify Console](https://us-west-2.console.aws.amazon.com/amplify/home?region=us-west-2)
- [ ] Click on your app (`umrahwebsite`)
- [ ] Click "Environment variables" in left menu
- [ ] Click "Manage variables"
- [ ] Add variable: `ORCHESTRATOR_ARN`
  - Value: `arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo`
- [ ] Add variable: `AWS_REGION`
  - Value: `us-west-2`
- [ ] Click "Save"

## Redeploy with Environment Variables

- [ ] Run `amplify publish` again
- [ ] Build completes
- [ ] Deployment completes

## Final Testing

- [ ] Open the Amplify URL
- [ ] Navigate through all steps
- [ ] Click "Generate My Umrah Trip Plan"
- [ ] Wait for AI response (30-60 seconds)
- [ ] Trip plan displays successfully
- [ ] Flight options show real data
- [ ] Hotel options show real data
- [ ] Itinerary displays correctly

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ Website loads at Amplify URL
- ✅ All steps work correctly
- ✅ AI generates trip plans
- ✅ Real flight and hotel data displays
- ✅ No console errors
- ✅ Mobile responsive

## Optional: Connect to GitHub

- [ ] Initialize git: `git init`
- [ ] Add files: `git add .`
- [ ] Commit: `git commit -m "Initial commit"`
- [ ] Create GitHub repo: `gh repo create umrah-website --public --source=. --remote=origin --push`
- [ ] Go to Amplify Console
- [ ] Click "Connect repository"
- [ ] Choose GitHub
- [ ] Authorize AWS Amplify
- [ ] Select repository
- [ ] Choose branch
- [ ] Save
- [ ] Test: Make a change, commit, push
- [ ] Verify: Amplify automatically deploys

## Optional: Add Custom Domain

- [ ] Go to Amplify Console
- [ ] Click "Domain management"
- [ ] Click "Add domain"
- [ ] Enter domain name
- [ ] Follow DNS configuration
- [ ] Wait for SSL certificate
- [ ] Test: Visit custom domain
- [ ] Verify: HTTPS works

## Monitoring Setup

- [ ] Go to Amplify Console
- [ ] Click "Monitoring"
- [ ] Review metrics dashboard
- [ ] Set up CloudWatch alarms (optional)
- [ ] Configure SNS notifications (optional)

## Documentation

- [ ] Save Amplify URL
- [ ] Document environment variables
- [ ] Note any custom configurations
- [ ] Share URL with team/users

## Troubleshooting Checklist

If something doesn't work:

### Build Fails
- [ ] Check Node version in Amplify build settings
- [ ] Review build logs in Amplify Console
- [ ] Verify all dependencies in package.json
- [ ] Try: Clear cache and rebuild

### API Errors
- [ ] Verify ORCHESTRATOR_ARN is set correctly
- [ ] Check AWS_REGION is set to `us-west-2`
- [ ] Verify orchestrator agent is deployed
- [ ] Check CloudWatch logs
- [ ] Verify IAM permissions

### Website Not Loading
- [ ] Wait 2-3 minutes after deployment
- [ ] Clear browser cache
- [ ] Try incognito/private mode
- [ ] Check Amplify Console for errors
- [ ] Verify deployment status is "Deployed"

### Environment Variables Not Working
- [ ] Verify variables are in Amplify Console (not .env.local)
- [ ] Check variable names match exactly
- [ ] Redeploy after adding variables
- [ ] Check build logs for variable loading

## Cost Monitoring

- [ ] Set up AWS Budgets
- [ ] Configure cost alerts
- [ ] Review monthly costs
- [ ] Expected: ~$25-35/month

## Security Checklist

- [ ] HTTPS enabled (automatic)
- [ ] Environment variables not in code
- [ ] No API keys in frontend
- [ ] CORS configured correctly
- [ ] Rate limiting considered

## Performance Checklist

- [ ] Website loads in <3 seconds
- [ ] Images optimized
- [ ] API responses <5 seconds
- [ ] Mobile performance good
- [ ] Lighthouse score >80

## Next Steps After Deployment

- [ ] Add authentication (Cognito)
- [ ] Add payment integration
- [ ] Add booking confirmation emails
- [ ] Add user dashboard
- [ ] Add analytics (Google Analytics)
- [ ] Add SEO optimization
- [ ] Add error tracking (Sentry)

---

## 📊 Deployment Status

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

- Pre-Deployment: ⬜
- Installation: ⬜
- Local Testing: ⬜
- Amplify Setup: ⬜
- First Deployment: ⬜
- Environment Variables: ⬜
- Final Testing: ⬜
- GitHub Connection: ⬜
- Custom Domain: ⬜

---

## 🆘 Quick Help

**Build fails?** Check build logs in Amplify Console

**API errors?** Verify environment variables are set

**Website not loading?** Wait 2-3 minutes, clear cache

**Need help?** Check `AMPLIFY_DEPLOYMENT_STEPS.md`

---

## 🎯 Quick Deploy Commands

```bash
cd umrah-website
npm install
amplify init
amplify add hosting
amplify publish
```

Then configure environment variables in Amplify Console and run `amplify publish` again.

---

**Good luck with your deployment!** 🚀
