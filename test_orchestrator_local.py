#!/usr/bin/env python3
"""Test orchestrator agent locally"""

import os
os.environ["ORCHESTRATOR_MODEL"] = "anthropic.claude-3-5-sonnet-20241022-v2:0"

from strands import Agent

# Create orchestrator agent
orchestrator = Agent(
    model=os.getenv("ORCHESTRATOR_MODEL"),
    system_prompt="""You are the main Umrah Trip Coordinator. Be helpful and concise."""
)

# Test invocation
print("Testing orchestrator agent...")
try:
    response = orchestrator("Hello, I want to plan an Umrah trip")
    print(f"\nSuccess! Response:\n{response.message['content'][0]['text']}")
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
