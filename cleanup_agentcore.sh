#!/bin/bash

# Umrah Trip Creator - AgentCore Cleanup Script
# This script removes all deployed resources from AWS AgentCore

set -e  # Exit on error

echo "=========================================="
echo "Umrah Trip Creator - AgentCore Cleanup"
echo "=========================================="

# Load environment variables if .env exists
if [ -f .env ]; then
    source .env
fi

echo ""
echo "⚠️  WARNING: This will delete all deployed resources!"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo "=========================================="
echo "Step 1: Destroying Agents"
echo "=========================================="

# Function to destroy an agent
destroy_agent() {
    local agent_name=$1
    
    echo ""
    echo "Destroying $agent_name..."
    agentcore destroy --agent "$agent_name" --force || echo "⚠️  Agent $agent_name not found or already deleted"
}

# Destroy all agents
destroy_agent "umrah-orchestrator"
destroy_agent "umrah-flight-agent"
destroy_agent "umrah-hotel-agent"
destroy_agent "umrah-visa-agent"
destroy_agent "umrah-itinerary-agent"

echo ""
echo "=========================================="
echo "Step 2: Deleting Gateway"
echo "=========================================="

if [ ! -z "$GATEWAY_ID" ]; then
    echo ""
    echo "Deleting gateway: $GATEWAY_ID"
    agentcore gateway delete-mcp-gateway --id "$GATEWAY_ID" --force || echo "⚠️  Gateway not found or already deleted"
else
    echo "⚠️  Gateway ID not found in .env file"
    echo "   You can manually delete gateways with:"
    echo "   agentcore gateway list-mcp-gateways"
    echo "   agentcore gateway delete-mcp-gateway --name <gateway-name> --force"
fi

echo ""
echo "=========================================="
echo "Step 3: Deleting Memory Resources"
echo "=========================================="

if [ ! -z "$MEMORY_STM_ID" ] || [ ! -z "$MEMORY_LTM_ID" ]; then
    echo ""
    echo "Deleting memory resources..."
    
    python3 << EOF
from bedrock_agentcore.memory import MemoryClient
import os

client = MemoryClient(region_name='us-west-2')

stm_id = os.getenv('MEMORY_STM_ID')
ltm_id = os.getenv('MEMORY_LTM_ID')

if stm_id:
    try:
        client.delete_memory(memory_id=stm_id)
        print(f"✅ Deleted STM memory: {stm_id}")
    except Exception as e:
        print(f"⚠️  Could not delete STM memory: {e}")

if ltm_id:
    try:
        client.delete_memory(memory_id=ltm_id)
        print(f"✅ Deleted LTM memory: {ltm_id}")
    except Exception as e:
        print(f"⚠️  Could not delete LTM memory: {e}")
EOF
else
    echo "⚠️  Memory IDs not found in .env file"
    echo "   You can manually delete memory resources with:"
    echo "   python -c \"from bedrock_agentcore.memory import MemoryClient; client = MemoryClient(region_name='us-west-2'); client.delete_memory(memory_id='<memory-id>')\""
fi

echo ""
echo "=========================================="
echo "Step 4: Cleaning Up Local Files"
echo "=========================================="

echo ""
echo "Removing generated configuration files..."
rm -f gateway_config.json
rm -f .bedrock_agentcore.yaml
echo "✅ Local files cleaned up"

echo ""
echo "=========================================="
echo "✅ Cleanup Complete!"
echo "=========================================="

echo ""
echo "All AgentCore resources have been removed."
echo ""
echo "Note: The following may still exist and require manual cleanup:"
echo "  - CloudWatch log groups (/aws/bedrock-agentcore/*)"
echo "  - IAM roles created by AgentCore"
echo "  - Cognito User Pools created by Gateway"
echo "  - S3 buckets (if frontend was deployed)"
echo ""
echo "To remove CloudWatch logs:"
echo "  aws logs delete-log-group --log-group-name /aws/bedrock-agentcore/umrah-orchestrator"
echo "  (repeat for each agent)"
echo ""
