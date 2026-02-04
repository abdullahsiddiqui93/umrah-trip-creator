"""
Setup AgentCore Memory for Umrah Trip Creator
Creates both short-term and long-term memory resources
"""

from bedrock_agentcore.memory import MemoryClient
import uuid

client = MemoryClient(region_name='us-west-2')

print("="*60)
print("Creating memory resources for Umrah Trip Creator...")
print("="*60)

# Short-Term Memory (STM) - for conversation within sessions
print("\n1. Creating Short-Term Memory (STM)...")
stm = client.create_memory_and_wait(
    name=f"UmrahTrip_STM_{uuid.uuid4().hex[:8]}",
    strategies=[],  # No extraction strategies
    event_expiry_days=7
)
print(f"✅ STM Memory Created: {stm['id']}")
print("   - Stores conversation within sessions")
print("   - 7-day retention")

# Long-Term Memory (LTM) - for user preferences across sessions
print("\n2. Creating Long-Term Memory (LTM)...")
ltm = client.create_memory_and_wait(
    name=f"UmrahTrip_LTM_{uuid.uuid4().hex[:8]}",
    strategies=[
        # Extract user travel preferences (single namespace per strategy)
        {"userPreferenceMemoryStrategy": {
            "name": "travel_preferences",
            "namespaces": ["/user/preferences/"]
        }},
        # Extract user facts (single namespace per strategy)
        {"semanticMemoryStrategy": {
            "name": "user_facts",
            "namespaces": ["/user/facts/"]
        }}
    ],
    event_expiry_days=90  # Keep for 90 days
)
print(f"✅ LTM Memory Created: {ltm['id']}")
print("   - Extracts preferences and facts")
print("   - 90-day retention")
print("   - Cross-session memory")

print("\n" + "="*60)
print("✅ Memory setup complete!")
print("="*60)
print("\nAdd these to your .env file:")
print(f"MEMORY_STM_ID={stm['id']}")
print(f"MEMORY_LTM_ID={ltm['id']}")
print("="*60)
