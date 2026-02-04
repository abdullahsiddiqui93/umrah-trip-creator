"""
Itinerary Agent for AgentCore Runtime
Simplified version for reliable deployment
"""

import os
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent

# Initialize AgentCore app
app = BedrockAgentCoreApp()

# Create itinerary agent
itinerary_agent = Agent(
    model=os.getenv("ITINERARY_AGENT_MODEL", "anthropic.claude-3-5-sonnet-20241022-v2:0"),
    system_prompt="""You are an Umrah Itinerary Planning Specialist.

Your expertise:
1. Create detailed day-by-day Umrah itineraries
2. Include essential Umrah rituals:
   - Ihram preparation
   - Tawaf (circumambulation of Kaaba)
   - Sa'i (walking between Safa and Marwa)
   - Hair cutting/shaving
   - Optional: Visit to Madinah
3. Recommend:
   - Best times for rituals (avoid crowds)
   - Ziyarat (historical sites)
   - Prayer times and locations
   - Rest periods
   - Shopping and dining

When creating itineraries, consider:
- Total trip duration
- Physical fitness level
- First-time vs. experienced pilgrims
- Family with children or elderly
- Ramadan vs. non-Ramadan timing

Provide spiritually meaningful and practically feasible itineraries."""
)


@app.entrypoint
def invoke(payload, context):
    """Main entry point for itinerary agent"""
    
    user_message = payload.get("prompt", "Hello")
    
    try:
        response = itinerary_agent(user_message)
        
        if hasattr(response, 'message') and 'content' in response.message:
            result_text = response.message['content'][0]['text']
        else:
            result_text = str(response)
        
        return {
            "result": result_text,
            "status": "success"
        }
    except Exception as e:
        print(f"Error processing request: {e}")
        return {
            "result": f"I apologize, but I encountered an error: {str(e)}",
            "status": "error"
        }


if __name__ == "__main__":
    app.run()
