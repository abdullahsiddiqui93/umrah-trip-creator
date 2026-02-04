#!/bin/bash

# Redeploy Flight and Hotel Agents with Real API Integration

echo "=========================================="
echo "Redeploying Agents with Real API Tools"
echo "=========================================="
echo ""

# Activate virtual environment
source .venv/bin/activate

# Deploy Flight Agent
echo "📡 Deploying Flight Agent with Amadeus API..."
cd agents/flight_agent
agentcore deploy --agent umrah_flight_agent --auto-update-on-conflict
if [ $? -eq 0 ]; then
    echo "✅ Flight Agent deployed successfully!"
else
    echo "❌ Flight Agent deployment failed!"
    exit 1
fi
cd ../..
echo ""

# Deploy Hotel Agent
echo "🏨 Deploying Hotel Agent with RapidAPI..."
cd agents/hotel_agent
agentcore deploy --agent umrah_hotel_agent --auto-update-on-conflict
if [ $? -eq 0 ]; then
    echo "✅ Hotel Agent deployed successfully!"
else
    echo "❌ Hotel Agent deployment failed!"
    exit 1
fi
cd ../..
echo ""

echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "Both agents now have real API integration:"
echo "  - Flight Agent: Using Amadeus API for real flight data"
echo "  - Hotel Agent: Using RapidAPI (Booking.com) for real hotel data"
echo ""
echo "Test the agents:"
echo "  cd agents/flight_agent"
echo "  agentcore invoke '{\"prompt\": \"Find flights from New York to Medina\"}' --agent umrah_flight_agent"
echo ""
