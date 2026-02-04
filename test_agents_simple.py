#!/usr/bin/env python3
"""
Simple test to invoke agents directly and see their responses
"""

import boto3
import json
import time

# Initialize boto3 client
client = boto3.client('bedrock-agentcore', region_name='us-west-2')

# Agent ARNs
AGENTS = {
    'flight': 'arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_flight_agent-ufM0XiC3fw',
    'hotel': 'arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_hotel_agent-P3Am0WF25G',
    'orchestrator': 'arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo'
}


def test_agent(agent_name, prompt, timeout=60):
    """Test a single agent"""
    print(f"\n{'='*60}")
    print(f"Testing {agent_name.upper()} Agent")
    print(f"{'='*60}")
    print(f"Prompt: {prompt}")
    print(f"\nInvoking agent...")
    
    agent_arn = AGENTS[agent_name]
    # Session ID must be at least 33 characters
    import uuid
    session_id = str(uuid.uuid4())  # This generates a 36-character UUID
    
    try:
        start_time = time.time()
        
        payload = json.dumps({"prompt": prompt}).encode()
        
        response = client.invoke_agent_runtime(
            agentRuntimeArn=agent_arn,
            runtimeSessionId=session_id,
            payload=payload
        )
        
        # Process response
        content_type = response.get("contentType", "")
        
        if "text/event-stream" in content_type:
            # Handle streaming response
            content = []
            for line in response["response"].iter_lines(chunk_size=10):
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        line = line[6:]
                        content.append(line)
            
            result = "\n".join(content) if content else "No content"
        elif content_type == "application/json":
            # Handle JSON response
            content = []
            for chunk in response.get("response", []):
                content.append(chunk.decode('utf-8'))
            result = ''.join(content)
        else:
            result = str(response)
        
        elapsed = time.time() - start_time
        
        print(f"\n✅ Success! (took {elapsed:.1f}s)")
        print(f"\nResponse:")
        print("-" * 60)
        print(result[:500])  # First 500 chars
        if len(result) > 500:
            print(f"\n... (truncated, total length: {len(result)} chars)")
        print("-" * 60)
        
        return True, result
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ Failed! (after {elapsed:.1f}s)")
        print(f"Error: {str(e)}")
        return False, str(e)


def main():
    """Run agent tests"""
    print("="*60)
    print("AGENT TESTING SUITE")
    print("="*60)
    
    results = {}
    
    # Test 1: Flight Agent
    success, response = test_agent(
        'flight',
        'Find 2-3 flight options from JFK to JED departing March 15, 2026 returning March 25, 2026 for 2 adults'
    )
    results['flight'] = success
    
    # Test 2: Hotel Agent
    success, response = test_agent(
        'hotel',
        'Find 2-3 hotel options in Makkah near Haram for March 15-20, 2026 for 2 adults, prefer 4-5 star'
    )
    results['hotel'] = success
    
    # Test 3: Orchestrator (this will take longer)
    print("\n⚠️  Note: Orchestrator test may take 2-3 minutes...")
    success, response = test_agent(
        'orchestrator',
        'Plan an Umrah trip from New York to Jeddah, March 15-25, 2026, 2 adults, budget $6000. Provide multiple flight and hotel options.'
    )
    results['orchestrator'] = success
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    for agent, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{agent.capitalize():15} {status}")
    print(f"{'='*60}")
    
    if all(results.values()):
        print("\n✅ All agents working correctly!")
    else:
        print("\n⚠️  Some agents failed. Check errors above.")


if __name__ == "__main__":
    main()
