#!/bin/bash

# Umrah Website Deployment Script for AWS Amplify

set -e

echo "🚀 Deploying Umrah Website to AWS Amplify"
echo "=========================================="

# Check if Amplify CLI is installed
if ! command -v amplify &> /dev/null; then
    echo "❌ Amplify CLI not found. Installing..."
    npm install -g @aws-amplify/cli
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
npm install

echo ""
echo "🔧 Amplify Setup"
echo "================"
echo ""
echo "If this is your first time, you'll need to:"
echo "1. Initialize Amplify: amplify init"
echo "2. Add hosting: amplify add hosting"
echo "3. Configure environment variables in Amplify Console"
echo ""

read -p "Have you initialized Amplify? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Please run: amplify init"
    echo "Then run this script again."
    exit 1
fi

# Build the application
echo ""
echo "🏗️  Building application..."
npm run build

# Deploy to Amplify
echo ""
echo "🚀 Deploying to AWS Amplify..."
amplify publish

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Go to AWS Amplify Console"
echo "2. Configure environment variables:"
echo "   - ORCHESTRATOR_ARN=arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo"
echo "   - AWS_REGION=us-west-2"
echo "3. Redeploy from Amplify Console"
echo "4. Your website will be live!"
echo ""
