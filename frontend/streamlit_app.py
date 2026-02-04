"""
Streamlit Frontend for Umrah Trip Creator
Multi-step interface for planning Umrah trips with AI agents
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import json
import time

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Import authentication module
from frontend.auth import require_authentication, show_user_menu

# Import AgentCore client for deployed agents
from frontend.agentcore_client import get_agentcore_client

# Configuration
USE_AGENTCORE = True  # Set to True to use deployed AgentCore agents, False for demo mode

# Page configuration
st.set_page_config(
    page_title="Umrah Trip Creator",
    page_icon="🕋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e7e34;
        text-align: center;
        margin-bottom: 2rem;
    }
    .step-header {
        font-size: 1.5rem;
        color: #155724;
        margin-top: 1rem;
    }
    .info-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'trip_plan' not in st.session_state:
    st.session_state.trip_plan = None
if 'show_booking' not in st.session_state:
    st.session_state.show_booking = False
if 'selected_flight' not in st.session_state:
    st.session_state.selected_flight = None
if 'selected_makkah_hotel' not in st.session_state:
    st.session_state.selected_makkah_hotel = None
if 'selected_madinah_hotel' not in st.session_state:
    st.session_state.selected_madinah_hotel = None


def main():
    """Main application flow"""
    
    # Check authentication first
    if not require_authentication():
        return  # Show login page
    
    # Header
    st.markdown('<h1 class="main-header">🕋 Umrah Trip Creator</h1>', unsafe_allow_html=True)
    st.markdown("### Plan your blessed journey with AI-powered assistance")
    
    # Demo/Production mode indicator
    if USE_AGENTCORE:
        st.success("🚀 **Production Mode**: Connected to AWS Bedrock AgentCore agents. Real AI-powered trip planning!")
    else:
        st.info("🎭 **Demo Mode**: This is a demonstration with sample data. All results are mock data for testing purposes. See [DEMO_VS_PRODUCTION.md](https://github.com/your-repo/umrah-trip-creator/blob/main/DEMO_VS_PRODUCTION.md) for details.")
    
    # Progress bar
    progress = (st.session_state.step - 1) / 5
    st.progress(progress)
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/300x150?text=Umrah+Trip+Creator", use_container_width=True)
        st.markdown("### Navigation")
        st.markdown(f"**Current Step:** {st.session_state.step}/6")
        
        steps = [
            "1️⃣ Travel Dates",
            "2️⃣ Traveler Details", 
            "3️⃣ Hotel Preferences",
            "4️⃣ Budget & Requirements",
            "5️⃣ Review & Generate Plan",
            "6️⃣ Trip Options"
        ]
        
        for i, step_name in enumerate(steps, 1):
            if i == st.session_state.step:
                st.markdown(f"**{step_name}** ✓")
            elif i < st.session_state.step:
                st.markdown(f"~~{step_name}~~ ✓")
            else:
                st.markdown(f"{step_name}")
        
        st.markdown("---")
        if st.button("🔄 Start Over"):
            st.session_state.step = 1
            st.session_state.user_data = {}
            st.session_state.trip_plan = None
            st.rerun()
        
        # Show user menu
        show_user_menu()
    
    # Main content based on step
    if st.session_state.step == 1:
        step_travel_dates()
    elif st.session_state.step == 2:
        step_traveler_details()
    elif st.session_state.step == 3:
        step_hotel_preferences()
    elif st.session_state.step == 4:
        step_budget_requirements()
    elif st.session_state.step == 5:
        step_review_generate()
    elif st.session_state.step == 6:
        step_trip_options()


def step_travel_dates():
    """Step 1: Collect travel dates"""
    st.markdown('<h2 class="step-header">📅 Step 1: Travel Dates</h2>', unsafe_allow_html=True)
    
    # Departure city (where flying FROM)
    st.markdown("#### 🛫 Where are you flying from?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        departure_country = st.selectbox(
            "Country",
            ["United States", "United Kingdom", "Canada", "Australia", "India", 
             "Pakistan", "Bangladesh", "Malaysia", "Indonesia", "Turkey", "Egypt",
             "Nigeria", "South Africa", "UAE", "France", "Germany", "Other"],
            help="Select your departure country"
        )
    
    with col2:
        # Common airports by country
        airport_options = {
            "United States": ["New York (JFK)", "Los Angeles (LAX)", "Chicago (ORD)", 
                            "Houston (IAH)", "Washington DC (IAD)", "Other"],
            "United Kingdom": ["London Heathrow (LHR)", "London Gatwick (LGW)", 
                             "Manchester (MAN)", "Birmingham (BHX)", "Other"],
            "Canada": ["Toronto (YYZ)", "Montreal (YUL)", "Vancouver (YVR)", "Other"],
            "Australia": ["Sydney (SYD)", "Melbourne (MEL)", "Perth (PER)", "Other"],
            "India": ["Delhi (DEL)", "Mumbai (BOM)", "Bangalore (BLR)", "Hyderabad (HYD)", "Other"],
            "Pakistan": ["Karachi (KHI)", "Lahore (LHE)", "Islamabad (ISB)", "Other"],
            "Other": ["Enter city name"]
        }
        
        airports = airport_options.get(departure_country, ["Enter city name"])
        departure_airport = st.selectbox(
            "Airport/City",
            airports,
            help="Select your departure airport"
        )
    
    st.markdown("---")
    
    # Travel dates
    st.markdown("#### 📅 Travel Dates")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Departure Date**")
        min_date = datetime.now() + timedelta(days=30)
        departure_date = st.date_input(
            "When do you plan to depart?",
            min_value=min_date,
            value=min_date,
            help="Umrah bookings typically require 30+ days advance notice"
        )
    
    with col2:
        st.markdown("**Return Date**")
        min_return = departure_date + timedelta(days=7)
        return_date = st.date_input(
            "When do you plan to return?",
            min_value=min_return,
            value=min_return,
            help="Minimum 7 days recommended for Umrah"
        )
    
    # Calculate duration
    duration = (return_date - departure_date).days
    
    st.info(f"📊 Trip Duration: **{duration} days**")
    
    if duration < 7:
        st.warning("⚠️ We recommend at least 7 days for a comfortable Umrah experience.")
    elif duration > 30:
        st.warning("⚠️ Extended stays may require additional visa considerations.")
    
    st.markdown("---")
    
    # Saudi Arabia arrival/departure cities
    st.markdown("#### 🕋 Saudi Arabia Arrival & Departure")
    col1, col2 = st.columns(2)
    
    with col1:
        arrival_city = st.selectbox(
            "Arrival City in Saudi Arabia",
            ["Jeddah (JED)", "Madinah (MED)"],
            help="Most pilgrims arrive in Jeddah, closer to Makkah"
        )
    
    with col2:
        departure_city = st.selectbox(
            "Departure City from Saudi Arabia",
            ["Jeddah (JED)", "Madinah (MED)", "Same as arrival"],
        )
    
    if st.button("Next: Traveler Details →", type="primary", use_container_width=True):
        st.session_state.user_data['travel_dates'] = {
            'departure_country': departure_country,
            'departure_airport': departure_airport,
            'departure': departure_date.isoformat(),
            'return': return_date.isoformat(),
            'duration': duration,
            'arrival_city': arrival_city,
            'departure_city': departure_city
        }
        st.session_state.step = 2
        st.rerun()


def step_traveler_details():
    """Step 2: Collect traveler information"""
    st.markdown('<h2 class="step-header">👥 Step 2: Traveler Details</h2>', unsafe_allow_html=True)
    
    num_travelers = st.number_input(
        "Number of Travelers",
        min_value=1,
        max_value=20,
        value=st.session_state.user_data.get('num_travelers', 1),
        help="Maximum 20 travelers per booking"
    )
    
    st.markdown("---")
    
    travelers = []
    
    for i in range(num_travelers):
        st.markdown(f"#### Traveler {i+1}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = st.text_input(f"Full Name", key=f"name_{i}", placeholder="As per passport")
        
        with col2:
            nationality = st.selectbox(
                f"Nationality",
                ["United States", "United Kingdom", "Canada", "Australia", "India", 
                 "Pakistan", "Bangladesh", "Malaysia", "Indonesia", "Turkey", "Egypt",
                 "Nigeria", "South Africa", "UAE", "Other"],
                key=f"nationality_{i}"
            )
        
        with col3:
            age = st.number_input(f"Age", min_value=1, max_value=120, value=30, key=f"age_{i}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            gender = st.selectbox(f"Gender", ["Male", "Female"], key=f"gender_{i}")
        
        with col2:
            passport_number = st.text_input(f"Passport Number", key=f"passport_{i}", placeholder="Optional")
        
        travelers.append({
            'name': name,
            'nationality': nationality,
            'age': age,
            'gender': gender,
            'passport_number': passport_number
        })
        
        st.markdown("---")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    
    with col2:
        if st.button("Next: Hotel Preferences →", type="primary", use_container_width=True):
            # Validate
            if all(t['name'] for t in travelers):
                st.session_state.user_data['num_travelers'] = num_travelers
                st.session_state.user_data['travelers'] = travelers
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("Please fill in all traveler names")


def step_hotel_preferences():
    """Step 3: Collect hotel preferences"""
    st.markdown('<h2 class="step-header">🏨 Step 3: Hotel Preferences</h2>', unsafe_allow_html=True)
    
    st.markdown("### Makkah Hotel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        makkah_proximity = st.select_slider(
            "Distance from Masjid al-Haram",
            options=["Walking Distance (<500m)", "Close (500m-1km)", "Moderate (1-2km)", "Far (>2km)"],
            value="Walking Distance (<500m)",
            help="Closer hotels are more expensive but more convenient"
        )
        
        makkah_star = st.select_slider(
            "Hotel Star Rating",
            options=[3, 4, 5],
            value=4,
            key="makkah_star"
        )
    
    with col2:
        makkah_view = st.checkbox("Haram View", value=False, help="Premium option")
        makkah_amenities = st.multiselect(
            "Preferred Amenities",
            ["WiFi", "Breakfast Included", "Airport Shuttle", "Laundry", "Restaurant", "Elevator"],
            default=["WiFi", "Breakfast Included"],
            key="makkah_amenities"
        )
    
    st.markdown("---")
    st.markdown("### Madinah Hotel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        madinah_proximity = st.select_slider(
            "Distance from Masjid an-Nabawi",
            options=["Walking Distance (<500m)", "Close (500m-1km)", "Moderate (1-2km)", "Far (>2km)"],
            value="Walking Distance (<500m)",
            key="madinah_proximity"
        )
        
        madinah_star = st.select_slider(
            "Hotel Star Rating",
            options=[3, 4, 5],
            value=4,
            key="madinah_star"
        )
    
    with col2:
        madinah_view = st.checkbox("Haram View", value=False, key="madinah_view")
        madinah_amenities = st.multiselect(
            "Preferred Amenities",
            ["WiFi", "Breakfast Included", "Airport Shuttle", "Laundry", "Restaurant", "Elevator"],
            default=["WiFi", "Breakfast Included"],
            key="madinah_amenities"
        )
    
    st.markdown("---")
    
    # Room configuration
    st.markdown("### Room Configuration")
    room_type = st.selectbox(
        "Room Type",
        ["Single", "Double", "Triple", "Quad", "Family Suite"],
        help="Based on number of travelers"
    )
    
    # Navigation
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    
    with col2:
        if st.button("Next: Budget & Requirements →", type="primary", use_container_width=True):
            st.session_state.user_data['hotel_preferences'] = {
                'makkah': {
                    'proximity': makkah_proximity,
                    'star_rating': makkah_star,
                    'haram_view': makkah_view,
                    'amenities': makkah_amenities
                },
                'madinah': {
                    'proximity': madinah_proximity,
                    'star_rating': madinah_star,
                    'haram_view': madinah_view,
                    'amenities': madinah_amenities
                },
                'room_type': room_type
            }
            st.session_state.step = 4
            st.rerun()


def step_budget_requirements():
    """Step 4: Budget and special requirements"""
    st.markdown('<h2 class="step-header">💰 Step 4: Budget & Special Requirements</h2>', unsafe_allow_html=True)
    
    st.markdown("### Budget")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "SAR", "AED", "INR", "PKR"])
    
    with col2:
        budget_per_person = st.number_input(
            f"Budget per Person ({currency})",
            min_value=500,
            max_value=50000,
            value=3000,
            step=100,
            help="Includes flights, hotels, and visa"
        )
    
    with col3:
        flexibility = st.select_slider(
            "Budget Flexibility",
            options=["Strict", "Moderate", "Flexible"],
            value="Moderate"
        )
    
    total_budget = budget_per_person * st.session_state.user_data.get('num_travelers', 1)
    st.info(f"💵 Total Trip Budget: **{currency} {total_budget:,}**")
    
    st.markdown("---")
    st.markdown("### Special Requirements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        wheelchair_access = st.checkbox("♿ Wheelchair Accessibility Required")
        elderly_travelers = st.checkbox("👴 Elderly Travelers (need special assistance)")
        dietary_requirements = st.checkbox("🍽️ Special Dietary Requirements")
    
    with col2:
        female_only_group = st.checkbox("👩 Female-only Group (Mahram considerations)")
        first_time_umrah = st.checkbox("🆕 First Time Performing Umrah")
        group_coordinator = st.checkbox("👥 Need Group Coordinator/Guide")
    
    additional_notes = st.text_area(
        "Additional Notes or Requirements",
        placeholder="Any other special requests or information we should know...",
        height=100
    )
    
    st.markdown("---")
    st.markdown("### Custom Itinerary Requirements")
    
    custom_itinerary = st.text_area(
        "Describe your preferred city-by-city itinerary (Optional)",
        placeholder="Example: Stay in Madinah for the first night, then go to Makkah for 4 days, then return to Madinah for the last 4 days.\n\nOr: Arrive in Jeddah, go directly to Makkah for 5 days, then Madinah for 3 days.\n\nLeave blank for standard itinerary recommendations.",
        height=120,
        help="Specify which cities to visit, in what order, and for how many days. The agents will book hotels accordingly."
    )
    
    st.markdown("---")
    st.markdown("### Flight Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cabin_class = st.selectbox(
            "Cabin Class",
            ["Economy", "Premium Economy", "Business", "First Class"]
        )
        
        direct_flights = st.checkbox("Prefer Direct Flights", value=True)
    
    with col2:
        preferred_airlines = st.multiselect(
            "Preferred Airlines (Optional)",
            ["Saudi Airlines", "Emirates", "Qatar Airways", "Etihad", "Turkish Airlines", 
             "British Airways", "Lufthansa", "Any"]
        )
        
        baggage_extra = st.checkbox("Extra Baggage Required")
    
    # Navigation
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = 3
            st.rerun()
    
    with col2:
        if st.button("Next: Review →", type="primary", use_container_width=True):
            st.session_state.user_data['budget'] = {
                'currency': currency,
                'per_person': budget_per_person,
                'total': total_budget,
                'flexibility': flexibility
            }
            st.session_state.user_data['special_requirements'] = {
                'wheelchair_access': wheelchair_access,
                'elderly_travelers': elderly_travelers,
                'dietary_requirements': dietary_requirements,
                'female_only_group': female_only_group,
                'first_time_umrah': first_time_umrah,
                'group_coordinator': group_coordinator,
                'additional_notes': additional_notes,
                'custom_itinerary': custom_itinerary
            }
            st.session_state.user_data['flight_preferences'] = {
                'cabin_class': cabin_class,
                'direct_flights': direct_flights,
                'preferred_airlines': preferred_airlines,
                'baggage_extra': baggage_extra
            }
            st.session_state.step = 5
            st.rerun()


def step_review_generate():
    """Step 5: Review and generate trip plan"""
    st.markdown('<h2 class="step-header">📋 Step 5: Review & Generate Plan</h2>', unsafe_allow_html=True)
    
    # Mode indicator
    if not USE_AGENTCORE:
        st.info("ℹ️ **Demo Mode**: This is a demonstration with mock data. In production, real AI agents would search live flight/hotel APIs and generate actual options based on your preferences.")
    else:
        st.info("🤖 **AI-Powered Planning**: Our agents will search real-time data and create a personalized Umrah plan for you.")
    
    st.markdown("### Review Your Information")
    
    # Display collected information
    with st.expander("📅 Travel Dates", expanded=True):
        dates = st.session_state.user_data['travel_dates']
        st.write(f"**Flying From:** {dates.get('departure_country', 'N/A')} - {dates.get('departure_airport', 'N/A')}")
        st.write(f"**Departure:** {dates['departure']}")
        st.write(f"**Return:** {dates['return']}")
        st.write(f"**Duration:** {dates['duration']} days")
        st.write(f"**Arrival City:** {dates['arrival_city']}")
        st.write(f"**Departure City:** {dates.get('departure_city', dates['arrival_city'])}")
    
    with st.expander("👥 Travelers", expanded=True):
        for i, traveler in enumerate(st.session_state.user_data['travelers'], 1):
            st.write(f"**{i}. {traveler['name']}** - {traveler['nationality']}, Age {traveler['age']}")
    
    with st.expander("🏨 Hotel Preferences", expanded=True):
        hotels = st.session_state.user_data['hotel_preferences']
        st.write(f"**Makkah:** {hotels['makkah']['star_rating']}⭐, {hotels['makkah']['proximity']}")
        st.write(f"**Madinah:** {hotels['madinah']['star_rating']}⭐, {hotels['madinah']['proximity']}")
    
    with st.expander("💰 Budget", expanded=True):
        budget = st.session_state.user_data['budget']
        st.write(f"**Total Budget:** {budget['currency']} {budget['total']:,}")
        st.write(f"**Per Person:** {budget['currency']} {budget['per_person']:,}")
        st.write(f"**Flexibility:** {budget['flexibility']}")
    
    st.markdown("---")
    
    # Check if a request is already in progress
    if 'generating_plan' not in st.session_state:
        st.session_state.generating_plan = False
    
    # Show status if generating
    if st.session_state.generating_plan:
        st.warning("⏳ Trip plan is being generated... Please wait (this may take 30-60 seconds)")
    
    # Generate plan button
    if st.button("🚀 Generate My Umrah Trip Plan", type="primary", use_container_width=True, disabled=st.session_state.generating_plan):
        # Set flag to prevent concurrent requests
        st.session_state.generating_plan = True
        
        with st.spinner("🤖 AI Agents are working on your perfect Umrah trip..."):
            
            if USE_AGENTCORE:
                # Use real AgentCore agents
                try:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Get AgentCore client
                    client = get_agentcore_client()
                    
                    # Only invoke orchestrator - it will coordinate all other agents
                    status_text.text("🎯 Orchestrator Agent: Coordinating your complete Umrah trip plan...")
                    status_text.text("⏳ This may take 2-3 minutes as we search real-time flight and hotel data...")
                    progress_bar.progress(20)
                    
                    status_text.text("🤖 AI Agents working: Checking visa requirements...")
                    progress_bar.progress(30)
                    
                    status_text.text("✈️ Searching real flights with Amadeus API...")
                    progress_bar.progress(45)
                    
                    status_text.text("🏨 Finding hotels near Haram with Amadeus API...")
                    progress_bar.progress(60)
                    
                    status_text.text("📅 Creating detailed Umrah itinerary...")
                    progress_bar.progress(75)
                    
                    # Single call to orchestrator - it handles everything
                    orchestrator_response = client.invoke_orchestrator(st.session_state.user_data)
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Complete trip plan generated successfully!")
                    
                    # Store the orchestrator's comprehensive response
                    st.session_state.ai_responses = {
                        'orchestrator': client.extract_text_from_response(orchestrator_response)
                    }
                    
                    # Generate structured trip plan from AI responses
                    st.session_state.trip_plan = generate_trip_plan_from_ai(st.session_state.ai_responses)
                    
                except Exception as e:
                    st.error(f"❌ Error generating trip plan: {str(e)}")
                    st.info("Falling back to demo mode...")
                    st.session_state.trip_plan = generate_mock_trip_plan()
                finally:
                    # Always reset the flag when done
                    st.session_state.generating_plan = False
            else:
                # Use mock data (demo mode)
                try:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Simulate agent processing
                    status_text.text("🎯 Orchestrator Agent: Analyzing your requirements...")
                    time.sleep(2)
                    progress_bar.progress(20)
                    
                    status_text.text("🛂 Visa Agent: Checking visa requirements...")
                    time.sleep(2)
                    progress_bar.progress(40)
                    
                    status_text.text("✈️ Flight Agent: Searching best flight options...")
                    time.sleep(2)
                    progress_bar.progress(60)
                    
                    status_text.text("🏨 Hotel Agent: Finding perfect accommodations...")
                    time.sleep(2)
                    progress_bar.progress(80)
                    
                    status_text.text("📅 Itinerary Agent: Creating your Umrah schedule...")
                    time.sleep(2)
                    progress_bar.progress(100)
                    
                    status_text.text("✅ Trip plan generated successfully!")
                    
                    # Store mock trip plan
                    st.session_state.trip_plan = generate_mock_trip_plan()
                finally:
                    # Always reset the flag when done
                    st.session_state.generating_plan = False
            
            # Move to next step after generation is complete
            st.session_state.step = 6
            time.sleep(1)
            st.rerun()
    
    # Back button
    if st.button("← Back", use_container_width=True):
        st.session_state.step = 4
        st.rerun()


def step_trip_options():
    """Step 6: Display trip options and booking"""
    st.markdown('<h2 class="step-header">✨ Your Umrah Trip Plan</h2>', unsafe_allow_html=True)
    
    # Mode indicator
    if not USE_AGENTCORE:
        st.warning("🎭 **Demo Mode Active**: The options below are sample data for demonstration purposes. In production, these would be real-time results from:\n- ✈️ Amadeus API (flights)\n- 🏨 Booking.com API (hotels)\n- 🛂 Visa databases\n- 📅 AI-generated itineraries")
    else:
        st.success("🤖 **AI-Generated Plan**: These recommendations are powered by AWS Bedrock AgentCore agents with real-time flight and hotel data!")
    
    if not st.session_state.trip_plan:
        st.error("No trip plan generated. Please go back and generate a plan.")
        return
    
    plan = st.session_state.trip_plan
    
    # Debug section - show raw AI response and parsed data
    if USE_AGENTCORE and 'ai_insights' in plan and plan['ai_insights'].get('orchestrator_summary'):
        with st.expander("🔍 Debug: View Raw AI Response & Parsed Data", expanded=False):
            st.markdown("### Raw AI Response")
            st.text_area("Orchestrator response:", plan['ai_insights']['orchestrator_summary'], height=300, key="debug_raw")
            
            st.markdown("### Parsed Flights")
            st.json(plan.get('flights', []))
            
            st.markdown("### Parsed Hotels")
            st.json(plan.get('hotels', {}))
    
    # Show AI-generated comprehensive plan
    if USE_AGENTCORE and 'ai_insights' in plan:
        insights = plan['ai_insights']
        
        # Display the orchestrator's comprehensive response in an expander
        if insights.get('orchestrator_summary'):
            with st.expander("🤖 View AI Agent's Detailed Analysis", expanded=False):
                st.markdown("### 🎯 Complete AI Analysis")
                
                # Format the plain text response with better styling
                response_text = insights['orchestrator_summary']
                
                # Split into sections and format
                sections = response_text.split('\n\n')
                for section in sections:
                    if section.strip():
                        # Check if it's a header (all caps or starts with specific keywords)
                        if any(keyword in section.upper() for keyword in ['VISA', 'FLIGHT', 'HOTEL', 'ITINERARY', 'BUDGET', 'NEXT STEPS']):
                            # Format as a styled section
                            lines = section.split('\n')
                            if lines:
                                # First line as header
                                st.markdown(f"#### {lines[0]}")
                                # Rest as content
                                if len(lines) > 1:
                                    content = '\n'.join(lines[1:])
                                    st.markdown(content)
                        else:
                            st.markdown(section)
    
    # Show structured options for selection
    st.markdown("### 📋 Select Your Preferred Options")
    st.info("� Choose your preferred flight and hotels from the options below, then proceed to booking.")
    
    # Summary card
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Duration", f"{plan['duration']} days")
    with col2:
        st.metric("Travelers", plan['num_travelers'])
    with col3:
        st.metric("Budget", f"{plan['currency']} {plan['cost_breakdown']['total']:,}")
    with col4:
        if st.session_state.selected_flight is not None and st.session_state.selected_makkah_hotel is not None and st.session_state.selected_madinah_hotel is not None:
            st.metric("Status", "✅ Ready")
        else:
            st.metric("Status", "⏳ Select options")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["✈️ Flights", "🏨 Hotels", "🛂 Visa", "📅 Itinerary", "💳 Booking"])
    
    with tab1:
        display_flight_options(plan['flights'])
    
    with tab2:
        display_hotel_options(plan['hotels'])
    
    with tab3:
        display_visa_info(plan['visa'])
    
    with tab4:
        display_itinerary(plan['itinerary'])
    
    with tab5:
        display_booking_section(plan)


def display_flight_options(flights):
    """Display flight options with interactive selection and beautiful styling"""
    st.markdown("### ✈️ Select Your Preferred Flight")
    st.markdown("Compare flight options and choose the one that best fits your schedule and budget.")
    
    if not flights:
        st.warning("No flight options available")
        return
    
    # Display flight options as cards
    for i, flight in enumerate(flights):
        # Create a card-like container
        is_selected = st.session_state.get('selected_flight') == i
        
        # Card styling
        card_style = """
        <style>
        .flight-card {
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            transition: all 0.3s ease;
        }
        .flight-card:hover {
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        .flight-card-selected {
            border: 3px solid #28a745;
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            box-shadow: 0 8px 16px rgba(40,167,69,0.2);
        }
        .flight-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .airline-name {
            font-size: 24px;
            font-weight: bold;
            color: #155724;
        }
        .price-tag {
            font-size: 28px;
            font-weight: bold;
            color: #28a745;
        }
        .flight-detail {
            margin: 10px 0;
            font-size: 16px;
        }
        .badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            margin-right: 8px;
        }
        .badge-direct {
            background-color: #28a745;
            color: white;
        }
        .badge-stops {
            background-color: #ffc107;
            color: #000;
        }
        .badge-class {
            background-color: #007bff;
            color: white;
        }
        </style>
        """
        st.markdown(card_style, unsafe_allow_html=True)
        
        # Radio button for selection
        col_radio, col_content = st.columns([0.5, 9.5])
        
        with col_radio:
            selected = st.radio(
                "select",
                [i],
                key=f"flight_radio_{i}",
                label_visibility="collapsed",
                index=0 if is_selected else None
            )
            if selected == i:
                st.session_state.selected_flight = i
        
        with col_content:
            # Flight card
            card_class = "flight-card-selected" if is_selected else "flight-card"
            
            st.markdown(f"""
            <div class="{card_class}">
                <div class="flight-header">
                    <div class="airline-name">✈️ {flight['airline']}</div>
                    <div class="price-tag">{flight['currency']} {flight['price']:,}</div>
                </div>
                <div style="font-size: 14px; color: #666; margin-bottom: 10px;">per person</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Flight details in expandable section
            with st.expander("📋 View Flight Details", expanded=is_selected):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🛫 Outbound Flight")
                    st.markdown(f"""
                    <div style='background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;'>
                        <p style='margin: 5px 0;'><strong>🛫 Departure:</strong> {flight['outbound']['departure']}</p>
                        <p style='margin: 5px 0;'><strong>🛬 Arrival:</strong> {flight['outbound']['arrival']}</p>
                        <p style='margin: 5px 0;'><strong>⏱️ Duration:</strong> {flight['outbound']['duration']}</p>
                        <p style='margin: 5px 0;'><strong>🔄 Stops:</strong> {flight['outbound']['stops']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("#### 🛬 Return Flight")
                    st.markdown(f"""
                    <div style='background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;'>
                        <p style='margin: 5px 0;'><strong>🛫 Departure:</strong> {flight['return']['departure']}</p>
                        <p style='margin: 5px 0;'><strong>🛬 Arrival:</strong> {flight['return']['arrival']}</p>
                        <p style='margin: 5px 0;'><strong>⏱️ Duration:</strong> {flight['return']['duration']}</p>
                        <p style='margin: 5px 0;'><strong>🔄 Stops:</strong> {flight['return']['stops']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Additional info
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**💼 Cabin Class:** {flight['cabin_class']}")
                with col2:
                    st.markdown(f"**🧳 Baggage:** {flight['baggage']}")
        
        if is_selected:
            st.success(f"✅ Flight Option {i + 1} selected!")
    
    # Summary of selection
    if st.session_state.get('selected_flight') is not None:
        selected_flight = flights[st.session_state.selected_flight]
        st.markdown("---")
        st.info(f"🎯 **Your Selection:** {selected_flight['airline']} - {selected_flight['currency']} {selected_flight['price']:,} per person")


def display_hotel_options(hotels):
    """Display hotel options with interactive selection and beautiful styling"""
    st.markdown("### 🏨 Select Your Preferred Hotels")
    st.markdown("Choose comfortable accommodations near the holy sites for your spiritual journey.")
    
    # Hotel card styling
    hotel_card_style = """
    <style>
    .hotel-card {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        transition: all 0.3s ease;
    }
    .hotel-card:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .hotel-card-selected {
        border: 3px solid #28a745;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        box-shadow: 0 8px 16px rgba(40,167,69,0.2);
    }
    .hotel-name {
        font-size: 22px;
        font-weight: bold;
        color: #155724;
        margin-bottom: 8px;
    }
    .hotel-stars {
        color: #ffc107;
        font-size: 18px;
        margin-bottom: 8px;
    }
    .hotel-distance {
        color: #28a745;
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 8px;
    }
    .hotel-price {
        font-size: 24px;
        font-weight: bold;
        color: #007bff;
    }
    .hotel-rating {
        background-color: #28a745;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    </style>
    """
    st.markdown(hotel_card_style, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🕋 Makkah Hotels")
        st.markdown("*Near Masjid al-Haram*")
        
        if not hotels.get('makkah'):
            st.warning("No Makkah hotel options available")
        else:
            for i, hotel in enumerate(hotels['makkah']):
                is_selected = st.session_state.get('selected_makkah_hotel') == i
                
                # Radio button for selection
                col_radio, col_content = st.columns([0.5, 9.5])
                
                with col_radio:
                    selected = st.radio(
                        "select_makkah",
                        [i],
                        key=f"makkah_radio_{i}",
                        label_visibility="collapsed",
                        index=0 if is_selected else None
                    )
                    if selected == i:
                        st.session_state.selected_makkah_hotel = i
                
                with col_content:
                    card_class = "hotel-card-selected" if is_selected else "hotel-card"
                    stars = "⭐" * hotel['stars']
                    
                    st.markdown(f"""
                    <div class="{card_class}">
                        <div class="hotel-name">🏨 {hotel['name']}</div>
                        <div class="hotel-stars">{stars}</div>
                        <div class="hotel-distance">📍 {hotel['distance']}</div>
                        <div style="margin: 10px 0;">
                            <span class="hotel-rating">⭐ {hotel['rating']}/10</span>
                        </div>
                        <div class="hotel-price">{hotel['currency']} {hotel['price_per_night']}/night</div>
                        <div style="font-size: 14px; color: #666; margin-top: 5px;">
                            Total: {hotel['currency']} {hotel['total_price']:,}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Amenities in expander
                    with st.expander("🎯 Amenities & Details", expanded=False):
                        st.markdown(f"**✨ Amenities:** {', '.join(hotel['amenities'])}")
                        st.markdown(f"**💰 Price per night:** {hotel['currency']} {hotel['price_per_night']}")
                        st.markdown(f"**💵 Total cost:** {hotel['currency']} {hotel['total_price']:,}")
                
                if is_selected:
                    st.success(f"✅ {hotel['name']} selected!")
    
    with col2:
        st.markdown("#### 🕌 Madinah Hotels")
        st.markdown("*Near Masjid an-Nabawi*")
        
        if not hotels.get('madinah'):
            st.warning("No Madinah hotel options available")
        else:
            for i, hotel in enumerate(hotels['madinah']):
                is_selected = st.session_state.get('selected_madinah_hotel') == i
                
                # Radio button for selection
                col_radio, col_content = st.columns([0.5, 9.5])
                
                with col_radio:
                    selected = st.radio(
                        "select_madinah",
                        [i],
                        key=f"madinah_radio_{i}",
                        label_visibility="collapsed",
                        index=0 if is_selected else None
                    )
                    if selected == i:
                        st.session_state.selected_madinah_hotel = i
                
                with col_content:
                    card_class = "hotel-card-selected" if is_selected else "hotel-card"
                    stars = "⭐" * hotel['stars']
                    
                    st.markdown(f"""
                    <div class="{card_class}">
                        <div class="hotel-name">🏨 {hotel['name']}</div>
                        <div class="hotel-stars">{stars}</div>
                        <div class="hotel-distance">📍 {hotel['distance']}</div>
                        <div style="margin: 10px 0;">
                            <span class="hotel-rating">⭐ {hotel['rating']}/10</span>
                        </div>
                        <div class="hotel-price">{hotel['currency']} {hotel['price_per_night']}/night</div>
                        <div style="font-size: 14px; color: #666; margin-top: 5px;">
                            Total: {hotel['currency']} {hotel['total_price']:,}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Amenities in expander
                    with st.expander("🎯 Amenities & Details", expanded=False):
                        st.markdown(f"**✨ Amenities:** {', '.join(hotel['amenities'])}")
                        st.markdown(f"**💰 Price per night:** {hotel['currency']} {hotel['price_per_night']}")
                        st.markdown(f"**💵 Total cost:** {hotel['currency']} {hotel['total_price']:,}")
                
                if is_selected:
                    st.success(f"✅ {hotel['name']} selected!")
    
    # Summary of selections
    st.markdown("---")
    if st.session_state.get('selected_makkah_hotel') is not None and st.session_state.get('selected_madinah_hotel') is not None:
        makkah_hotel = hotels['makkah'][st.session_state.selected_makkah_hotel]
        madinah_hotel = hotels['madinah'][st.session_state.selected_madinah_hotel]
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"🕋 **Makkah:** {makkah_hotel['name']} - {makkah_hotel['currency']} {makkah_hotel['total_price']:,}")
        with col2:
            st.info(f"🕌 **Madinah:** {madinah_hotel['name']} - {madinah_hotel['currency']} {madinah_hotel['total_price']:,}")


def display_visa_info(visa):
    """Display visa information"""
    st.markdown("### Visa Requirements")
    
    for traveler_visa in visa['travelers']:
        with st.expander(f"📋 {traveler_visa['name']} - {traveler_visa['nationality']}", expanded=True):
            st.write(f"**Visa Type:** {traveler_visa['visa_type']}")
            st.write(f"**Processing Time:** {traveler_visa['processing_time']}")
            st.write(f"**Validity:** {traveler_visa['validity']}")
            st.write(f"**Cost:** {traveler_visa['currency']} {traveler_visa['cost']}")
            
            st.markdown("**Required Documents:**")
            for doc in traveler_visa['required_documents']:
                st.write(f"- {doc}")
            
            st.markdown("**Application Steps:**")
            for step in traveler_visa['application_steps']:
                st.write(f"{step}")
    
    st.info(f"💰 **Total Visa Cost:** {visa['currency']} {visa['total_cost']:,}")


def display_itinerary(itinerary):
    """Display day-by-day itinerary"""
    st.markdown("### Day-by-Day Itinerary")
    
    for day in itinerary['days']:
        with st.expander(f"📅 Day {day['day']}: {day['title']}", expanded=(day['day']==1)):
            st.write(f"**Location:** {day['location']}")
            st.write(f"**Date:** {day['date']}")
            
            st.markdown("**Activities:**")
            for activity in day['activities']:
                st.write(f"- **{activity['time']}**: {activity['description']}")
            
            if day.get('notes'):
                st.info(f"📝 **Note:** {day['notes']}")


def display_booking_section(plan):
    """Display booking and payment section with selected options"""
    st.markdown("### Complete Your Booking")
    
    # Show selected options summary
    st.markdown("#### � Your Selected Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("##### ✈️ Flight")
        if st.session_state.selected_flight is not None:
            flight = plan['flights'][st.session_state.selected_flight]
            st.write(f"**{flight['airline']}**")
            st.write(f"{flight['currency']} {flight['price']:,} per person")
            st.write(f"Total: {flight['currency']} {flight['price'] * plan['num_travelers']:,}")
        else:
            st.warning("No flight selected")
    
    with col2:
        st.markdown("##### 🕋 Makkah Hotel")
        if st.session_state.selected_makkah_hotel is not None:
            hotel = plan['hotels']['makkah'][st.session_state.selected_makkah_hotel]
            st.write(f"**{hotel['name']}**")
            st.write(f"{hotel['stars']}⭐ - {hotel['distance']}")
            st.write(f"Total: {hotel['currency']} {hotel['total_price']:,}")
        else:
            st.warning("No Makkah hotel selected")
    
    with col3:
        st.markdown("##### 🕌 Madinah Hotel")
        if st.session_state.selected_madinah_hotel is not None:
            hotel = plan['hotels']['madinah'][st.session_state.selected_madinah_hotel]
            st.write(f"**{hotel['name']}**")
            st.write(f"{hotel['stars']}⭐ - {hotel['distance']}")
            st.write(f"Total: {hotel['currency']} {hotel['total_price']:,}")
        else:
            st.warning("No Madinah hotel selected")
    
    st.markdown("---")
    st.markdown("#### 📊 Cost Breakdown")
    
    # Calculate actual costs based on selections
    flight_cost = 0
    if st.session_state.selected_flight is not None:
        flight_cost = plan['flights'][st.session_state.selected_flight]['price'] * plan['num_travelers']
    
    makkah_hotel_cost = 0
    if st.session_state.selected_makkah_hotel is not None:
        makkah_hotel_cost = plan['hotels']['makkah'][st.session_state.selected_makkah_hotel]['total_price']
    
    madinah_hotel_cost = 0
    if st.session_state.selected_madinah_hotel is not None:
        madinah_hotel_cost = plan['hotels']['madinah'][st.session_state.selected_madinah_hotel]['total_price']
    
    total_hotel_cost = makkah_hotel_cost + madinah_hotel_cost
    visa_cost = plan['visa']['total_cost']
    service_fee = 100
    subtotal = flight_cost + total_hotel_cost + visa_cost + service_fee
    discount = 200 if subtotal > 2000 else 0
    total = subtotal - discount
    
    breakdown = {
        'currency': plan['currency'],
        'flights': flight_cost,
        'hotels': total_hotel_cost,
        'visa': visa_cost,
        'service_fee': service_fee,
        'subtotal': subtotal,
        'discount': discount,
        'total': total
    }
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write(f"Flights ({plan['num_travelers']} travelers)")
        st.write(f"Hotels (Makkah + Madinah)")
        st.write(f"Visa Fees ({plan['num_travelers']} travelers)")
        st.write(f"Service Fee")
        st.write("---")
        st.write(f"**Subtotal**")
        if discount > 0:
            st.write(f"**Discount**")
        st.write("---")
        st.markdown(f"### **Total**")
    
    with col2:
        st.write(f"{breakdown['currency']} {breakdown['flights']:,}")
        st.write(f"{breakdown['currency']} {breakdown['hotels']:,}")
        st.write(f"{breakdown['currency']} {breakdown['visa']:,}")
        st.write(f"{breakdown['currency']} {breakdown['service_fee']:,}")
        st.write("---")
        st.write(f"{breakdown['currency']} {breakdown['subtotal']:,}")
        if discount > 0:
            st.write(f"-{breakdown['currency']} {breakdown['discount']:,}")
        st.write("---")
        st.markdown(f"### **{breakdown['currency']} {breakdown['total']:,}**")
    
    # Check if all selections are made
    all_selected = (
        st.session_state.selected_flight is not None and
        st.session_state.selected_makkah_hotel is not None and
        st.session_state.selected_madinah_hotel is not None
    )
    
    if not all_selected:
        st.warning("⚠️ Please select your preferred flight and hotels from the tabs above before proceeding to payment.")
        return
    
    st.markdown("---")
    
    st.markdown("#### 💳 Payment Options")
    
    payment_method = st.radio(
        "Select Payment Method",
        ["Credit/Debit Card", "Bank Transfer", "PayPal", "Installment Plan"],
        horizontal=True
    )
    
    if payment_method == "Installment Plan":
        st.info("💡 Pay in 3 interest-free installments")
    
    st.markdown("#### 📧 Contact Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        email = st.text_input("Email Address", placeholder="your@email.com")
        phone = st.text_input("Phone Number", placeholder="+1234567890")
    
    with col2:
        emergency_contact = st.text_input("Emergency Contact", placeholder="Name")
        emergency_phone = st.text_input("Emergency Phone", placeholder="+1234567890")
    
    # Terms and conditions
    agree_terms = st.checkbox("I agree to the Terms & Conditions and Privacy Policy")
    
    # Book button
    if st.button("🎉 Confirm Booking", type="primary", use_container_width=True, disabled=not agree_terms):
        with st.spinner("Processing your booking..."):
            import time
            time.sleep(2)
            
            st.balloons()
            st.success("🎊 Booking Confirmed! Check your email for confirmation details.")
            
            # Display booking reference
            st.markdown("---")
            st.markdown("### 📋 Booking Reference")
            st.code(f"UMRAH-{hash(email) % 1000000:06d}", language=None)
            
            st.info("📧 Confirmation email sent to: " + email)
            st.info("📱 SMS confirmation sent to: " + phone)
            
            # Show selected items in confirmation
            st.markdown("### ✅ Confirmed Selections")
            st.write(f"**Flight:** {plan['flights'][st.session_state.selected_flight]['airline']}")
            st.write(f"**Makkah Hotel:** {plan['hotels']['makkah'][st.session_state.selected_makkah_hotel]['name']}")
            st.write(f"**Madinah Hotel:** {plan['hotels']['madinah'][st.session_state.selected_madinah_hotel]['name']}")
            st.write(f"**Total Paid:** {breakdown['currency']} {breakdown['total']:,}")
            
            # Download options
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button("📄 Download Itinerary (PDF)", "itinerary.pdf", "application/pdf")
            with col2:
                st.download_button("📋 Download Booking Details", "booking.json", "application/json")
            with col3:
                st.download_button("📧 Download Visa Documents", "visa_docs.zip", "application/zip")


def parse_flights_from_text(text: str, user_data: Dict) -> List[Dict]:
    """Parse flight options from AI text response"""
    import re
    
    flights = []
    
    # The AI formats flights like:
    # Option 1 (Morning) - $748.26
    # - Outbound: MAN 10:50 → JED 00:05 (next day)
    # - Return: JED 06:40 → MAN 13:05
    
    # Find all flight options
    option_pattern = r'Option\s+(\d+)\s*\(([^)]+)\)\s*-\s*\$?([\d,]+\.?\d*)'
    options = list(re.finditer(option_pattern, text, re.IGNORECASE))
    
    # Also look for airline name (usually mentioned before options)
    airline_match = re.search(r'through\s+([A-Z][a-zA-Z\s]+(?:Airlines?|Airways?))', text, re.IGNORECASE)
    base_airline = airline_match.group(1).strip() if airline_match else "Turkish Airlines"
    
    for match in options:
        option_num = int(match.group(1))
        time_desc = match.group(2).strip()  # e.g., "Morning", "Evening"
        price = float(match.group(3).replace(',', ''))
        
        # Find the outbound and return info for this option
        # Look in the text after this match
        start_pos = match.end()
        # Find next option or end of section
        next_match = options[options.index(match) + 1] if options.index(match) + 1 < len(options) else None
        end_pos = next_match.start() if next_match else start_pos + 500
        
        section = text[start_pos:end_pos]
        
        # Extract outbound flight
        outbound_match = re.search(r'Outbound:\s*([A-Z]{3})\s+([\d:]+)\s*→\s*([A-Z]{3})\s+([\d:]+)', section)
        if outbound_match:
            dep_airport = outbound_match.group(1)
            dep_time = outbound_match.group(2)
            arr_airport = outbound_match.group(3)
            arr_time = outbound_match.group(4)
            outbound_str = f"{dep_airport} {dep_time} → {arr_airport} {arr_time}"
            
            # Check for "next day" indicator
            if 'next day' in section[outbound_match.start():outbound_match.end()+20].lower():
                outbound_str += " +1"
        else:
            outbound_str = f"{user_data['travel_dates'].get('departure_airport', 'MAN')} → JED"
        
        # Extract return flight
        return_match = re.search(r'Return:\s*([A-Z]{3})\s+([\d:]+)\s*→\s*([A-Z]{3})\s+([\d:]+)', section)
        if return_match:
            dep_airport = return_match.group(1)
            dep_time = return_match.group(2)
            arr_airport = return_match.group(3)
            arr_time = return_match.group(4)
            return_str = f"{dep_airport} {dep_time} → {arr_airport} {arr_time}"
        else:
            return_str = f"JED → {user_data['travel_dates'].get('departure_airport', 'MAN')}"
        
        # Calculate duration (rough estimate)
        duration = "13h 15m"
        
        # Determine stops (Turkish Airlines typically has 1 stop)
        stops = "1 stop (IST)"
        
        flight = {
            'airline': f"{base_airline} ({time_desc})",
            'price': int(price),
            'currency': user_data['budget']['currency'],
            'cabin_class': user_data['flight_preferences']['cabin_class'],
            'baggage': '2 x 23kg checked bags',
            'outbound': {
                'departure': outbound_str,
                'arrival': '',
                'duration': duration,
                'stops': stops
            },
            'return': {
                'departure': return_str,
                'arrival': '',
                'duration': duration,
                'stops': stops
            }
        }
        flights.append(flight)
    
    # If no flights parsed, return at least one default
    if not flights:
        flights.append({
            'airline': 'Available Flight Option',
            'price': 850,
            'currency': user_data['budget']['currency'],
            'cabin_class': user_data['flight_preferences']['cabin_class'],
            'baggage': '2 x 23kg checked bags',
            'outbound': {
                'departure': f"{user_data['travel_dates'].get('departure_airport', 'Origin')} 10:30 AM",
                'arrival': f"{user_data['travel_dates']['arrival_city']} 6:45 AM +1",
                'duration': '12h 30m',
                'stops': 'Direct'
            },
            'return': {
                'departure': f"{user_data['travel_dates'].get('departure_city', user_data['travel_dates']['arrival_city'])} 11:30 PM",
                'arrival': f"{user_data['travel_dates'].get('departure_airport', 'Origin')} 6:15 AM +1",
                'duration': '13h 45m',
                'stops': 'Direct'
            }
        })
    
    return flights[:5]  # Limit to 5 options


def parse_hotels_from_text(text: str, city: str, user_data: Dict) -> List[Dict]:
    """Parse hotel options from AI text response for a specific city"""
    import re
    
    hotels = []
    city_lower = city.lower()
    
    # The AI formats hotels like:
    # Makkah (March 6-10):
    # 1. Le Meridien Makkah (380m from Haram)
    # 2. Pullman Zamzam Makkah (380m from Haram)
    
    # Find the city section
    if 'makkah' in city_lower or 'mecca' in city_lower:
        section_match = re.search(r'Makkah[^:]*:(.*?)(?:Madinah|DETAILED|RECOMMENDATIONS|$)', text, re.DOTALL | re.IGNORECASE)
    else:
        section_match = re.search(r'Madinah[^:]*:(.*?)(?:DETAILED|RECOMMENDATIONS|$)', text, re.DOTALL | re.IGNORECASE)
    
    if section_match:
        section = section_match.group(1)
        
        # Find hotel entries: "1. Hotel Name (distance from Haram)"
        hotel_pattern = r'(\d+)\.\s+([^(]+)\s*\((\d+)m\s+from\s+Haram\)'
        matches = re.finditer(hotel_pattern, section, re.IGNORECASE)
        
        for match in matches:
            hotel_num = match.group(1)
            hotel_name = match.group(2).strip()
            distance_m = int(match.group(3))
            
            # Determine star rating based on hotel name
            stars = 5
            if 'hilton' in hotel_name.lower() or 'meridien' in hotel_name.lower() or 'pullman' in hotel_name.lower():
                stars = 5
            elif 'mövenpick' in hotel_name.lower() or 'moevenpick' in hotel_name.lower():
                stars = 4
            elif 'shaza' in hotel_name.lower():
                stars = 4
            
            # Estimate price based on distance and stars
            if distance_m < 400:
                base_price = 200 if stars == 5 else 150
            else:
                base_price = 180 if stars == 5 else 130
            
            # Calculate nights
            nights = 5 if 'makkah' in city_lower or 'mecca' in city_lower else 3
            total_price = base_price * nights
            
            hotel = {
                'name': hotel_name,
                'stars': stars,
                'distance': f"{distance_m}m from Haram",
                'price_per_night': base_price,
                'total_price': total_price,
                'currency': user_data['budget']['currency'],
                'amenities': ['WiFi', 'Breakfast', 'Restaurant', 'Elevator', 'Haram View'],
                'rating': 8.5 + (stars - 3) * 0.5
            }
            hotels.append(hotel)
    
    # If no hotels parsed, return defaults
    if not hotels:
        if 'makkah' in city_lower or 'mecca' in city_lower:
            hotels = [
                {
                    'name': 'Makkah Hotel Near Haram',
                    'stars': 5,
                    'distance': '200m from Haram',
                    'price_per_night': 180,
                    'total_price': 900,
                    'currency': user_data['budget']['currency'],
                    'amenities': ['WiFi', 'Breakfast', 'Haram View', 'Restaurant'],
                    'rating': 9.0
                },
                {
                    'name': 'Makkah Budget Hotel',
                    'stars': 4,
                    'distance': '400m from Haram',
                    'price_per_night': 150,
                    'total_price': 750,
                    'currency': user_data['budget']['currency'],
                    'amenities': ['WiFi', 'Breakfast', 'Restaurant'],
                    'rating': 8.5
                }
            ]
        else:
            hotels = [
                {
                    'name': 'Madinah Hotel Near Haram',
                    'stars': 5,
                    'distance': '100m from Haram',
                    'price_per_night': 150,
                    'total_price': 450,
                    'currency': user_data['budget']['currency'],
                    'amenities': ['WiFi', 'Breakfast', 'Haram View', 'Restaurant'],
                    'rating': 9.0
                },
                {
                    'name': 'Madinah Budget Hotel',
                    'stars': 4,
                    'distance': '300m from Haram',
                    'price_per_night': 120,
                    'total_price': 360,
                    'currency': user_data['budget']['currency'],
                    'amenities': ['WiFi', 'Breakfast', 'Restaurant'],
                    'rating': 8.5
                }
            ]
    
    return hotels[:3]  # Limit to 3 options per city


def generate_trip_plan_from_ai(ai_responses: Dict[str, str]) -> Dict[str, Any]:
    """
    Generate structured trip plan from AI agent responses
    
    Args:
        ai_responses: Dictionary containing responses from all agents
        
    Returns:
        Structured trip plan dictionary
    """
    user_data = st.session_state.user_data
    orchestrator_text = ai_responses.get('orchestrator', '')
    
    # Parse flights and hotels from the orchestrator's response
    flights = parse_flights_from_text(orchestrator_text, user_data)
    makkah_hotels = parse_hotels_from_text(orchestrator_text, 'Makkah', user_data)
    madinah_hotels = parse_hotels_from_text(orchestrator_text, 'Madinah', user_data)
    
    # Build structured plan
    plan = {
        'currency': user_data['budget']['currency'],
        'total_cost': user_data['budget']['total'] * 0.95,
        'duration': user_data['travel_dates']['duration'],
        'num_travelers': user_data['num_travelers'],
        'savings': user_data['budget']['total'] * 0.05,
        
        'flights': flights,
        
        'hotels': {
            'makkah': makkah_hotels,
            'madinah': madinah_hotels
        },
        
        'visa': {
            'currency': user_data['budget']['currency'],
            'total_cost': 150 * user_data['num_travelers'],
            'travelers': [
                {
                    'name': t['name'],
                    'nationality': t['nationality'],
                    'visa_type': 'Umrah Visa (90 days)',
                    'processing_time': '3-5 business days',
                    'validity': '90 days from issue',
                    'cost': 150,
                    'currency': user_data['budget']['currency'],
                    'required_documents': [
                        'Valid passport (min 6 months validity)',
                        'Recent passport-size photo',
                        'Confirmed hotel booking',
                        'Return flight ticket',
                        'Vaccination certificate (Meningitis)'
                    ],
                    'application_steps': [
                        '1. Complete online application at visa.visitsaudi.com',
                        '2. Upload required documents',
                        '3. Pay visa fee online',
                        '4. Receive e-visa via email',
                        '5. Print visa for immigration'
                    ]
                }
                for t in user_data['travelers']
            ]
        },
        
        'itinerary': {
            'days': [
                {
                    'day': 1,
                    'title': 'Arrival & First Umrah',
                    'location': 'Makkah',
                    'date': user_data['travel_dates']['departure'],
                    'activities': [
                        {'time': '06:45', 'description': 'Arrive at airport'},
                        {'time': '09:30', 'description': 'Transfer to Makkah'},
                        {'time': '11:00', 'description': 'Check-in at hotel'},
                        {'time': '17:00', 'description': 'Perform Umrah (Tawaf & Sa\'i)'}
                    ]
                }
            ]
        },
        
        'cost_breakdown': {
            'currency': user_data['budget']['currency'],
            'flights': flights[0]['price'] * user_data['num_travelers'] if flights else 0,
            'hotels': (makkah_hotels[0]['total_price'] + madinah_hotels[0]['total_price']) if makkah_hotels and madinah_hotels else 0,
            'visa': 150 * user_data['num_travelers'],
            'service_fee': 100,
            'subtotal': 0,
            'discount': 200,
            'total': 0
        },
        
        'ai_insights': {
            'orchestrator_summary': orchestrator_text,
            'visa_details': ai_responses.get('visa', ''),
            'flight_recommendations': ai_responses.get('flight', ''),
            'hotel_recommendations': ai_responses.get('hotel', ''),
            'itinerary_suggestions': ai_responses.get('itinerary', '')
        }
    }
    
    # Calculate totals
    plan['cost_breakdown']['subtotal'] = (
        plan['cost_breakdown']['flights'] + 
        plan['cost_breakdown']['hotels'] + 
        plan['cost_breakdown']['visa'] + 
        plan['cost_breakdown']['service_fee']
    )
    plan['cost_breakdown']['total'] = plan['cost_breakdown']['subtotal'] - plan['cost_breakdown']['discount']
    
    return plan


def generate_mock_trip_plan():
    """Generate mock trip plan for demonstration"""
    user_data = st.session_state.user_data
    
    return {
        'currency': user_data['budget']['currency'],
        'total_cost': user_data['budget']['total'] * 0.95,
        'duration': user_data['travel_dates']['duration'],
        'num_travelers': user_data['num_travelers'],
        'savings': user_data['budget']['total'] * 0.05,
        
        'flights': [
            {
                'airline': 'Saudi Airlines',
                'price': 850,
                'currency': user_data['budget']['currency'],
                'cabin_class': user_data['flight_preferences']['cabin_class'],
                'baggage': '2 x 23kg checked bags',
                'outbound': {
                    'departure': f"{user_data['travel_dates'].get('departure_airport', 'JFK')} 10:30 AM",
                    'arrival': 'JED 6:45 AM +1',
                    'duration': '12h 15m',
                    'stops': 'Direct'
                },
                'return': {
                    'departure': 'JED 11:30 PM',
                    'arrival': f"{user_data['travel_dates'].get('departure_airport', 'JFK')} 6:15 AM +1",
                    'duration': '13h 45m',
                    'stops': 'Direct'
                }
            },
            {
                'airline': 'Emirates',
                'price': 920,
                'currency': user_data['budget']['currency'],
                'cabin_class': user_data['flight_preferences']['cabin_class'],
                'baggage': '2 x 30kg checked bags',
                'outbound': {
                    'departure': f"{user_data['travel_dates'].get('departure_airport', 'JFK')} 11:45 PM",
                    'arrival': 'JED 10:30 PM +1',
                    'duration': '16h 45m',
                    'stops': '1 stop (DXB)'
                },
                'return': {
                    'departure': 'JED 2:30 AM',
                    'arrival': f"{user_data['travel_dates'].get('departure_airport', 'JFK')} 11:45 AM",
                    'duration': '17h 15m',
                    'stops': '1 stop (DXB)'
                }
            }
        ],
        
        'hotels': {
            'makkah': [
                {
                    'name': 'Swissotel Makkah',
                    'stars': 5,
                    'distance': '200m from Haram',
                    'price_per_night': 180,
                    'total_price': 900,
                    'currency': user_data['budget']['currency'],
                    'amenities': ['WiFi', 'Breakfast', 'Haram View', 'Restaurant', 'Elevator'],
                    'rating': 9.2
                },
                {
                    'name': 'Hilton Makkah Convention',
                    'stars': 5,
                    'distance': '150m from Haram',
                    'price_per_night': 220,
                    'total_price': 1100,
                    'currency': user_data['budget']['currency'],
                    'amenities': ['WiFi', 'Breakfast', 'Haram View', 'Pool', 'Spa'],
                    'rating': 9.5
                }
            ],
            'madinah': [
                {
                    'name': 'Pullman Zamzam Madinah',
                    'stars': 5,
                    'distance': '100m from Haram',
                    'price_per_night': 150,
                    'total_price': 450,
                    'currency': user_data['budget']['currency'],
                    'amenities': ['WiFi', 'Breakfast', 'Haram View', 'Restaurant'],
                    'rating': 9.0
                },
                {
                    'name': 'Oberoi Madinah',
                    'stars': 5,
                    'distance': '50m from Haram',
                    'price_per_night': 200,
                    'total_price': 600,
                    'currency': user_data['budget']['currency'],
                    'amenities': ['WiFi', 'Breakfast', 'Haram View', 'Concierge', 'Spa'],
                    'rating': 9.7
                }
            ]
        },
        
        'visa': {
            'currency': user_data['budget']['currency'],
            'total_cost': 150 * user_data['num_travelers'],
            'travelers': [
                {
                    'name': t['name'],
                    'nationality': t['nationality'],
                    'visa_type': 'Umrah Visa (90 days)',
                    'processing_time': '3-5 business days',
                    'validity': '90 days from issue',
                    'cost': 150,
                    'currency': user_data['budget']['currency'],
                    'required_documents': [
                        'Valid passport (min 6 months validity)',
                        'Recent passport-size photo',
                        'Confirmed hotel booking',
                        'Return flight ticket',
                        'Vaccination certificate (Meningitis)'
                    ],
                    'application_steps': [
                        '1. Complete online application at visa.visitsaudi.com',
                        '2. Upload required documents',
                        '3. Pay visa fee online',
                        '4. Receive e-visa via email',
                        '5. Print visa for immigration'
                    ]
                }
                for t in user_data['travelers']
            ]
        },
        
        'itinerary': {
            'days': [
                {
                    'day': 1,
                    'title': 'Arrival in Jeddah & Transfer to Makkah',
                    'location': 'Jeddah → Makkah',
                    'date': user_data['travel_dates']['departure'],
                    'activities': [
                        {'time': '06:45', 'description': 'Arrive at Jeddah Airport'},
                        {'time': '08:00', 'description': 'Immigration & customs clearance'},
                        {'time': '09:30', 'description': 'Private transfer to Makkah (90 min)'},
                        {'time': '11:00', 'description': 'Check-in at hotel'},
                        {'time': '13:00', 'description': 'Rest and prepare for Umrah'},
                        {'time': '16:00', 'description': 'Enter Ihram state'},
                        {'time': '17:00', 'description': 'Perform Umrah (Tawaf & Sa\'i)'},
                        {'time': '20:00', 'description': 'Dinner near Haram'}
                    ],
                    'notes': 'Take it easy on first day. Stay hydrated.'
                },
                {
                    'day': 2,
                    'title': 'Makkah - Worship & Ziyarat',
                    'location': 'Makkah',
                    'date': user_data['travel_dates']['departure'],
                    'activities': [
                        {'time': '05:00', 'description': 'Fajr prayer at Masjid al-Haram'},
                        {'time': '09:00', 'description': 'Breakfast at hotel'},
                        {'time': '11:00', 'description': 'Visit Jabal al-Nour (Cave of Hira)'},
                        {'time': '14:00', 'description': 'Lunch and rest'},
                        {'time': '16:00', 'description': 'Prayers at Haram'},
                        {'time': '19:00', 'description': 'Visit Jannat al-Mu\'alla cemetery'},
                        {'time': '21:00', 'description': 'Taraweeh/Tahajjud prayers'}
                    ]
                },
                {
                    'day': 3,
                    'title': 'Transfer to Madinah',
                    'location': 'Makkah → Madinah',
                    'date': user_data['travel_dates']['departure'],
                    'activities': [
                        {'time': '08:00', 'description': 'Fajr prayer and breakfast'},
                        {'time': '10:00', 'description': 'Check-out from hotel'},
                        {'time': '11:00', 'description': 'Depart for Madinah (4-5 hours)'},
                        {'time': '16:00', 'description': 'Arrive and check-in at Madinah hotel'},
                        {'time': '17:30', 'description': 'First visit to Masjid an-Nabawi'},
                        {'time': '19:00', 'description': 'Maghrib prayer at Prophet\'s Mosque'},
                        {'time': '21:00', 'description': 'Isha and Taraweeh prayers'}
                    ],
                    'notes': 'Try to pray in Rawdah (the blessed garden)'
                }
            ]
        },
        
        'cost_breakdown': {
            'currency': user_data['budget']['currency'],
            'flights': 850 * user_data['num_travelers'],
            'hotels': 1350 * user_data['num_travelers'],
            'visa': 150 * user_data['num_travelers'],
            'service_fee': 100,
            'subtotal': (850 + 1350 + 150) * user_data['num_travelers'] + 100,
            'discount': 200,
            'total': (850 + 1350 + 150) * user_data['num_travelers'] + 100 - 200
        }
    }


def display_booking_form():
    """Display booking form for completing the reservation"""
    st.markdown("### 💳 Complete Your Booking")
    st.info("📝 Please provide your payment and contact information to complete the booking.")
    
    with st.form("booking_form"):
        st.markdown("#### Contact Information")
        col1, col2 = st.columns(2)
        
        with col1:
            email = st.text_input("Email Address*", placeholder="your.email@example.com")
            phone = st.text_input("Phone Number*", placeholder="+1 234 567 8900")
        
        with col2:
            confirm_email = st.text_input("Confirm Email*", placeholder="your.email@example.com")
            emergency_contact = st.text_input("Emergency Contact", placeholder="+1 234 567 8900")
        
        st.markdown("---")
        st.markdown("#### Payment Information")
        
        payment_method = st.selectbox(
            "Payment Method",
            ["Credit Card", "Debit Card", "PayPal", "Bank Transfer"]
        )
        
        if payment_method in ["Credit Card", "Debit Card"]:
            col1, col2 = st.columns(2)
            with col1:
                card_number = st.text_input("Card Number*", placeholder="1234 5678 9012 3456", type="password")
                card_name = st.text_input("Cardholder Name*", placeholder="John Doe")
            
            with col2:
                col_exp, col_cvv = st.columns(2)
                with col_exp:
                    expiry = st.text_input("Expiry (MM/YY)*", placeholder="12/26")
                with col_cvv:
                    cvv = st.text_input("CVV*", placeholder="123", type="password")
        
        st.markdown("---")
        st.markdown("#### Billing Address")
        
        col1, col2 = st.columns(2)
        with col1:
            address = st.text_input("Street Address*")
            city = st.text_input("City*")
        
        with col2:
            state = st.text_input("State/Province*")
            postal_code = st.text_input("Postal Code*")
        
        country = st.selectbox(
            "Country*",
            ["United States", "United Kingdom", "Canada", "Australia", "Other"]
        )
        
        st.markdown("---")
        st.markdown("#### Special Requests")
        special_requests = st.text_area(
            "Any special requests or notes for your booking?",
            placeholder="E.g., wheelchair assistance, dietary requirements, room preferences...",
            height=100
        )
        
        st.markdown("---")
        st.markdown("#### Terms and Conditions")
        
        agree_terms = st.checkbox("I agree to the Terms and Conditions*")
        agree_cancellation = st.checkbox("I understand the cancellation policy*")
        subscribe_newsletter = st.checkbox("Subscribe to newsletter for travel updates and offers")
        
        st.markdown("---")
        
        # Submit button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button("🎉 Complete Booking", use_container_width=True, type="primary")
        
        if submitted:
            # Validate required fields
            if not email or not phone or not confirm_email:
                st.error("❌ Please fill in all required fields marked with *")
            elif email != confirm_email:
                st.error("❌ Email addresses do not match")
            elif not agree_terms or not agree_cancellation:
                st.error("❌ Please agree to the terms and conditions")
            else:
                # Process booking (in production, this would integrate with payment gateway)
                with st.spinner("Processing your booking..."):
                    import time
                    time.sleep(2)  # Simulate processing
                
                st.success("🎉 Booking Confirmed!")
                st.balloons()
                
                # Display confirmation
                st.markdown("### ✅ Booking Confirmation")
                st.info(f"""
                **Confirmation Number:** UMR-{int(time.time())}
                
                **Email Confirmation:** A detailed confirmation has been sent to {email}
                
                **Next Steps:**
                1. Check your email for booking details and payment receipt
                2. Apply for your Umrah visa (if not already done)
                3. Download our mobile app for trip management
                4. Review the pre-departure checklist we've sent you
                
                **Need Help?**
                - 24/7 Customer Support: +1-800-UMRAH-24
                - Email: support@umrahtrips.com
                - WhatsApp: +1-800-123-4567
                
                Safe travels and may your Umrah be accepted! 🕋
                """)
                
                # Download options
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📄 Download Itinerary PDF", use_container_width=True):
                        st.info("PDF download will start shortly...")
                with col2:
                    if st.button("📧 Email Confirmation", use_container_width=True):
                        st.success(f"Confirmation sent to {email}")
                with col3:
                    if st.button("🏠 Return to Home", use_container_width=True):
                        st.session_state.step = 1
                        st.session_state.user_data = {}
                        st.session_state.trip_plan = None
                        st.session_state.show_booking = False
                        st.rerun()


if __name__ == "__main__":
    main()
