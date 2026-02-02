# Umrah Trip Creator - Multi-Agent System

A comprehensive multi-agent system built on Amazon Bedrock AgentCore for planning and booking Umrah trips. The system uses Agent-to-Agent (A2A) protocol to coordinate specialized agents for flights, hotels, visas, and itinerary planning.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                   Streamlit Web Interface                       │
│  (Multi-step form: Dates → Travelers → Hotels → Budget)        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Main Orchestrator Agent (Strands)                  │
│  • Collects & validates user requirements                       │
│  • Coordinates specialized agents via A2A protocol              │
│  • Aggregates results & presents options                        │
│  • Handles booking confirmations                                │
└─────┬──────────┬──────────┬──────────┬────────────────────────┘
      │          │          │          │
      │ A2A      │ A2A      │ A2A      │ A2A
      │          │          │          │
      ▼          ▼          ▼          ▼
┌──────────┐ ┌────────┐ ┌────────┐ ┌──────────────┐
│ Flight   │ │ Hotel  │ │ Visa   │ │ Itinerary    │
│ Agent    │ │ Agent  │ │ Agent  │ │ Agent        │
│ (OpenAI) │ │(Claude)│ │(OpenAI)│ │  (Claude)    │
└────┬─────┘ └───┬────┘ └───┬────┘ └──────┬───────┘
     │           │          │             │
     ▼           ▼          ▼             ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐
│ Amadeus │ │Booking  │ │  Visa   │ │  Umrah   │
│   API   │ │   API   │ │Database │ │Knowledge │
└─────────┘ └─────────┘ └─────────┘ └──────────┘

                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Amazon Bedrock AgentCore Runtime                   │
│  • Agent hosting & scaling                                      │
│  • A2A protocol support                                         │
│  • Memory management (short & long-term)                        │
│  • Observability (CloudWatch, OpenTelemetry)                    │
│  • Gateway for API access                                       │
│  • Identity & authentication (Cognito OAuth 2.0)                │
└─────────────────────────────────────────────────────────────────┘
```

## Features

- **Intelligent Orchestration**: Main agent coordinates all specialized agents
- **Flight Search**: Find best flight options based on dates, budget, and preferences
- **Hotel Booking**: Search hotels near Haram with user preferences
- **Visa Processing**: Check visa requirements by nationality and assist with applications
- **Itinerary Planning**: Create detailed day-by-day Umrah ritual schedules
- **Multi-nationality Support**: Handle visa requirements for different countries
- **Group Travel**: Support for multiple travelers with different requirements
- **AWS Cognito Authentication**: Secure user sign up, sign in, and session management
- **Demo Mode**: Test without authentication, production mode with full security

## User Input Collection

The main agent collects:
- Travel dates (departure & return)
- Number of travelers
- Nationalities (for visa requirements)
- Hotel preferences (proximity to Haram, star rating, amenities)
- Budget constraints
- Special requirements (wheelchair access, dietary needs, etc.)

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured with credentials
3. **Python 3.10+**
4. **uv** package manager
5. **API Keys**:
   - Amadeus API (for flights)
   - Booking.com API (for hotels)
   - OpenAI/Anthropic API keys

## Quick Start

```bash
# Clone and navigate to project
cd umrah-trip-creator

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Deploy to AWS
uv run deploy.py

# Run locally for testing
uv run test_local.py
```

## Project Structure

```
umrah-trip-creator/
├── agents/
│   ├── orchestrator/          # Main coordinator agent
│   ├── flight_agent/          # Flight search & booking
│   ├── hotel_agent/           # Hotel search & booking
│   ├── visa_agent/            # Visa requirements & processing
│   └── itinerary_agent/       # Umrah ritual scheduling
├── tools/
│   ├── flight_tools.py        # Flight API integrations
│   ├── hotel_tools.py         # Hotel API integrations
│   ├── visa_tools.py          # Visa database & APIs
│   └── itinerary_tools.py     # Umrah ritual information
├── frontend/                  # React web interface
├── infrastructure/            # CloudFormation templates
├── deploy.py                  # Deployment script
├── cleanup.py                 # Cleanup script
└── test_local.py             # Local testing
```

## Agent Details

### 1. Orchestrator Agent
- Collects user requirements
- Validates input data
- Delegates tasks to specialized agents
- Aggregates results and presents options
- Handles booking confirmations

### 2. Flight Agent
- Searches flights to Jeddah/Medina
- Compares prices across airlines
- Checks baggage allowances
- Handles multi-city options (Jeddah → Medina)

### 3. Hotel Agent
- Searches hotels in Makkah and Madinah
- Filters by proximity to Haram
- Checks availability for group bookings
- Provides amenity information

### 4. Visa Agent
- Checks visa requirements by nationality
- Provides application procedures
- Estimates processing times
- Tracks visa status

### 5. Itinerary Agent
- Creates Umrah ritual schedules
- Suggests optimal times for rituals
- Provides guidance for each step
- Includes transportation between sites

## Deployment

The system deploys on Amazon Bedrock AgentCore Runtime with:
- Auto-scaling for high availability
- OAuth 2.0 authentication via Cognito
- CloudWatch observability
- S3 for document storage
- DynamoDB for booking data

## Testing

```bash
# Test individual agents
uv run test/test_flight_agent.py
uv run test/test_hotel_agent.py
uv run test/test_visa_agent.py
uv run test/test_itinerary_agent.py

# Test full orchestration
uv run test/test_orchestrator.py

# Interactive testing
uv run test/interactive_test.py
```

## Cleanup

```bash
uv run cleanup.py
```

## License

MIT License - See LICENSE file for details
