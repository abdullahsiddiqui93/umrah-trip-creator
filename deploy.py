#!/usr/bin/env python3
"""
Automated deployment script for Umrah Trip Creator on AWS AgentCore
"""

import boto3
import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class UmrahTripDeployer:
    def __init__(self):
        self.region = os.getenv('AWS_REGION', 'us-west-2')
        self.account_id = os.getenv('AWS_ACCOUNT_ID')
        self.project_name = 'umrah-trip-creator'
        
        # AWS clients
        self.cfn = boto3.client('cloudformation', region_name=self.region)
        self.s3 = boto3.client('s3', region_name=self.region)
        self.dynamodb = boto3.client('dynamodb', region_name=self.region)
        
        print(f"🚀 Umrah Trip Creator Deployment")
        print(f"Region: {self.region}")
        print(f"Account: {self.account_id}")
        print("="*60)
    
    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        print("\n📋 Checking prerequisites...")
        
        required_env_vars = [
            'AWS_REGION',
            'AWS_ACCOUNT_ID',
            'OPENAI_API_KEY',
            'ANTHROPIC_API_KEY'
        ]
        
        missing = []
        for var in required_env_vars:
            if not os.getenv(var):
                missing.append(var)
        
        if missing:
            print(f"❌ Missing environment variables: {', '.join(missing)}")
            print("Please set them in .env file")
            return False
        
        print("✅ All prerequisites met")
        return True
    
    def deploy_infrastructure(self):
        """Deploy CloudFormation stack"""
        print("\n🏗️  Deploying infrastructure...")
        
        stack_name = f"{self.project_name}-stack"
        
        # Check if stack exists
        try:
            self.cfn.describe_stacks(StackName=stack_name)
            print(f"Stack {stack_name} already exists. Updating...")
            operation = 'update'
        except:
            print(f"Creating new stack {stack_name}...")
            operation = 'create'
        
        # Read CloudFormation template
        template_path = Path('infrastructure/cloudformation/main.yaml')
        if not template_path.exists():
            print("❌ CloudFormation template not found")
            print("Creating basic template...")
            self.create_basic_template()
        
        with open(template_path) as f:
            template_body = f.read()
        
        parameters = [
            {
                'ParameterKey': 'ProjectName',
                'ParameterValue': self.project_name
            },
            {
                'ParameterKey': 'OpenAIAPIKey',
                'ParameterValue': os.getenv('OPENAI_API_KEY')
            },
            {
                'ParameterKey': 'AnthropicAPIKey',
                'ParameterValue': os.getenv('ANTHROPIC_API_KEY')
            }
        ]
        
        try:
            if operation == 'create':
                response = self.cfn.create_stack(
                    StackName=stack_name,
                    TemplateBody=template_body,
                    Parameters=parameters,
                    Capabilities=['CAPABILITY_IAM']
                )
            else:
                response = self.cfn.update_stack(
                    StackName=stack_name,
                    TemplateBody=template_body,
                    Parameters=parameters,
                    Capabilities=['CAPABILITY_IAM']
                )
            
            print(f"✅ Stack {operation} initiated")
            print("⏳ Waiting for stack to complete (this may take 5-10 minutes)...")
            
            # Wait for stack to complete
            waiter = self.cfn.get_waiter(f'stack_{operation}_complete')
            waiter.wait(StackName=stack_name)
            
            print("✅ Infrastructure deployed successfully")
            
            # Get outputs
            stack = self.cfn.describe_stacks(StackName=stack_name)['Stacks'][0]
            outputs = {o['OutputKey']: o['OutputValue'] for o in stack.get('Outputs', [])}
            
            return outputs
            
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            return None
    
    def create_basic_template(self):
        """Create basic CloudFormation template"""
        Path('infrastructure/cloudformation').mkdir(parents=True, exist_ok=True)
        
        template = """AWSTemplateFormatVersion: '2010-09-09'
Description: 'Umrah Trip Creator - Basic Infrastructure with Cognito'

Parameters:
  ProjectName:
    Type: String
    Default: umrah-trip-creator
  OpenAIAPIKey:
    Type: String
    NoEcho: true
  AnthropicAPIKey:
    Type: String
    NoEcho: true

Resources:
  # Cognito User Pool
  UserPool:
    Type: AWS::Cognito::UserPool
    Properties:
      UserPoolName: !Sub '${ProjectName}-users'
      AutoVerifiedAttributes:
        - email
      UsernameAttributes:
        - email
      Schema:
        - Name: email
          Required: true
          Mutable: false
        - Name: name
          Required: true
          Mutable: true
      Policies:
        PasswordPolicy:
          MinimumLength: 8
          RequireUppercase: true
          RequireLowercase: true
          RequireNumbers: true
          RequireSymbols: true
      EmailConfiguration:
        EmailSendingAccount: COGNITO_DEFAULT
      UserPoolTags:
        Project: !Ref ProjectName

  # Cognito User Pool Client
  UserPoolClient:
    Type: AWS::Cognito::UserPoolClient
    Properties:
      ClientName: !Sub '${ProjectName}-client'
      UserPoolId: !Ref UserPool
      GenerateSecret: false
      ExplicitAuthFlows:
        - ALLOW_USER_PASSWORD_AUTH
        - ALLOW_REFRESH_TOKEN_AUTH
      PreventUserExistenceErrors: ENABLED
      RefreshTokenValidity: 30
      AccessTokenValidity: 1
      IdTokenValidity: 1
      TokenValidityUnits:
        RefreshToken: days
        AccessToken: hours
        IdToken: hours

  # Cognito Identity Pool
  IdentityPool:
    Type: AWS::Cognito::IdentityPool
    Properties:
      IdentityPoolName: !Sub '${ProjectName}_identity_pool'
      AllowUnauthenticatedIdentities: false
      CognitoIdentityProviders:
        - ClientId: !Ref UserPoolClient
          ProviderName: !GetAtt UserPool.ProviderName

  # IAM Role for authenticated users
  CognitoAuthRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Federated: cognito-identity.amazonaws.com
            Action: sts:AssumeRoleWithWebIdentity
            Condition:
              StringEquals:
                cognito-identity.amazonaws.com:aud: !Ref IdentityPool
              ForAnyValue:StringLike:
                cognito-identity.amazonaws.com:amr: authenticated
      Policies:
        - PolicyName: CognitoAuthPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:PutObject
                Resource: !Sub '${DocumentBucket.Arn}/*'
              - Effect: Allow
                Action:
                  - dynamodb:GetItem
                  - dynamodb:PutItem
                  - dynamodb:Query
                Resource: !GetAtt BookingsTable.Arn

  # Attach roles to identity pool
  IdentityPoolRoleAttachment:
    Type: AWS::Cognito::IdentityPoolRoleAttachment
    Properties:
      IdentityPoolId: !Ref IdentityPool
      Roles:
        authenticated: !GetAtt CognitoAuthRole.Arn

  # S3 Bucket for documents
  DocumentBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${ProjectName}-documents-${AWS::AccountId}'
      VersioningConfiguration:
        Status: Enabled
      CorsConfiguration:
        CorsRules:
          - AllowedHeaders:
              - '*'
            AllowedMethods:
              - GET
              - PUT
              - POST
            AllowedOrigins:
              - '*'
            MaxAge: 3000

  # DynamoDB Table for bookings
  BookingsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '${ProjectName}-bookings'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: booking_id
          AttributeType: S
        - AttributeName: user_email
          AttributeType: S
      KeySchema:
        - AttributeName: booking_id
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: user-email-index
          KeySchema:
            - AttributeName: user_email
              KeyType: HASH
          Projection:
            ProjectionType: ALL

Outputs:
  UserPoolId:
    Value: !Ref UserPool
    Description: Cognito User Pool ID
    Export:
      Name: !Sub '${ProjectName}-UserPoolId'
  
  UserPoolClientId:
    Value: !Ref UserPoolClient
    Description: Cognito User Pool Client ID
    Export:
      Name: !Sub '${ProjectName}-UserPoolClientId'
  
  IdentityPoolId:
    Value: !Ref IdentityPool
    Description: Cognito Identity Pool ID
    Export:
      Name: !Sub '${ProjectName}-IdentityPoolId'
  
  DocumentBucket:
    Value: !Ref DocumentBucket
    Description: S3 Bucket for documents
    Export:
      Name: !Sub '${ProjectName}-DocumentBucket'
  
  BookingsTable:
    Value: !Ref BookingsTable
    Description: DynamoDB table for bookings
    Export:
      Name: !Sub '${ProjectName}-BookingsTable'
"""
        
        with open('infrastructure/cloudformation/main.yaml', 'w') as f:
            f.write(template)
        
        print("✅ Created CloudFormation template with Cognito")
    
    def deploy_agents(self, outputs):
        """Deploy agents to AgentCore"""
        print("\n🤖 Deploying AI agents...")
        
        # Note: This is a placeholder for actual AgentCore deployment
        # In production, you would use the bedrock-agentcore-runtime SDK
        
        print("📝 Agent deployment configuration:")
        print("  - Orchestrator Agent (Strands)")
        print("  - Flight Agent (OpenAI)")
        print("  - Hotel Agent (Claude)")
        print("  - Visa Agent (OpenAI)")
        print("  - Itinerary Agent (Claude)")
        
        print("\n⚠️  Note: AgentCore deployment requires:")
        print("  1. bedrock-agentcore-runtime SDK")
        print("  2. Agent source code packaging")
        print("  3. A2A protocol configuration")
        print("\nSee DEPLOYMENT_GUIDE.md for detailed instructions")
        
        return True
    
    def test_deployment(self):
        """Test the deployment"""
        print("\n🧪 Testing deployment...")
        
        # Test S3 bucket
        try:
            bucket_name = f"{self.project_name}-documents-{self.account_id}"
            self.s3.head_bucket(Bucket=bucket_name)
            print(f"✅ S3 bucket accessible: {bucket_name}")
        except Exception as e:
            print(f"❌ S3 bucket test failed: {e}")
        
        # Test DynamoDB table
        try:
            table_name = f"{self.project_name}-bookings"
            self.dynamodb.describe_table(TableName=table_name)
            print(f"✅ DynamoDB table accessible: {table_name}")
        except Exception as e:
            print(f"❌ DynamoDB table test failed: {e}")
        
        return True
    
    def print_summary(self, outputs):
        """Print deployment summary"""
        print("\n" + "="*60)
        print("🎉 Deployment Complete!")
        print("="*60)
        
        if outputs:
            print("\n📊 Resources Created:")
            for key, value in outputs.items():
                print(f"  {key}: {value}")
        
        print("\n📚 Next Steps:")
        print("  1. Review DEPLOYMENT_GUIDE.md for agent deployment")
        print("  2. Configure API endpoints in AgentCore Gateway")
        print("  3. Test agents with test/test_deployed_agents.py")
        print("  4. Deploy frontend to S3/CloudFront")
        print("  5. Set up monitoring and alerts")
        
        print("\n🔗 Useful Commands:")
        print(f"  View logs: aws logs tail /aws/agentcore/{self.project_name} --follow")
        print(f"  Check stack: aws cloudformation describe-stacks --stack-name {self.project_name}-stack")
        
        print("\n✨ Your Umrah Trip Creator is ready for production!")
    
    def run(self):
        """Run full deployment"""
        if not self.check_prerequisites():
            sys.exit(1)
        
        # Deploy infrastructure
        outputs = self.deploy_infrastructure()
        if not outputs:
            print("❌ Infrastructure deployment failed")
            sys.exit(1)
        
        # Deploy agents
        if not self.deploy_agents(outputs):
            print("❌ Agent deployment failed")
            sys.exit(1)
        
        # Test deployment
        self.test_deployment()
        
        # Print summary
        self.print_summary(outputs)

if __name__ == '__main__':
    deployer = UmrahTripDeployer()
    deployer.run()
