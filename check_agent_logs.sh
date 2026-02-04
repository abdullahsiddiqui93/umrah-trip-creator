#!/bin/bash

echo "==================================="
echo "Checking Agent Logs for Errors"
echo "==================================="

echo ""
echo "1. Flight Agent Logs (last 50 lines):"
echo "-----------------------------------"
aws logs tail /aws/bedrock-agentcore/runtimes/umrah_flight_agent-ufM0XiC3fw-DEFAULT \
  --log-stream-name-prefix "2026/02/03/[runtime-logs" \
  --since 30m \
  --format short | tail -50

echo ""
echo "2. Hotel Agent Logs (last 50 lines):"
echo "-----------------------------------"
aws logs tail /aws/bedrock-agentcore/runtimes/umrah_hotel_agent-P3Am0WF25G-DEFAULT \
  --log-stream-name-prefix "2026/02/03/[runtime-logs" \
  --since 30m \
  --format short | tail -50

echo ""
echo "3. Orchestrator Logs (last 50 lines):"
echo "-----------------------------------"
aws logs tail /aws/bedrock-agentcore/runtimes/umrah_orchestrator-DFFg1bHZKo-DEFAULT \
  --log-stream-name-prefix "2026/02/03/[runtime-logs" \
  --since 30m \
  --format short | tail -50

echo ""
echo "==================================="
echo "Log check complete"
echo "==================================="
