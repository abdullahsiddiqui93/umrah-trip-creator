# 🔧 Troubleshooting Guide

Common issues and solutions for deploying the Umrah website to AWS Amplify.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Build Failures](#build-failures)
3. [Deployment Errors](#deployment-errors)
4. [API Errors](#api-errors)
5. [Environment Variable Issues](#environment-variable-issues)
6. [Performance Issues](#performance-issues)
7. [GitHub Integration Issues](#github-integration-issues)

---

## Installation Issues

### Error: `npm install` fails

**Symptoms:**
```
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
```

**Solutions:**
```bash
# Try with legacy peer deps
npm install --legacy-peer-deps

# Or use force
npm install --force

# Or clear cache first
npm cache clean --force
npm install
```

### Error: Node version mismatch

**Symptoms:**
```
error: The engine "node" is incompatible with this module
```

**Solutions:**
```bash
# Check your Node version
node --version

# Should be 18.x or higher
# If not, install Node 18+:
# macOS:
brew install node@18

# Or use nvm:
nvm install 18
nvm use 18
```

---

## Build Failures

### Error: Build fails in Amplify

**Symptoms:**
- Build status shows "Failed"
- Red error message in Amplify Console

**Solutions:**

1. **Check Node version in Amplify:**
   - Go to Amplify Console
   - Click "Build settings"
   - Ensure Node version is 18 or higher
   - Add to build settings if needed:
   ```yaml
   version: 1
   frontend:
     phases:
       preBuild:
         commands:
           - nvm install 18
           - nvm use 18
           - npm ci
       build:
         commands:
           - npm run build
     artifacts:
       baseDirectory: .next
       files:
         - '**/*'
     cache:
       paths:
         - node_modules/**/*
   ```

2. **Check build logs:**
   - Go to Amplify Console
   - Click on failed build
   - Review "Build logs"
   - Look for specific error messages

3. **Clear cache and rebuild:**
   - Go to Amplify Console
   - Click "Build settings"
   - Click "Clear cache"
   - Redeploy

### Error: TypeScript errors during build

**Symptoms:**
```
Type error: Cannot find module '@/lib/types'
```

**Solutions:**
```bash
# Check tsconfig.json paths are correct
# Ensure all imports use correct paths

# Test build locally first
npm run build

# If local build works but Amplify fails:
# Check that all files are committed to git
git status
git add .
git commit -m "Fix missing files"
git push
```

---

## Deployment Errors

### Error: `amplify init` fails

**Symptoms:**
```
Error: Failed to initialize project
```

**Solutions:**
```bash
# Check AWS credentials
aws configure list

# Reconfigure if needed
aws configure

# Try with specific profile
amplify init --profile default

# If still fails, check IAM permissions
# Required permissions:
# - AmplifyFullAccess
# - CloudFormationFullAccess
# - IAMFullAccess
```

### Error: `amplify publish` fails

**Symptoms:**
```
Error: Deployment failed
```

**Solutions:**
```bash
# Check Amplify status
amplify status

# Try pushing backend first
amplify push

# Then publish
amplify publish

# If still fails, check CloudFormation
# Go to AWS Console → CloudFormation
# Look for failed stacks
# Review error messages
```

---

## API Errors

### Error: API returns 500 Internal Server Error

**Symptoms:**
- Trip generation fails
- Console shows: `Error generating trip: Failed to generate trip plan`

**Solutions:**

1. **Check environment variables:**
   ```bash
   # In Amplify Console:
   # 1. Go to Environment variables
   # 2. Verify these exist:
   ORCHESTRATOR_ARN=arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo
   AWS_REGION=us-west-2
   
   # 3. If missing, add them
   # 4. Redeploy: amplify publish
   ```

2. **Check CloudWatch logs:**
   ```bash
   # View API logs
   aws logs tail /aws/lambda/umrah-api --follow
   
   # View orchestrator logs
   aws logs tail /aws/bedrock-agentcore/runtimes/umrah_orchestrator-DFFg1bHZKo-DEFAULT --follow
   ```

3. **Verify orchestrator is deployed:**
   ```bash
   # Test orchestrator directly
   agentcore invoke \
     --agent-id umrah_orchestrator-DFFg1bHZKo \
     --session-id test-123 \
     --text "Test message"
   ```

4. **Check IAM permissions:**
   - Lambda needs permission to invoke Bedrock AgentCore
   - Add policy to Lambda execution role:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "bedrock:InvokeAgent",
           "bedrock-agentcore:InvokeAgent"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

### Error: API returns 404 Not Found

**Symptoms:**
- API endpoint not found
- Console shows: `Failed to fetch`

**Solutions:**
```bash
# Check API route exists
ls app/api/generate-trip/route.ts

# Verify build includes API routes
npm run build
# Check .next/server/app/api/generate-trip/route.js exists

# Redeploy
amplify publish
```

### Error: CORS errors

**Symptoms:**
```
Access to fetch at '...' from origin '...' has been blocked by CORS policy
```

**Solutions:**
- Next.js API routes should handle CORS automatically
- If issues persist, add CORS headers to `app/api/generate-trip/route.ts`:
```typescript
export async function POST(request: NextRequest) {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
  
  // ... rest of code
  
  return NextResponse.json(data, { headers });
}
```

---

## Environment Variable Issues

### Error: Environment variables not working

**Symptoms:**
- API works locally but fails in Amplify
- Console shows: `ORCHESTRATOR_ARN is undefined`

**Solutions:**

1. **Verify variables in Amplify Console:**
   - Go to Amplify Console
   - Click "Environment variables"
   - Ensure variables exist
   - Check spelling exactly matches code

2. **Redeploy after adding variables:**
   ```bash
   # Variables only take effect after redeploy
   amplify publish
   ```

3. **Check variable names:**
   - Must NOT have `NEXT_PUBLIC_` prefix for server-side variables
   - Server-side: `ORCHESTRATOR_ARN`
   - Client-side: `NEXT_PUBLIC_API_URL`

4. **Test locally with .env.local:**
   ```bash
   # Create .env.local
   cat > .env.local << 'EOF'
   ORCHESTRATOR_ARN=arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo
   AWS_REGION=us-west-2
   EOF
   
   # Test
   npm run dev
   ```

---

## Performance Issues

### Issue: Website loads slowly

**Solutions:**

1. **Enable caching:**
   - Amplify automatically uses CloudFront CDN
   - Check CloudFront distribution is active

2. **Optimize images:**
   - Use Next.js Image component
   - Compress images before uploading

3. **Check API response time:**
   ```bash
   # Test API locally
   time curl -X POST http://localhost:3000/api/generate-trip \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```

4. **Monitor in CloudWatch:**
   - Go to CloudWatch
   - Check Lambda duration
   - Check API Gateway latency

### Issue: API takes too long (>30 seconds)

**Solutions:**

1. **Increase Lambda timeout:**
   - Default is 30 seconds
   - May need to increase for AgentCore calls
   - Configure in Amplify settings

2. **Add loading indicators:**
   - Already implemented in UI
   - Shows "⏳ Generating..." during API call

3. **Consider async processing:**
   - For very long operations
   - Use SQS + Lambda for background processing
   - Poll for results

---

## GitHub Integration Issues

### Error: GitHub connection fails

**Symptoms:**
- Can't connect repository in Amplify Console
- Authorization fails

**Solutions:**

1. **Reauthorize GitHub:**
   - Go to GitHub Settings
   - Click "Applications"
   - Click "Authorized OAuth Apps"
   - Find "AWS Amplify"
   - Click "Revoke"
   - Try connecting again in Amplify Console

2. **Check repository permissions:**
   - Ensure you have admin access to repository
   - Repository must not be private (or Amplify needs access)

3. **Use GitHub CLI:**
   ```bash
   # Create repo with CLI
   gh repo create umrah-website --public --source=. --remote=origin --push
   
   # Then connect in Amplify Console
   ```

### Error: Automatic deployments not working

**Symptoms:**
- Push to GitHub but Amplify doesn't deploy
- No build triggered

**Solutions:**

1. **Check webhook:**
   - Go to GitHub repository
   - Click "Settings" → "Webhooks"
   - Verify Amplify webhook exists
   - Check recent deliveries for errors

2. **Check branch configuration:**
   - Go to Amplify Console
   - Click "App settings" → "General"
   - Verify correct branch is connected

3. **Manually trigger build:**
   - Go to Amplify Console
   - Click "Run build"
   - Check if build succeeds

---

## Common Error Messages

### "Cannot find module '@aws-sdk/client-bedrock-agent-runtime'"

**Solution:**
```bash
npm install @aws-sdk/client-bedrock-agent-runtime
```

### "Module not found: Can't resolve '@/lib/agentcore'"

**Solution:**
- Check file exists: `ls lib/agentcore.ts`
- Check tsconfig.json has correct paths
- Rebuild: `npm run build`

### "Error: Invalid agent ID"

**Solution:**
- Verify ORCHESTRATOR_ARN is correct
- Should be full ARN, not just agent ID
- Format: `arn:aws:bedrock-agentcore:REGION:ACCOUNT:runtime/AGENT_NAME`

### "Error: Session not found"

**Solution:**
- Session IDs are auto-generated
- Check session ID is being passed correctly
- Verify agent is deployed and accessible

---

## Getting More Help

### Check Logs

```bash
# Amplify logs
amplify console

# CloudWatch logs
aws logs tail /aws/lambda/umrah-api --follow

# AgentCore logs
aws logs tail /aws/bedrock-agentcore/runtimes/umrah_orchestrator-DFFg1bHZKo-DEFAULT --follow
```

### Debug Locally

```bash
# Run in development mode
npm run dev

# Check browser console
# Open DevTools → Console

# Check network requests
# Open DevTools → Network
```

### AWS Support

- [AWS Amplify Documentation](https://docs.amplify.aws/)
- [AWS Support Center](https://console.aws.amazon.com/support/)
- [AWS Forums](https://forums.aws.amazon.com/)

### Community Help

- [Next.js Discord](https://nextjs.org/discord)
- [AWS Discord](https://discord.gg/aws)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/aws-amplify)

---

## Still Having Issues?

If you're still stuck:

1. **Check all documentation:**
   - `README.md`
   - `AMPLIFY_DEPLOYMENT_STEPS.md`
   - `DEPLOYMENT_CHECKLIST.md`

2. **Review logs carefully:**
   - Amplify build logs
   - CloudWatch logs
   - Browser console

3. **Test components individually:**
   - Test local build: `npm run build`
   - Test API locally: `npm run dev`
   - Test orchestrator: `agentcore invoke ...`

4. **Start fresh if needed:**
   ```bash
   # Delete Amplify app
   amplify delete
   
   # Clean install
   rm -rf node_modules package-lock.json
   npm install
   
   # Redeploy
   amplify init
   amplify add hosting
   amplify publish
   ```

---

**Good luck troubleshooting!** 🔧
