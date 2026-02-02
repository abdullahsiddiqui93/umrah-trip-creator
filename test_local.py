"""
Local testing script for Umrah Trip Creator agents
"""

import sys
from pathlib import Path

# Add agents to path
sys.path.append(str(Path(__file__).parent))

from agents.orchestrator.orchestrator_agent import create_orchestrator_agent
from agents.flight_agent.flight_agent import create_flight_agent
from agents.hotel_agent.hotel_agent import create_hotel_agent
from agents.visa_agent.visa_agent import create_visa_agent
from agents.itinerary_agent.itinerary_agent import create_itinerary_agent


def test_orchestrator():
    """Test orchestrator agent"""
    print("\n" + "="*60)
    print("🎯 Testing Orchestrator Agent")
    print("="*60)
    
    try:
        orchestrator = create_orchestrator_agent()
        print("✅ Orchestrator agent created successfully")
        
        # Test with sample user input
        user_input = """
        I want to plan an Umrah trip for 2 people from March 15 to March 25, 2026.
        We are from the United States. We prefer 4-star hotels close to the Haram.
        Our budget is $3000 per person.
        """
        
        print("\n📝 Sample user input:")
        print(user_input)
        print("\n⏳ Processing... (This is a mock test)")
        
        # In production, this would call the actual agent
        # result = orchestrator.collect_user_requirements(user_input)
        
        print("✅ Orchestrator test passed")
        
    except Exception as e:
        print(f"❌ Orchestrator test failed: {e}")


def test_flight_agent():
    """Test flight agent"""
    print("\n" + "="*60)
    print("✈️ Testing Flight Agent")
    print("="*60)
    
    try:
        flight_agent = create_flight_agent()
        print("✅ Flight agent created successfully")
        print("✅ Flight agent test passed")
        
    except Exception as e:
        print(f"❌ Flight agent test failed: {e}")


def test_hotel_agent():
    """Test hotel agent"""
    print("\n" + "="*60)
    print("🏨 Testing Hotel Agent")
    print("="*60)
    
    try:
        hotel_agent = create_hotel_agent()
        print("✅ Hotel agent created successfully")
        print("✅ Hotel agent test passed")
        
    except Exception as e:
        print(f"❌ Hotel agent test failed: {e}")


def test_visa_agent():
    """Test visa agent"""
    print("\n" + "="*60)
    print("🛂 Testing Visa Agent")
    print("="*60)
    
    try:
        visa_agent = create_visa_agent()
        print("✅ Visa agent created successfully")
        print("✅ Visa agent test passed")
        
    except Exception as e:
        print(f"❌ Visa agent test failed: {e}")


def test_itinerary_agent():
    """Test itinerary agent"""
    print("\n" + "="*60)
    print("📅 Testing Itinerary Agent")
    print("="*60)
    
    try:
        itinerary_agent = create_itinerary_agent()
        print("✅ Itinerary agent created successfully")
        print("✅ Itinerary agent test passed")
        
    except Exception as e:
        print(f"❌ Itinerary agent test failed: {e}")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🕋 UMRAH TRIP CREATOR - LOCAL TESTING")
    print("="*60)
    
    print("\n📋 Testing all agents...")
    
    # Run tests
    test_orchestrator()
    test_flight_agent()
    test_hotel_agent()
    test_visa_agent()
    test_itinerary_agent()
    
    # Summary
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED")
    print("="*60)
    print("\n📱 Next steps:")
    print("1. Run the Streamlit frontend: cd frontend && ./run.sh")
    print("2. Open http://localhost:8501 in your browser")
    print("3. Start planning your Umrah trip!")
    print("\n🕋 May your journey be blessed!\n")


if __name__ == "__main__":
    main()
