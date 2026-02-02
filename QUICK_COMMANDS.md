# Quick Commands Reference

## 🚀 GitHub Setup (2 minutes)

```bash
# 1. Initialize and commit
cd umrah-trip-creator
git init
git add .
git commit -m "Initial commit: Multi-agent Umrah trip creator"

# 2. Create repo on GitHub: https://github.com/new
# Name: umrah-trip-creator

# 3. Push to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/umrah-trip-creator.git
git branch -M main
git push -u origin main
```

---

## ☁️ AWS AgentCore Deployment (10 minutes)

```bash
# 1. Configure AWS
aws configure
# Enter: Access Key, Secret Key, Region (us-west-2)

# 2. Set up environment
cp .env.example .env
nano .env  # Add your API keys

# 3. Deploy
python deploy.py

# 4. Test
python test_local.py
```

---

## 🧪 Testing

```bash
# Run demo locally
streamlit run frontend/streamlit_app.py

# Test agents
python test_local.py

# View AWS logs
aws logs tail /aws/agentcore/umrah-trip-creator --follow
```

---

## 📊 Monitoring

```bash
# Check CloudFormation stack
aws cloudformation describe-stacks --stack-name umrah-trip-creator-stack

# List S3 buckets
aws s3 ls | grep umrah-trip-creator

# Check DynamoDB tables
aws dynamodb list-tables | grep umrah-trip-creator

# View costs
aws ce get-cost-and-usage --time-period Start=2026-02-01,End=2026-02-28 --granularity MONTHLY --metrics BlendedCost
```

---

## 🗑️ Cleanup

```bash
# Remove all AWS resources
python cleanup.py
# Type 'DELETE' to confirm
```

---

## 🔄 Updates

```bash
# Pull latest changes
git pull origin main

# Make changes and push
git add .
git commit -m "Your commit message"
git push origin main

# Redeploy to AWS
python deploy.py
```

---

## 🆘 Troubleshooting

```bash
# GitHub: Authentication issues
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/umrah-trip-creator.git

# AWS: Permission denied
aws iam get-user
aws sts get-caller-identity

# AWS: Stack failed
aws cloudformation describe-stack-events --stack-name umrah-trip-creator-stack

# Python: Module not found
pip install -r frontend/requirements.txt
```

---

## 📚 Documentation

- **Start Here**: [START_HERE.md](START_HERE.md)
- **Complete Guide**: [COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md)
- **GitHub Setup**: [GITHUB_SETUP.md](GITHUB_SETUP.md)
- **AWS Deployment**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Demo vs Prod**: [DEMO_VS_PRODUCTION.md](DEMO_VS_PRODUCTION.md)

---

**That's it! You're ready to go! 🎉**
