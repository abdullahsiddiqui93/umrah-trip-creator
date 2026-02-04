# Manual User Verification Guide

If you didn't receive the verification email, you can manually verify your account using AWS CLI.

## Step 1: Find Your Username

```bash
aws cognito-idp list-users --user-pool-id us-west-2_AAvuQJ0g6
```

This will show all users. Look for your email address in the output.

## Step 2: Manually Confirm Your Account

Replace `YOUR_EMAIL@example.com` with your actual email:

```bash
aws cognito-idp admin-confirm-sign-up \
  --user-pool-id us-west-2_AAvuQJ0g6 \
  --username YOUR_EMAIL@example.com
```

## Step 3: Sign In

After running the command above, go back to http://localhost:8501 and sign in with your email and password!

## Alternative: Set Password Directly

If you want to set a new password without verification:

```bash
aws cognito-idp admin-set-user-password \
  --user-pool-id us-west-2_AAvuQJ0g6 \
  --username YOUR_EMAIL@example.com \
  --password "YourNewPassword123!" \
  --permanent
```

Then confirm the user:

```bash
aws cognito-idp admin-confirm-sign-up \
  --user-pool-id us-west-2_AAvuQJ0g6 \
  --username YOUR_EMAIL@example.com
```

## Why No Email?

Cognito User Pools in development mode have limited email sending capabilities:
- **Sandbox Mode**: AWS SES (email service) starts in sandbox mode
- **Limit**: Only 1 email per second, 200 emails per day
- **Verification**: Only verified email addresses can receive emails

### To Fix Email Sending (Optional):

1. **Verify Your Email in SES**:
   ```bash
   aws ses verify-email-identity --email-address your@email.com --region us-west-2
   ```
   Then check your email and click the verification link.

2. **Request Production Access** (for unlimited emails):
   - Go to AWS Console → SES → Account Dashboard
   - Click "Request production access"
   - Fill out the form explaining your use case

3. **Configure Cognito to Use SES**:
   ```bash
   aws cognito-idp update-user-pool \
     --user-pool-id us-west-2_AAvuQJ0g6 \
     --email-configuration SourceArn=arn:aws:ses:us-west-2:985444479029:identity/your@email.com
   ```

## Quick Fix: Use Demo Mode

If you just want to test the app without dealing with email verification:

1. Edit `.env` file:
   ```
   DEMO_MODE=true
   ```

2. Restart Streamlit:
   ```bash
   streamlit run frontend/streamlit_app.py
   ```

3. You'll be auto-logged in as "Demo User"

---

**Note**: For production use, you'll want to properly configure SES and move out of sandbox mode.
