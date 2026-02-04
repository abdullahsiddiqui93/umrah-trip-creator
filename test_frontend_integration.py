#!/usr/bin/env python3
"""
Test script to verify frontend integration with AgentCore agents
Run this to ensure everything is working before launching the Streamlit app
"""

import sys
from pathlib import Path

# Add frontend to path
sys.path.append(str(Path(__file__).parent))

from frontend.agentcore_client import get_agentcore_client

def test_agent(agent_type, prompt):
    """Test a single agent"""
    print(f"\n{'='*60}")
    print(f"Testing {agent_type.upper()} Agent")
    print(f"{'='*60}")
    print(f"Prompt: {prompt}")
    print(f"\nInvoking agent...")
    
    try:
        client = get_agentcore_client()
        response = client.invoke_agent(agent_type, prompt)
        
        if 'error' in response:
            print(f"❌ Error: {response['error']}")
            return False
        else:
            result = client.extract_text_from_response(response)
            print(f"\n✅ Success! Response:\n{result[:500]}...")
            return True
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_orchestrator_with_requirements():
    """Test orchestrator with full requirements"""
    print(f"\n{'='*60}")
    print(f"Testing ORCHESTRATOR with Full Requirements")
    print(f"{'='*60}")
    
    try:
        client = get_agentcore_client()
        
        requirements = {
            'travel_dates': {
                'departure_airport': 'New York (JFK)',
                'departure': '2026-03-15',
                'return': '2026-03-22',
                'duration': 7,
                'arrival_city': 'Jeddah (JED)'
            },
            'travelers': [
                {'name': 'Test User', 'nationality': 'United States', 'age': 35}
            ],
            'budget': {
                'total': 5000,
                'per_person': 5000,
                'currency': 'USD',
                'flexibility': 'Moderate'
            },
            'hotel_preferences': {
                'makkah': {'star_rating': 5, 'proximity': 'Walking Distance (<500m)'},
                'madinah': {'star_rating': 4, 'proximity': 'Close (500m-1km)'}
            },
            'flight_preferences': {
                'cabin_class': 'Economy',
                'direct_flights': True
            },
            'special_requirements': {
                'first_time_umrah': True
            }
        }
        
        print("Invoking orchestrator with full requirements...")
        response = client.invoke_orchestrator(requirements)
        
        if 'error' in response:
            print(f"❌ Error: {response['error']}")
            return False
        else:
            result = client.extract_text_from_response(response)
            print(f"\n✅ Success! Response:\n{result[:500]}...")
            return True
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("UMRAH TRIP CREATOR - FRONTEND INTEGRATION TEST")
    print("="*60)
    print("\nThis script tests the connection between the frontend")
    print("and deployed AgentCore agents.")
    print("\nMake sure:")
    print("  1. AWS credentials are configured")
    print("  2. All agents are deployed and running")
    print("  3. You're in the project root directory")
    print("\n" + "="*60)
    
    input("\nPress Enter to start tests...")
    
    results = {}
    
    # Test each agent
    tests = [
        ('orchestrator', 'Hello, I want to plan an Umrah trip'),
        ('flight', 'Find me flights from New York to Jeddah for 2 passengers'),
        ('hotel', 'Find hotels in Makkah near Masjid al-Haram'),
        ('visa', 'What are the Umrah visa requirements for US citizens?'),
        ('itinerary', 'Create a 7-day Umrah itinerary')
    ]
    
    for agent_type, prompt in tests:
        results[agent_type] = test_agent(agent_type, prompt)
    
    # Test orchestrator with full requirements
    results['orchestrator_full'] = test_orchestrator_with_requirements()
    
    # Summary
    print(f"\n\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20s}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Frontend is ready to use.")
        print("\nNext steps:")
        print("  1. Run: streamlit run frontend/streamlit_app.py")
        print("  2. Open: http://localhost:8501")
        print("  3. Start planning Umrah trips!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        print("\nTroubleshooting:")
        print("  1. Verify AWS credentials: aws sts get-caller-identity")
        print("  2. Check agent status: agentcore status --agent umrah_orchestrator")
        print("  3. View logs: aws logs tail /aws/bedrock-agentcore/runtimes/...")
    
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
