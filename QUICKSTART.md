# Quick Start Guide - Umrah Trip Creator

Get your Umrah trip planning system up and running in minutes!

## Prerequisites

- Python 3.10 or higher
- AWS Account (for deployment)
- API Keys (for production use)

## Local Development (Streamlit Frontend)

### 1. Clone and Setup

```bash
cd umrah-trip-creator
```

### 2. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r frontend/requirements.txt
```

### 3. Run Streamlit App

```bash
# Option 1: Using the run script
cd frontend
chmod +x run.sh
./run.sh

# Option 2: Direct streamlit command
streamlit run frontend/streamlit_app.py
```

### 4. Open Your Browser

Navigate to: **http://localhost:8501**

## Using the Application

### Step 1: Travel Dates
- Select your departure and return dates
- Choose arrival/departure cities (Jeddah or Madinah)
- Minimum 7 days recommended

### Step 2: Traveler Details
- Add information for all travelers
- Include names, nationalities, ages
- Passport numbers (optional but recommended)

### Step 3: Hotel Preferences
- Set preferences for Makkah hotel
- Set preferences for Madinah hotel
- Choose proximity to Haram
- Select star rating and amenities

### Step 4: Budget & Requirements
- Set your budget per person
- Specify special requirements
- Choose flight preferences
- Add any additional notes

### Step 5: Review & Generate
- Review all your information
- Click "Generate My Umrah Trip Plan"
- AI agents will work together to create your plan

### Step 6: Trip Options
- View flight options
- Compare hotel choices
- Check visa requirements
- Review detailed itinerary
- Complete booking

## Features

### 🤖 Multi-Agent System
- **Orchestrator Agent**: Coordinates all other agents
- **Flight Agent**: Searches best flight options
- **Hotel Agent**: Finds accommodations near Haram
- **Visa Agent**: Handles visa requirements
- **Itinerary Agent**: Creates spiritual journey schedule

### ✨ Key Features
- Real-time flight and hotel search
- Visa requirement checking by nationality
- Detailed Umrah ritual guidance
- Day-by-day itinerary planning
- Cost breakdown and comparison
- Multi-traveler support
- Special requirements handling

## Deployment to AWS

### 1. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys and AWS details
```

### 2. Deploy

```bash
uv run deploy.py
```

### 3. Access Deployed Application

The deployment script will provide you with:
- API Gateway URL
- CloudFront distribution URL
- AgentCore Runtime endpoints

## Testing

### Test Individual Agents

```bash
# Test flight agent
uv run test/test_flight_agent.py

# Test hotel agent
uv run test/test_hotel_agent.py

# Test visa agent
uv run test/test_visa_agent.py

# Test itinerary agent
uv run test/test_itinerary_agent.py
```

### Interactive Testing

```bash
uv run test/interactive_test.py
```

## Troubleshooting

### Port Already in Use

```bash
# Kill process on port 8501
lsof -ti:8501 | xargs kill -9

# Or use a different port
streamlit run frontend/streamlit_app.py --server.port 8502
```

### Missing Dependencies

```bash
# Reinstall all dependencies
uv sync --reinstall
```

### API Connection Issues

Check your `.env` file has correct API keys:
- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- AWS credentials

## Next Steps

1. **Customize Agents**: Modify agent prompts in `agents/` directory
2. **Add Tools**: Create custom tools in `tools/` directory
3. **Enhance UI**: Customize Streamlit interface in `frontend/`
4. **Deploy**: Use `deploy.py` for AWS deployment

## Support

For issues or questions:
- Check the main README.md
- Review agent documentation
- Check AWS CloudWatch logs (for deployed version)

## Tips for Best Results

1. **Be Specific**: Provide detailed preferences for better results
2. **Plan Ahead**: Book at least 30 days in advance
3. **Check Visa**: Verify visa requirements early
4. **Stay Flexible**: Consider multiple options for best deals
5. **Review Carefully**: Double-check all details before booking

---

**May your Umrah journey be blessed and accepted! 🕋**
