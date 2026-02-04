# Multiple Options & Custom Itinerary Update

## Summary
Enhanced the Umrah Trip Creator to provide multiple flight and hotel options, and added support for custom itinerary requirements.

## Changes Made

### 1. Frontend Updates (`frontend/streamlit_app.py`)

**Added Custom Itinerary Field:**
- New text area in Step 4 (Budget & Requirements) for users to specify custom itinerary
- Example: "Stay in Madinah for the first night, then go to Makkah for 4 days, then return to Madinah for last 4 days"
- Field is optional - if left blank, agents will use standard recommendations

**Location:** Step 4 - Budget & Requirements section

### 2. Client Updates (`frontend/agentcore_client.py`)

**Enhanced Prompt Formatting:**
- Added custom itinerary requirements to the prompt sent to orchestrator
- Explicitly requests multiple options (2-3) for both flights and hotels
- Instructs agents to follow custom itinerary when booking hotels

**Key Changes:**
```python
# Custom itinerary handling
if special_reqs.get('custom_itinerary'):
    prompt += f"\n**Custom Itinerary Requirements:**\n{special_reqs.get('custom_itinerary')}\n"
    prompt += "\nIMPORTANT: Please follow this custom itinerary when booking hotels..."

# Request multiple options
prompt += "\nPlease help me plan this Umrah trip with MULTIPLE flight options (at least 2-3 options)..."
prompt += "\nFor flights: Provide at least 2-3 different flight options..."
prompt += "\nFor hotels: Provide at least 2-3 hotel options for each city..."
```

### 3. Orchestrator Agent Updates (`agents/orchestrator/orchestrator_runtime.py`)

**Enhanced System Prompt:**
- Explicitly instructs orchestrator to request multiple options from specialized agents
- Added detailed workflow for handling custom itineraries
- Provides examples of how to call agents for multiple options

**Key Features:**
- Requests 2-3 flight options with different airlines and price points
- Requests 2-3 hotel options per city with different star ratings and distances
- Handles custom itineraries by calling hotel agent separately for each city/date range
- Example: "Madinah 1 night, Makkah 4 nights, Madinah 4 nights" → 3 separate hotel searches

**Workflow for Custom Itineraries:**
```
If user specifies: "Madinah 1 night, then Makkah 4 nights, then Madinah 4 nights"
1. Search Madinah hotels for March 15-16 (1 night)
2. Search Makkah hotels for March 16-20 (4 nights)
3. Search Madinah hotels for March 20-24 (4 nights)
```

### 4. Flight Agent Updates (`agents/flight_agent/flight_runtime.py`)

**Enhanced System Prompt:**
- Instructs agent to always provide 2-3 flight options minimum
- Presents options with different airlines, price points, times, and connections
- Compares options (cheapest, fastest, most convenient)

**Key Features:**
- Returns up to 5 results from Amadeus API
- Presents at least 2-3 options to users
- Includes variety: different airlines, times, direct vs connecting flights
- Clear option numbering (Option 1, Option 2, etc.)

### 5. Hotel Agent Updates (`agents/hotel_agent/hotel_runtime.py`)

**Enhanced System Prompt:**
- Instructs agent to always provide 2-3 hotel options per city minimum
- Handles custom itineraries by searching each city/date range separately
- Presents options with different star ratings, prices, and distances

**Key Features:**
- Returns up to 10 results from Amadeus API
- Presents at least 2-3 options per city
- Includes variety: 3-star, 4-star, 5-star, different distances from Haram
- Clear option numbering for each city
- Compares options (closest, best value, most luxurious)

**Custom Itinerary Handling:**
- Searches each city separately with specific date ranges
- Example: If user wants "Madinah → Makkah → Madinah", agent searches:
  1. Madinah hotels for first date range
  2. Makkah hotels for second date range
  3. Madinah hotels for third date range

## Deployment Status

All agents have been successfully redeployed:
- ✅ Orchestrator Agent: `arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo`
- ✅ Flight Agent: `arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_flight_agent-ufM0XiC3fw`
- ✅ Hotel Agent: `arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_hotel_agent-P3Am0WF25G`

## How to Use

### Multiple Options
The system now automatically provides multiple options:
- **Flights:** 2-3 options with different airlines, times, and prices
- **Hotels:** 2-3 options per city with different star ratings and distances

No special action needed - just submit your trip requirements and the agents will provide multiple options.

### Custom Itinerary
In Step 4 (Budget & Requirements), use the "Custom Itinerary Requirements" field:

**Example 1:**
```
Stay in Madinah for the first night, then go to Makkah for 4 days, then return to Madinah for the last 4 days.
```

**Example 2:**
```
Arrive in Jeddah, go directly to Makkah for 5 days, then Madinah for 3 days.
```

**Example 3:**
```
Madinah first for 3 nights, then Makkah for 5 nights.
```

The agents will:
1. Book hotels in the specified cities
2. Follow the exact order and duration you specify
3. Provide multiple hotel options for each leg of the journey
4. Adjust flight arrival/departure cities accordingly

## Testing

To test the new features:

1. **Multiple Options Test:**
   - Fill out trip requirements normally
   - Leave custom itinerary blank
   - Generate plan
   - Verify you receive 2-3 flight options and 2-3 hotel options per city

2. **Custom Itinerary Test:**
   - Fill out trip requirements
   - Add custom itinerary: "Madinah 2 nights, then Makkah 5 nights, then Madinah 2 nights"
   - Generate plan
   - Verify hotels are booked in the specified order and duration
   - Verify you receive multiple options for each city/date range

## Frontend Access

The Streamlit frontend is running at: http://localhost:8501

## Notes

- The orchestrator may take 2-3 minutes to complete as it coordinates multiple agents
- The 5-minute timeout is configured to handle this
- Custom itineraries are optional - if left blank, agents use standard recommendations
- All options include real-time data from Amadeus API (flights and hotels)
