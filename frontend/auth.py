"""
AWS Cognito Authentication Module for Umrah Trip Creator
"""

import boto3
import hmac
import hashlib
import base64
import os
import streamlit as st
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()


class CognitoAuth:
    """Handle AWS Cognito authentication"""
    
    def __init__(self):
        self.region = os.getenv('AWS_REGION', 'us-west-2')
        self.user_pool_id = os.getenv('COGNITO_USER_POOL_ID')
        self.client_id = os.getenv('COGNITO_CLIENT_ID')
        self.client_secret = os.getenv('COGNITO_CLIENT_SECRET')
        
        self.client = boto3.client('cognito-idp', region_name=self.region)
    
    def _get_secret_hash(self, username):
        """Calculate secret hash for Cognito"""
        if not self.client_secret:
            return None
        
        message = bytes(username + self.client_id, 'utf-8')
        secret = bytes(self.client_secret, 'utf-8')
        dig = hmac.new(secret, message, hashlib.sha256).digest()
        return base64.b64encode(dig).decode()
    
    def sign_up(self, email, password, name):
        """Register a new user"""
        try:
            params = {
                'ClientId': self.client_id,
                'Username': email,
                'Password': password,
                'UserAttributes': [
                    {'Name': 'email', 'Value': email},
                    {'Name': 'name', 'Value': name}
                ]
            }
            
            if self.client_secret:
                params['SecretHash'] = self._get_secret_hash(email)
            
            response = self.client.sign_up(**params)
            
            return {
                'success': True,
                'message': 'Account created! Please check your email for verification code.',
                'user_sub': response['UserSub']
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            
            if error_code == 'UsernameExistsException':
                return {'success': False, 'message': 'Email already registered'}
            elif error_code == 'InvalidPasswordException':
                return {'success': False, 'message': 'Password does not meet requirements'}
            elif error_code == 'InvalidParameterException':
                return {'success': False, 'message': 'Invalid email or password format'}
            else:
                return {'success': False, 'message': f'Registration failed: {str(e)}'}
    
    def confirm_sign_up(self, email, code):
        """Confirm user registration with verification code"""
        try:
            params = {
                'ClientId': self.client_id,
                'Username': email,
                'ConfirmationCode': code
            }
            
            if self.client_secret:
                params['SecretHash'] = self._get_secret_hash(email)
            
            self.client.confirm_sign_up(**params)
            
            return {'success': True, 'message': 'Email verified successfully!'}
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            
            if error_code == 'CodeMismatchException':
                return {'success': False, 'message': 'Invalid verification code'}
            elif error_code == 'ExpiredCodeException':
                return {'success': False, 'message': 'Verification code expired'}
            else:
                return {'success': False, 'message': f'Verification failed: {str(e)}'}
    
    def sign_in(self, email, password):
        """Sign in user"""
        try:
            params = {
                'ClientId': self.client_id,
                'AuthFlow': 'USER_PASSWORD_AUTH',
                'AuthParameters': {
                    'USERNAME': email,
                    'PASSWORD': password
                }
            }
            
            if self.client_secret:
                params['AuthParameters']['SECRET_HASH'] = self._get_secret_hash(email)
            
            response = self.client.initiate_auth(**params)
            
            return {
                'success': True,
                'message': 'Login successful!',
                'tokens': {
                    'id_token': response['AuthenticationResult']['IdToken'],
                    'access_token': response['AuthenticationResult']['AccessToken'],
                    'refresh_token': response['AuthenticationResult']['RefreshToken']
                }
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            
            if error_code == 'NotAuthorizedException':
                return {'success': False, 'message': 'Incorrect email or password'}
            elif error_code == 'UserNotConfirmedException':
                return {'success': False, 'message': 'Please verify your email first'}
            elif error_code == 'UserNotFoundException':
                return {'success': False, 'message': 'User not found'}
            else:
                return {'success': False, 'message': f'Login failed: {str(e)}'}
    
    def sign_out(self, access_token):
        """Sign out user"""
        try:
            self.client.global_sign_out(AccessToken=access_token)
            return {'success': True, 'message': 'Signed out successfully'}
        except ClientError as e:
            return {'success': False, 'message': f'Sign out failed: {str(e)}'}
    
    def forgot_password(self, email):
        """Initiate forgot password flow"""
        try:
            params = {
                'ClientId': self.client_id,
                'Username': email
            }
            
            if self.client_secret:
                params['SecretHash'] = self._get_secret_hash(email)
            
            self.client.forgot_password(**params)
            
            return {
                'success': True,
                'message': 'Password reset code sent to your email'
            }
            
        except ClientError as e:
            return {'success': False, 'message': f'Failed to send reset code: {str(e)}'}
    
    def confirm_forgot_password(self, email, code, new_password):
        """Confirm forgot password with code"""
        try:
            params = {
                'ClientId': self.client_id,
                'Username': email,
                'ConfirmationCode': code,
                'Password': new_password
            }
            
            if self.client_secret:
                params['SecretHash'] = self._get_secret_hash(email)
            
            self.client.confirm_forgot_password(**params)
            
            return {'success': True, 'message': 'Password reset successfully!'}
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            
            if error_code == 'CodeMismatchException':
                return {'success': False, 'message': 'Invalid reset code'}
            elif error_code == 'ExpiredCodeException':
                return {'success': False, 'message': 'Reset code expired'}
            else:
                return {'success': False, 'message': f'Password reset failed: {str(e)}'}
    
    def get_user(self, access_token):
        """Get user information"""
        try:
            response = self.client.get_user(AccessToken=access_token)
            
            user_attributes = {attr['Name']: attr['Value'] 
                             for attr in response['UserAttributes']}
            
            return {
                'success': True,
                'username': response['Username'],
                'email': user_attributes.get('email'),
                'name': user_attributes.get('name'),
                'email_verified': user_attributes.get('email_verified') == 'true'
            }
            
        except ClientError as e:
            return {'success': False, 'message': f'Failed to get user: {str(e)}'}
    
    def refresh_token(self, refresh_token):
        """Refresh access token"""
        try:
            params = {
                'ClientId': self.client_id,
                'AuthFlow': 'REFRESH_TOKEN_AUTH',
                'AuthParameters': {
                    'REFRESH_TOKEN': refresh_token
                }
            }
            
            response = self.client.initiate_auth(**params)
            
            return {
                'success': True,
                'tokens': {
                    'id_token': response['AuthenticationResult']['IdToken'],
                    'access_token': response['AuthenticationResult']['AccessToken']
                }
            }
            
        except ClientError as e:
            return {'success': False, 'message': f'Token refresh failed: {str(e)}'}


def init_session_state():
    """Initialize authentication session state"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'access_token' not in st.session_state:
        st.session_state.access_token = None
    if 'refresh_token' not in st.session_state:
        st.session_state.refresh_token = None
    if 'auth_page' not in st.session_state:
        st.session_state.auth_page = 'login'


def show_login_page(auth):
    """Display login page"""
    st.markdown("### 🔐 Sign In")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Sign In", use_container_width=True)
        with col2:
            if st.form_submit_button("Create Account", use_container_width=True):
                st.session_state.auth_page = 'signup'
                st.rerun()
        
        if submit:
            if email and password:
                with st.spinner("Signing in..."):
                    result = auth.sign_in(email, password)
                
                if result['success']:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.session_state.access_token = result['tokens']['access_token']
                    st.session_state.refresh_token = result['tokens']['refresh_token']
                    
                    # Get user details
                    user_info = auth.get_user(result['tokens']['access_token'])
                    if user_info['success']:
                        st.session_state.user_name = user_info.get('name', email)
                    
                    st.success(result['message'])
                    st.rerun()
                else:
                    st.error(result['message'])
            else:
                st.error("Please enter email and password")
    
    if st.button("Forgot Password?"):
        st.session_state.auth_page = 'forgot_password'
        st.rerun()


def show_signup_page(auth):
    """Display signup page"""
    st.markdown("### 📝 Create Account")
    
    with st.form("signup_form"):
        name = st.text_input("Full Name", placeholder="John Smith")
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password", 
                                help="Min 8 characters, uppercase, lowercase, number, special char")
        password_confirm = st.text_input("Confirm Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Create Account", use_container_width=True)
        with col2:
            if st.form_submit_button("Back to Login", use_container_width=True):
                st.session_state.auth_page = 'login'
                st.rerun()
        
        if submit:
            if not all([name, email, password, password_confirm]):
                st.error("Please fill in all fields")
            elif password != password_confirm:
                st.error("Passwords do not match")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters")
            else:
                with st.spinner("Creating account..."):
                    result = auth.sign_up(email, password, name)
                
                if result['success']:
                    st.success(result['message'])
                    st.session_state.auth_page = 'verify'
                    st.session_state.pending_email = email
                    st.rerun()
                else:
                    st.error(result['message'])


def show_verify_page(auth):
    """Display email verification page"""
    st.markdown("### ✉️ Verify Email")
    st.info(f"We sent a verification code to {st.session_state.get('pending_email', 'your email')}")
    
    with st.form("verify_form"):
        code = st.text_input("Verification Code", placeholder="123456")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Verify", use_container_width=True)
        with col2:
            if st.form_submit_button("Back to Login", use_container_width=True):
                st.session_state.auth_page = 'login'
                st.rerun()
        
        if submit:
            if code:
                with st.spinner("Verifying..."):
                    result = auth.confirm_sign_up(st.session_state.pending_email, code)
                
                if result['success']:
                    st.success(result['message'])
                    st.session_state.auth_page = 'login'
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(result['message'])
            else:
                st.error("Please enter verification code")


def show_forgot_password_page(auth):
    """Display forgot password page"""
    st.markdown("### 🔑 Reset Password")
    
    if 'reset_email' not in st.session_state:
        # Step 1: Request reset code
        with st.form("forgot_password_form"):
            email = st.text_input("Email", placeholder="your@email.com")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Send Reset Code", use_container_width=True)
            with col2:
                if st.form_submit_button("Back to Login", use_container_width=True):
                    st.session_state.auth_page = 'login'
                    st.rerun()
            
            if submit:
                if email:
                    with st.spinner("Sending reset code..."):
                        result = auth.forgot_password(email)
                    
                    if result['success']:
                        st.success(result['message'])
                        st.session_state.reset_email = email
                        st.rerun()
                    else:
                        st.error(result['message'])
                else:
                    st.error("Please enter your email")
    else:
        # Step 2: Reset password with code
        st.info(f"Reset code sent to {st.session_state.reset_email}")
        
        with st.form("reset_password_form"):
            code = st.text_input("Reset Code", placeholder="123456")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Reset Password", use_container_width=True)
            with col2:
                if st.form_submit_button("Cancel", use_container_width=True):
                    del st.session_state.reset_email
                    st.session_state.auth_page = 'login'
                    st.rerun()
            
            if submit:
                if not all([code, new_password, confirm_password]):
                    st.error("Please fill in all fields")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    with st.spinner("Resetting password..."):
                        result = auth.confirm_forgot_password(
                            st.session_state.reset_email, code, new_password
                        )
                    
                    if result['success']:
                        st.success(result['message'])
                        del st.session_state.reset_email
                        st.session_state.auth_page = 'login'
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(result['message'])


def require_authentication():
    """Decorator to require authentication for pages"""
    init_session_state()
    
    # Demo mode - skip authentication
    if os.getenv('DEMO_MODE', 'true').lower() == 'true':
        if not st.session_state.authenticated:
            st.session_state.authenticated = True
            st.session_state.user_email = "demo@umrahtrip.com"
            st.session_state.user_name = "Demo User"
        return True
    
    # Production mode - require Cognito auth
    if not st.session_state.authenticated:
        auth = CognitoAuth()
        
        st.markdown('<h1 class="main-header">🕋 Umrah Trip Creator</h1>', 
                   unsafe_allow_html=True)
        st.markdown("### Welcome! Please sign in to continue")
        
        # Show appropriate auth page
        if st.session_state.auth_page == 'login':
            show_login_page(auth)
        elif st.session_state.auth_page == 'signup':
            show_signup_page(auth)
        elif st.session_state.auth_page == 'verify':
            show_verify_page(auth)
        elif st.session_state.auth_page == 'forgot_password':
            show_forgot_password_page(auth)
        
        return False
    
    return True


def show_user_menu():
    """Display user menu in sidebar"""
    if st.session_state.authenticated:
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"👤 **{st.session_state.user_name}**")
            st.markdown(f"📧 {st.session_state.user_email}")
            
            if st.button("🚪 Sign Out", use_container_width=True):
                # Sign out
                if os.getenv('DEMO_MODE', 'true').lower() != 'true':
                    auth = CognitoAuth()
                    auth.sign_out(st.session_state.access_token)
                
                # Clear session
                st.session_state.authenticated = False
                st.session_state.user_email = None
                st.session_state.user_name = None
                st.session_state.access_token = None
                st.session_state.refresh_token = None
                st.session_state.step = 1
                st.session_state.user_data = {}
                
                st.rerun()
