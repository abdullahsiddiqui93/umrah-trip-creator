#!/bin/bash

# Umrah Trip Creator - AgentCore Deployment Script
# This script automates the deployment of all agents to AWS AgentCore

set -e  # Exit on error

echo "=========================================="
echo "Umrah Trip Creator - AgentCore Deployment"
echo "=========================================="

# Check prerequisites
echo ""
echo "Checking prerequisites..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first."
    exit 1
fi
echo "✅ AWS CLI found"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install it first."
    exit 1
fi
echo "✅ Python 3 found"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi
echo "✅ .env file found"

# Load environment variables
source .env

# Check required environment variables
if [ -z "$AWS_REGION" ]; then
    echo "❌ Missing required environment variable: AWS_REGION"
    exit 1
fi
echo "✅ Environment variables configured"

# Check if agentcore CLI is installed
if ! command -v agentcore &> /dev/null; then
    echo ""
    echo "AgentCore CLI not found. Installing..."
    pip3 install bedrock-agentcore-starter-toolkit bedrock-agentcore strands-agents
fi
echo "✅ AgentCore CLI ready"

echo ""
echo "=========================================="
echo "Step 1: Setting up AgentCore Memory"
echo "=========================================="

if [ -z "$MEMORY_LTM_ID" ]; then
    echo "Memory not configured. Running setup_memory.py..."
    python3 setup_memory.py
    echo ""
    echo "⚠️  Please add the memory IDs to your .env file and run this script again."
    exit 0
else
    echo "✅ Memory already configured: $MEMORY_LTM_ID"
fi

echo ""
echo "=========================================="
echo "Step 2: Setting up AgentCore Gateway"
echo "=========================================="

if [ -z "$GATEWAY_URL" ]; then
    echo "Gateway not configured. Running setup_gateway.py..."
    python3 setup_gateway.py
    echo ""
    echo "⚠️  Please add the gateway configuration to your .env file and run this script again."
    exit 0
else
    echo "✅ Gateway already configured: $GATEWAY_URL"
fi

echo ""
echo "=========================================="
echo "Step 3: Deploying Agents to AgentCore Runtime"
echo "=========================================="

# Function to deploy an agent
deploy_agent() {
    local agent_dir=$1
    local agent_name=$2
    local entrypoint=$3
    local protocol=$4
    local env_vars=$5
    
    echo ""
    echo "Deploying $agent_name..."
    cd "$agent_dir"
    
    # Configure agent with direct_code_deploy (no Docker/ECR needed)
    agentcore configure \
        --create \
        --entrypoint "$entrypoint" \
        --name "$agent_name" \
        --runtime PYTHON_3_12 \
        --deployment-type direct_code_deploy \
        --requirements-file requirements.txt \
        --protocol "$protocol" \
        --non-interactive
    
    # Deploy agent with environment variables
    agentcore deploy \
        --agent "$agent_name" \
        $env_vars \
        --auto-update-on-conflict
    
    echo "✅ $agent_name deployed successfully"
    cd - > /dev/null
}

# Deploy Orchestrator Agent
deploy_agent \
    "agents/orchestrator" \
    "umrah_orchestrator" \
    "orchestrator_runtime.py" \
    "A2A" \
    "--env MEMORY_LTM_ID=$MEMORY_LTM_ID --env GATEWAY_URL=$GATEWAY_URL --env GATEWAY_ACCESS_TOKEN=$GATEWAY_ACCESS_TOKEN"

# Deploy Flight Agent
deploy_agent \
    "agents/flight_agent" \
    "umrah_flight_agent" \
    "flight_runtime.py" \
    "A2A" \
    "--env GATEWAY_URL=$GATEWAY_URL --env GATEWAY_ACCESS_TOKEN=$GATEWAY_ACCESS_TOKEN"

# Deploy Hotel Agent
deploy_agent \
    "agents/hotel_agent" \
    "umrah_hotel_agent" \
    "hotel_runtime.py" \
    "A2A" \
    "--env GATEWAY_URL=$GATEWAY_URL --env GATEWAY_ACCESS_TOKEN=$GATEWAY_ACCESS_TOKEN"

# Deploy Visa Agent
deploy_agent \
    "agents/visa_agent" \
    "umrah_visa_agent" \
    "visa_runtime.py" \
    "A2A" \
    "--env GATEWAY_URL=$GATEWAY_URL --env GATEWAY_ACCESS_TOKEN=$GATEWAY_ACCESS_TOKEN"

# Deploy Itinerary Agent
deploy_agent \
    "agents/itinerary_agent" \
    "umrah_itinerary_agent" \
    "itinerary_runtime.py" \
    "A2A" \
    ""

echo ""
echo "=========================================="
echo "Step 4: Testing Deployment"
echo "=========================================="

echo ""
echo "Testing orchestrator agent..."
agentcore invoke '{"prompt": "Hello, I want to plan an Umrah trip"}' \
    --agent umrah_orchestrator

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="

echo ""
echo "Your Umrah Trip Creator is now deployed to AWS AgentCore!"
echo ""
echo "Deployed agents:"
echo "  - umrah_orchestrator (main coordinator)"
echo "  - umrah_flight_agent (flight search)"
echo "  - umrah_hotel_agent (hotel search)"
echo "  - umrah_visa_agent (visa requirements)"
echo "  - umrah_itinerary_agent (trip planning)"
echo ""
echo "Next steps:"
echo "  1. Test agents: agentcore invoke '{\"prompt\": \"...\"}' --agent <agent-name>"
echo "  2. Check status: agentcore status --agent <agent-name> --verbose"
echo "  3. View logs: aws logs tail /aws/bedrock-agentcore/<agent-name> --follow"
echo "  4. Update frontend to use deployed agents"
echo ""
echo "To clean up: ./cleanup_agentcore.sh"
echo ""
