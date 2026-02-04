#!/bin/bash

# Simple deployment script for all agents
set -e

echo "=========================================="
echo "Deploying All Umrah Trip Agents"
echo "=========================================="

# Load environment variables
source .env

# Array of agents to deploy
agents=(
    "orchestrator:umrah_orchestrator:orchestrator_runtime.py:--env MEMORY_LTM_ID=$MEMORY_LTM_ID --env GATEWAY_URL=$GATEWAY_URL --env GATEWAY_ACCESS_TOKEN=$GATEWAY_ACCESS_TOKEN"
    "flight_agent:umrah_flight_agent:flight_runtime.py:--env GATEWAY_URL=$GATEWAY_URL --env GATEWAY_ACCESS_TOKEN=$GATEWAY_ACCESS_TOKEN"
    "hotel_agent:umrah_hotel_agent:hotel_runtime.py:--env GATEWAY_URL=$GATEWAY_URL --env GATEWAY_ACCESS_TOKEN=$GATEWAY_ACCESS_TOKEN"
    "visa_agent:umrah_visa_agent:visa_runtime.py:--env GATEWAY_URL=$GATEWAY_URL --env GATEWAY_ACCESS_TOKEN=$GATEWAY_ACCESS_TOKEN"
    "itinerary_agent:umrah_itinerary_agent:itinerary_runtime.py:"
)

for agent_info in "${agents[@]}"; do
    IFS=':' read -r dir name entrypoint env_vars <<< "$agent_info"
    
    echo ""
    echo "=========================================="
    echo "Deploying $name..."
    echo "=========================================="
    
    cd "agents/$dir"
    
    # Configure agent
    agentcore configure \
        --entrypoint "$entrypoint" \
        --name "$name" \
        --deployment-type direct_code_deploy \
        --runtime PYTHON_3_12 \
        --requirements-file requirements.txt \
        --protocol A2A \
        --non-interactive
    
    # Deploy agent
    agentcore deploy \
        --agent "$name" \
        $env_vars \
        --auto-update-on-conflict
    
    cd ../..
    
    echo "✅ $name deployed successfully!"
done

echo ""
echo "=========================================="
echo "✅ All Agents Deployed Successfully!"
echo "=========================================="
echo ""
echo "Deployed agents:"
echo "  - umrah_orchestrator"
echo "  - umrah_flight_agent"
echo "  - umrah_hotel_agent"
echo "  - umrah_visa_agent"
echo "  - umrah_itinerary_agent"
echo ""
echo "Test with: agentcore invoke '{\"prompt\": \"Hello\"}' --agent umrah_orchestrator"
