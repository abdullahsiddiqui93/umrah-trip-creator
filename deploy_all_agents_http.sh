#!/bin/bash
# Deploy all agents with HTTP protocol

set -e

echo "=========================================="
echo "Deploying All Umrah Trip Agents (HTTP)"
echo "=========================================="

agents=(
    "flight_agent:umrah_flight_agent:flight_runtime.py"
    "hotel_agent:umrah_hotel_agent:hotel_runtime.py"
    "visa_agent:umrah_visa_agent:visa_runtime.py"
    "itinerary_agent:umrah_itinerary_agent:itinerary_runtime.py"
)

for agent_info in "${agents[@]}"; do
    IFS=':' read -r dir name entrypoint <<< "$agent_info"
    
    echo ""
    echo "=========================================="
    echo "Deploying $name..."
    echo "=========================================="
    
    cd "agents/$dir"
    
    # Configure agent with HTTP protocol
    agentcore configure \
        --entrypoint "$entrypoint" \
        --name "$name" \
        --deployment-type direct_code_deploy \
        --runtime PYTHON_3_12 \
        --requirements-file requirements.txt \
        --protocol HTTP \
        --non-interactive
    
    # Deploy agent
    agentcore deploy --agent "$name"
    
    cd ../..
    
    echo "✅ $name deployed successfully!"
done

echo ""
echo "=========================================="
echo "✅ All Agents Deployed Successfully!"
echo "=========================================="
echo ""
echo "Deployed agents:"
echo "  - umrah_orchestrator (already deployed)"
echo "  - umrah_flight_agent"
echo "  - umrah_hotel_agent"
echo "  - umrah_visa_agent"
echo "  - umrah_itinerary_agent"
echo ""
echo "Test with: agentcore invoke '{\"prompt\": \"Hello\"}' --agent <agent_name>"
