# 🕋 Umrah Trip Creator - START HERE

Welcome! This is your complete multi-agent Umrah trip planning system.

## 🚀 Quick Start (3 Steps)

### 1. Navigate to Frontend
```bash
cd umrah-trip-creator/frontend
```

### 2. Make Run Script Executable
```bash
chmod +x run.sh
```

### 3. Launch the App
```bash
./run.sh
```

Then open your browser to: **http://localhost:8501**

---

## 📚 Documentation Guide

### For Users
- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[USER_FLOW.md](USER_FLOW.md)** - See how the app works
- **[FEATURES.md](FEATURES.md)** - All features explained

### For Developers
- **[README.md](README.md)** - Complete technical documentation
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - What we built
- **[test_local.py](test_local.py)** - Test the agents

---

## 📁 Project Structure

```
umrah-trip-creator/
│
├── 📄 START_HERE.md          ← You are here!
├── 📄 README.md              ← Main documentation
├── 📄 QUICKSTART.md          ← Quick start guide
├── 📄 FEATURES.md            ← Feature list
├── 📄 PROJECT_SUMMARY.md     ← Project overview
├── 📄 USER_FLOW.md           ← User journey
│
├── 🤖 agents/                ← AI Agents
│   ├── orchestrator/         ← Main coordinator
│   ├── flight_agent/         ← Flight search
│   ├── hotel_agent/          ← Hotel booking
│   ├── visa_agent/           ← Visa processing
│   └── itinerary_agent/      ← Trip planning
│
├── 🎨 frontend/              ← Streamlit Web App
│   ├── streamlit_app.py      ← Main application
│   ├── config.py             ← Configuration
│   ├── requirements.txt      ← Dependencies
│   └── run.sh               ← Launch script
│
├── 🧪 test_local.py          ← Testing script
├── ⚙️ pyproject.toml         ← Project config
├── 📝 .env.example           ← Environment template
└── 🚫 .gitignore             ← Git ignore rules
```

---

## 🎯 What This System Does

### For Pilgrims
1. **Collects** your travel preferences
2. **Searches** flights, hotels, and visa requirements
3. **Creates** a detailed Umrah itinerary
4. **Presents** multiple options to choose from
5. **Handles** booking and confirmation

### How It Works
- **5 AI Agents** work together using A2A protocol
- **Orchestrator** coordinates everything
- **Specialized agents** handle specific tasks
- **Streamlit UI** provides beautiful interface
- **Real-time processing** with progress tracking

---

## 🎨 User Interface

### 6-Step Wizard
1. 📅 **Travel Dates** - When are you going?
2. 👥 **Travelers** - Who's coming along?
3. 🏨 **Hotels** - Where to stay?
4. 💰 **Budget** - How much to spend?
5. 📋 **Review** - Check everything
6. ✨ **Options** - Choose and book!

---

## 🤖 The AI Agents

### 1. Orchestrator Agent (Strands)
- Coordinates all other agents
- Validates user input
- Aggregates results
- Manages booking process

### 2. Flight Agent (OpenAI)
- Searches flights to Saudi Arabia
- Compares prices and timings
- Considers baggage and amenities
- Recommends best options

### 3. Hotel Agent (Claude)
- Finds hotels near Haram
- Filters by preferences
- Checks reviews and ratings
- Suggests best value options

### 4. Visa Agent (OpenAI)
- Checks visa requirements
- Provides application guide
- Lists required documents
- Estimates processing time

### 5. Itinerary Agent (Claude)
- Creates day-by-day schedule
- Plans Umrah rituals
- Suggests ziyarat sites
- Optimizes timing

---

## 💻 System Requirements

- **Python**: 3.10 or higher
- **Browser**: Chrome, Firefox, Safari, or Edge
- **Internet**: Required for AI models
- **RAM**: 4GB minimum
- **Disk**: 500MB free space

---

## 🔧 Installation Options

### Option 1: Quick Start (Recommended)
```bash
cd umrah-trip-creator/frontend
./run.sh
```

### Option 2: Manual Setup
```bash
cd umrah-trip-creator
pip install -r frontend/requirements.txt
streamlit run frontend/streamlit_app.py
```

### Option 3: Using uv
```bash
cd umrah-trip-creator
uv sync
uv run streamlit run frontend/streamlit_app.py
```

---

## 🧪 Testing

### Test All Agents
```bash
python test_local.py
```

### Test Individual Components
```bash
# Test orchestrator
python -c "from agents.orchestrator.orchestrator_agent import create_orchestrator_agent; print('✅ Orchestrator OK')"

# Test flight agent
python -c "from agents.flight_agent.flight_agent import create_flight_agent; print('✅ Flight Agent OK')"

# Test hotel agent
python -c "from agents.hotel_agent.hotel_agent import create_hotel_agent; print('✅ Hotel Agent OK')"

# Test visa agent
python -c "from agents.visa_agent.visa_agent import create_visa_agent; print('✅ Visa Agent OK')"

# Test itinerary agent
python -c "from agents.itinerary_agent.itinerary_agent import create_itinerary_agent; print('✅ Itinerary Agent OK')"
```

---

## 🎓 Learning Path

### Beginner
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Run the Streamlit app
3. Try planning a sample trip
4. Explore the UI features

### Intermediate
1. Read [README.md](README.md)
2. Review agent code in `agents/`
3. Understand the architecture
4. Modify agent prompts

### Advanced
1. Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
2. Add API integrations
3. Deploy to AWS
4. Customize for your needs

---

## 🆘 Troubleshooting

### App Won't Start
```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install -r frontend/requirements.txt --force-reinstall

# Try different port
streamlit run frontend/streamlit_app.py --server.port 8502
```

### Import Errors
```bash
# Make sure you're in the right directory
pwd  # Should end with /umrah-trip-creator

# Add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Port Already in Use
```bash
# Kill process on port 8501
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run frontend/streamlit_app.py --server.port 8502
```

---

## 🌟 Key Features

- ✅ Multi-agent AI system
- ✅ Beautiful Streamlit interface
- ✅ 6-step wizard workflow
- ✅ Real-time agent coordination
- ✅ Flight search & comparison
- ✅ Hotel recommendations
- ✅ Visa requirement checking
- ✅ Detailed itinerary planning
- ✅ Cost breakdown
- ✅ Booking management
- ✅ Downloadable documents
- ✅ Multi-traveler support
- ✅ Special requirements handling
- ✅ 30+ nationalities supported
- ✅ 14 currencies supported

---

## 📞 Next Steps

1. **Run the app** - See it in action!
2. **Read the docs** - Understand how it works
3. **Test the agents** - Verify everything works
4. **Customize** - Make it your own
5. **Deploy** - Share with others

---

## 🎉 You're Ready!

Everything is set up and ready to go. Just run:

```bash
cd umrah-trip-creator/frontend
./run.sh
```

Then open **http://localhost:8501** and start planning!

---

**May your Umrah journey be blessed and accepted! 🕋**

*Built with ❤️ for the Muslim community*
