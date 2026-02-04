# 🚀 Deploy to Vercel (Recommended for Next.js)

Vercel is made by the creators of Next.js and supports it perfectly, including API routes.

## ✅ Why Vercel?

- ✅ **Made for Next.js** - Perfect support for SSR and API routes
- ✅ **Free tier** - Generous free plan
- ✅ **Instant deployment** - Deploy in 2 minutes
- ✅ **Automatic HTTPS** - SSL certificate included
- ✅ **Global CDN** - Fast worldwide
- ✅ **Auto-scaling** - Handles traffic spikes
- ✅ **GitHub integration** - Auto-deploy on push

## 🎯 Deploy Now (2 Minutes)

### Step 1: Install Vercel CLI

```bash
export PATH="/opt/homebrew/opt/node@20/bin:$PATH"
npm install -g vercel
```

### Step 2: Deploy

```bash
cd umrah-website
vercel
```

Answer the prompts:
- Set up and deploy: **Y**
- Which scope: (your account)
- Link to existing project: **N**
- Project name: **umrah-website**
- Directory: **./umrah-website** (or just press Enter if already in umrah-website)
- Override settings: **N**

### Step 3: Add Environment Variables

```bash
vercel env add ORCHESTRATOR_ARN
# Paste: arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo

vercel env add BEDROCK_REGION
# Paste: us-west-2
```

### Step 4: Deploy to Production

```bash
vercel --prod
```

## 🎉 Done!

Your website will be live at: `https://umrah-website-xxxxx.vercel.app`

## 🔄 Automatic Deployments

Connect to GitHub for automatic deployments:

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Import Project"
3. Choose GitHub
4. Select your repository
5. Configure:
   - Root Directory: `umrah-website`
   - Framework: Next.js (auto-detected)
   - Environment Variables: Add the two variables above
6. Deploy

Now every `git push` will automatically deploy!

## 💰 Cost

**FREE** for personal projects!
- Unlimited deployments
- 100GB bandwidth/month
- Automatic HTTPS
- Global CDN

## 📊 vs Amplify

| Feature | Amplify Gen 1 | Vercel |
|---------|---------------|--------|
| Next.js SSR | ❌ Complex | ✅ Perfect |
| API Routes | ❌ Doesn't work | ✅ Works |
| Setup Time | 30+ minutes | 2 minutes |
| Cost | ~$25-35/month | FREE |
| Deployment | Manual/Complex | Automatic |

## 🎯 Quick Commands

```bash
# Deploy
cd umrah-website
vercel

# Deploy to production
vercel --prod

# View logs
vercel logs

# View deployments
vercel ls

# Remove project
vercel remove
```

## ✨ What You Get

- ✅ Full Next.js SSR support
- ✅ API routes working
- ✅ Real AI trip generation
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Auto-scaling
- ✅ GitHub integration
- ✅ Preview deployments
- ✅ Analytics

## 🔗 Links

- Vercel Dashboard: https://vercel.com/dashboard
- Vercel Docs: https://vercel.com/docs
- Next.js on Vercel: https://vercel.com/docs/frameworks/nextjs

---

**Ready to deploy?**

```bash
cd umrah-website
npm install -g vercel
vercel
```

Your website will be live in 2 minutes! 🚀
