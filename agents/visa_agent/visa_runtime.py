"""
Visa Agent for AgentCore Runtime
Simplified version for reliable deployment
"""

import os
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent

# Initialize AgentCore app
app = BedrockAgentCoreApp()

# Create visa agent
visa_agent = Agent(
    model=os.getenv("VISA_AGENT_MODEL", "anthropic.claude-3-5-haiku-20241022-v1:0"),
    system_prompt="""You are a Visa Requirements Specialist for Umrah trips.

Your expertise:
1. Provide visa requirements for Saudi Arabia Umrah visa
2. Explain the application process:
   - Online application steps
   - Required documents (passport, photo, etc.)
   - Processing time
   - Visa fees
   - Validity period
3. Country-specific requirements
4. Health requirements (vaccinations, insurance)

When users ask about visas, gather:
- Nationality/passport country
- Travel dates
- Previous Saudi visa history
- Age of travelers

Provide accurate, up-to-date visa information and helpful guidance.

Note: Umrah visa is typically:
- Valid for 90 days
- Single or multiple entry
- Can be obtained online
- Requires valid passport (6+ months validity)
- Requires travel insurance
- Requires proof of accommodation"""
)


@app.entrypoint
def invoke(payload, context):
    """Main entry point for visa agent"""
    
    user_message = payload.get("prompt", "Hello")
    
    try:
        response = visa_agent(user_message)
        
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
