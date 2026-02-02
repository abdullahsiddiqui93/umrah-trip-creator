# AWS Cognito Authentication Guide

Complete guide to authentication in Umrah Trip Creator using AWS Cognito.

---

## 🔐 Overview

The system uses **AWS Cognito** for secure user authentication with:
- ✅ Email/password sign up and sign in
- ✅ Email verification
- ✅ Password reset flow
- ✅ Session management with JWT tokens
- ✅ Secure token refresh
- ✅ User profile management

---

## 🎭 Demo Mode vs Production

### Demo Mode (Default)
- **No authentication required**
- Automatically logs in as "Demo User"
- Perfect for testing and development
- Set `DEMO_MODE=true` in `.env`

### Production Mode
- **Full Cognito authentication**
- Users must sign up and verify email
- Secure JWT token-based sessions
- Set `DEMO_MODE=false` in `.env`

---

## 🚀 Quick Setup

### Step 1: Deploy Cognito (Automatic)

```bash
# Deploy infrastructure (includes Cognito)
python deploy.py
```

This creates:
- Cognito User Pool
- User Pool Client
- Identity Pool
- IAM roles for authenticated users

### Step 2: Get Cognito IDs

```bash
# Get User Pool ID
aws cloudformation describe-stacks \
  --stack-name umrah-trip-creator-stack \
  --query 'Stacks[0].Outputs[?OutputKey==`UserPoolId`].OutputValue' \
  --output text

# Get Client ID
aws cloudformation describe-stacks \
  --stack-name umrah-trip-creator-stack \
  --query 'Stacks[0].Outputs[?OutputKey==`UserPoolClientId`].OutputValue' \
  --output text
```

### Step 3: Update .env

```bash
# Edit .env file
nano .env
```

Add:
```bash
# Enable production mode
DEMO_MODE=false

# Add Cognito IDs (from step 2)
COGNITO_USER_POOL_ID=us-west-2_xxxxxxxxx
COGNITO_CLIENT_ID=your-client-id
```

### Step 4: Restart App

```bash
streamlit run frontend/streamlit_app.py
```

Now you'll see the login page!

---

## 📱 User Flows

### 1. Sign Up Flow

```
User visits app
  ↓
Sees "Create Account" button
  ↓
Fills: Name, Email, Password
  ↓
Clicks "Create Account"
  ↓
Receives verification email
  ↓
Enters 6-digit code
  ↓
Account verified!
  ↓
Redirected to login
```

**Password Requirements:**
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character

### 2. Sign In Flow

```
User visits app
  ↓
Enters email and password
  ↓
Clicks "Sign In"
  ↓
Cognito validates credentials
  ↓
Returns JWT tokens:
  - ID Token (user identity)
  - Access Token (API access)
  - Refresh Token (renew session)
  ↓
User authenticated!
  ↓
Redirected to main app
```

### 3. Forgot Password Flow

```
User clicks "Forgot Password?"
  ↓
Enters email
  ↓
Receives reset code via email
  ↓
Enters code + new password
  ↓
Password reset!
  ↓
Can now sign in
```

### 4. Sign Out Flow

```
User clicks "Sign Out"
  ↓
Tokens invalidated
  ↓
Session cleared
  ↓
Redirected to login
```

---

## 🔑 Token Management

### Token Types

1. **ID Token**
   - Contains user identity info
   - Used for user profile
   - Valid for 1 hour

2. **Access Token**
   - Used for API authorization
   - Grants access to AWS resources
   - Valid for 1 hour

3. **Refresh Token**
   - Used to get new access/ID tokens
   - Valid for 30 days
   - Automatically refreshed

### Token Storage

Tokens are stored in Streamlit session state:
```python
st.session_state.access_token
st.session_state.refresh_token
st.session_state.id_token
```

### Auto-Refresh

Tokens are automatically refreshed when expired:
```python
# In auth.py
def refresh_token(self, refresh_token):
    # Gets new access and ID tokens
    # Refresh token remains valid
```

---

## 🛡️ Security Features

### 1. Password Policy
- Enforced by Cognito
- Minimum complexity requirements
- Prevents weak passwords

### 2. Email Verification
- Required before first login
- Prevents fake accounts
- Confirms user identity

### 3. Token Encryption
- JWT tokens are signed
- Cannot be tampered with
- Expire automatically

### 4. Secure Storage
- Tokens never stored in cookies
- Only in server-side session
- Cleared on sign out

### 5. HTTPS Only
- All auth requests over HTTPS
- Tokens encrypted in transit
- Prevents man-in-the-middle attacks

---

## 👤 User Profile

### Stored Attributes

```python
{
    'email': 'user@example.com',
    'name': 'John Smith',
    'email_verified': True,
    'sub': 'uuid-user-id'
}
```

### Access User Info

```python
# In your code
user_email = st.session_state.user_email
user_name = st.session_state.user_name

# Get full profile
auth = CognitoAuth()
user_info = auth.get_user(st.session_state.access_token)
```

---

## 🔧 Customization

### Custom Email Templates

Edit in AWS Console:
1. Go to Cognito → User Pools
2. Select your pool
3. Message customizations
4. Edit verification/reset emails

### Custom Domain

```bash
# Add custom domain
aws cognito-idp create-user-pool-domain \
  --domain your-domain \
  --user-pool-id us-west-2_xxxxxxxxx
```

### MFA (Multi-Factor Auth)

Enable in CloudFormation:
```yaml
UserPool:
  Type: AWS::Cognito::UserPool
  Properties:
    MfaConfiguration: OPTIONAL
    EnabledMfas:
      - SOFTWARE_TOKEN_MFA
```

---

## 🧪 Testing Authentication

### Test Sign Up

```bash
# Using AWS CLI
aws cognito-idp sign-up \
  --client-id YOUR_CLIENT_ID \
  --username test@example.com \
  --password TestPass123! \
  --user-attributes Name=email,Value=test@example.com Name=name,Value="Test User"
```

### Test Sign In

```bash
aws cognito-idp initiate-auth \
  --client-id YOUR_CLIENT_ID \
  --auth-flow USER_PASSWORD_AUTH \
  --auth-parameters USERNAME=test@example.com,PASSWORD=TestPass123!
```

### Verify Email (Admin)

```bash
# Skip email verification for testing
aws cognito-idp admin-confirm-sign-up \
  --user-pool-id us-west-2_xxxxxxxxx \
  --username test@example.com
```

---

## 📊 Monitoring

### CloudWatch Metrics

Monitor in AWS Console:
- Sign-up attempts
- Sign-in successes/failures
- Token refresh rate
- User pool size

### Custom Logging

```python
# In auth.py
import logging

logger = logging.getLogger(__name__)

def sign_in(self, email, password):
    logger.info(f"Sign-in attempt for {email}")
    # ... auth logic
    logger.info(f"Sign-in successful for {email}")
```

---

## 🐛 Troubleshooting

### "User not found"
- User hasn't signed up yet
- Check email spelling
- Verify user pool ID is correct

### "Incorrect username or password"
- Wrong password
- Account not verified
- Check Caps Lock

### "User is not confirmed"
- Email not verified
- Resend verification code
- Or use admin-confirm-sign-up

### "Invalid verification code"
- Code expired (valid 24 hours)
- Wrong code entered
- Request new code

### "Token expired"
- Session timed out
- Use refresh token
- Or sign in again

### "Access denied"
- Missing IAM permissions
- Check Cognito policies
- Verify identity pool roles

---

## 💰 Costs

### Cognito Pricing

**Free Tier:**
- 50,000 MAUs (Monthly Active Users)
- Includes all features

**Beyond Free Tier:**
- $0.0055 per MAU (50K-100K)
- $0.0046 per MAU (100K-1M)
- $0.00325 per MAU (>1M)

**Example:**
- 1,000 users/month: **FREE**
- 10,000 users/month: **FREE**
- 100,000 users/month: **$275/month**

---

## 🔄 Migration from Demo to Production

### Step 1: Enable Production Mode

```bash
# In .env
DEMO_MODE=false
```

### Step 2: Deploy Cognito

```bash
python deploy.py
```

### Step 3: Update Environment

```bash
# Get Cognito IDs
aws cloudformation describe-stacks \
  --stack-name umrah-trip-creator-stack

# Add to .env
COGNITO_USER_POOL_ID=...
COGNITO_CLIENT_ID=...
```

### Step 4: Test

```bash
# Restart app
streamlit run frontend/streamlit_app.py

# Try signing up
# Verify email
# Sign in
```

### Step 5: Migrate Demo Users (Optional)

```python
# Script to create users from demo data
import boto3

client = boto3.client('cognito-idp')

users = [
    {'email': 'user1@example.com', 'name': 'User One'},
    {'email': 'user2@example.com', 'name': 'User Two'},
]

for user in users:
    client.admin_create_user(
        UserPoolId='us-west-2_xxxxxxxxx',
        Username=user['email'],
        UserAttributes=[
            {'Name': 'email', 'Value': user['email']},
            {'Name': 'name', 'Value': user['name']},
            {'Name': 'email_verified', 'Value': 'true'}
        ],
        TemporaryPassword='TempPass123!',
        MessageAction='SUPPRESS'  # Don't send email
    )
```

---

## 📚 Additional Resources

### AWS Documentation
- [Cognito User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html)
- [Cognito Identity Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-identity.html)
- [JWT Tokens](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-with-identity-providers.html)

### Code Examples
- `frontend/auth.py` - Authentication module
- `frontend/streamlit_app.py` - Integration example
- `deploy.py` - Cognito deployment

---

## ✅ Checklist

Before going to production:

- [ ] Deploy Cognito via CloudFormation
- [ ] Get User Pool ID and Client ID
- [ ] Update .env with Cognito IDs
- [ ] Set DEMO_MODE=false
- [ ] Test sign up flow
- [ ] Test email verification
- [ ] Test sign in flow
- [ ] Test password reset
- [ ] Test sign out
- [ ] Customize email templates
- [ ] Set up monitoring
- [ ] Review security settings
- [ ] Test token refresh
- [ ] Document for users

---

**Your authentication is now production-ready! 🔐**
