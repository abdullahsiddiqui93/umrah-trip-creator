"""
Streamlit Frontend for Umrah Trip Creator
Multi-step interface for planning Umrah trips with AI agents
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import time

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Import authentication module
from frontend.auth import require_authentication, show_user_menu

# Note: Agent imports commented out for demo mode
# Uncomment when agent dependencies are installed
# from agents.orchestrator.orchestrator_agent import create_orchestrator_agent
# from agents.flight_agent.flight_agent import create_flight_agent
# from agents.hotel_agent.hotel_agent import create_hotel_agent
# from agents.visa_agent.visa_agent import create_visa_agent
# from agents.itinerary_agent.itinerary_agent import create_itinerary_agent

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


def main():
    """Main application flow"""
    
    # Check authentication first
    if not require_authentication():
        return  # Show login page
    
    # Header
    st.markdown('<h1 class="main-header">🕋 Umrah Trip Creator</h1>', unsafe_allow_html=True)
    st.markdown("### Plan your blessed journey with AI-powered assistance")
    
    # Demo mode indicator
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
                'additional_notes': additional_notes
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
    
    # Demo mode banner
    st.info("ℹ️ **Demo Mode**: This is a demonstration with mock data. In production, real AI agents would search live flight/hotel APIs and generate actual options based on your preferences.")
    
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
    
    # Generate plan button
    if st.button("🚀 Generate My Umrah Trip Plan", type="primary", use_container_width=True):
        with st.spinner("🤖 AI Agents are working on your perfect Umrah trip..."):
            # Simulate agent processing
            import time
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Orchestrator
            status_text.text("🎯 Orchestrator Agent: Analyzing your requirements...")
            time.sleep(2)
            progress_bar.progress(20)
            
            # Step 2: Visa Agent
            status_text.text("🛂 Visa Agent: Checking visa requirements...")
            time.sleep(2)
            progress_bar.progress(40)
            
            # Step 3: Flight Agent
            status_text.text("✈️ Flight Agent: Searching best flight options...")
            time.sleep(2)
            progress_bar.progress(60)
            
            # Step 4: Hotel Agent
            status_text.text("🏨 Hotel Agent: Finding perfect accommodations...")
            time.sleep(2)
            progress_bar.progress(80)
            
            # Step 5: Itinerary Agent
            status_text.text("📅 Itinerary Agent: Creating your Umrah schedule...")
            time.sleep(2)
            progress_bar.progress(100)
            
            status_text.text("✅ Trip plan generated successfully!")
            
            # Store mock trip plan
            st.session_state.trip_plan = generate_mock_trip_plan()
            st.session_state.step = 6
            
            time.sleep(1)
            st.rerun()
    
    # Back button
    if st.button("← Back", use_container_width=True):
        st.session_state.step = 4
        st.rerun()


def step_trip_options():
    """Step 6: Display trip options and booking"""
    st.markdown('<h2 class="step-header">✨ Your Umrah Trip Options</h2>', unsafe_allow_html=True)
    
    # Demo mode banner
    st.warning("🎭 **Demo Mode Active**: The options below are sample data for demonstration purposes. In production, these would be real-time results from:\n- ✈️ Amadeus API (flights)\n- 🏨 Booking.com API (hotels)\n- 🛂 Visa databases\n- 📅 AI-generated itineraries")
    
    if not st.session_state.trip_plan:
        st.error("No trip plan generated. Please go back and generate a plan.")
        return
    
    plan = st.session_state.trip_plan
    
    # Summary card
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Cost", f"{plan['currency']} {plan['total_cost']:,}")
    with col2:
        st.metric("Duration", f"{plan['duration']} days")
    with col3:
        st.metric("Travelers", plan['num_travelers'])
    with col4:
        st.metric("Savings", f"{plan['currency']} {plan['savings']:,}")
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
    """Display flight options"""
    st.markdown("### Flight Options")
    
    for i, flight in enumerate(flights, 1):
        with st.expander(f"Option {i}: {flight['airline']} - {flight['currency']} {flight['price']:,}", expanded=(i==1)):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Outbound Flight**")
                st.write(f"🛫 {flight['outbound']['departure']}")
                st.write(f"🛬 {flight['outbound']['arrival']}")
                st.write(f"⏱️ Duration: {flight['outbound']['duration']}")
                st.write(f"🔄 Stops: {flight['outbound']['stops']}")
            
            with col2:
                st.markdown("**Return Flight**")
                st.write(f"🛫 {flight['return']['departure']}")
                st.write(f"🛬 {flight['return']['arrival']}")
                st.write(f"⏱️ Duration: {flight['return']['duration']}")
                st.write(f"🔄 Stops: {flight['return']['stops']}")
            
            st.write(f"**Baggage:** {flight['baggage']}")
            st.write(f"**Cabin Class:** {flight['cabin_class']}")
            
            if st.button(f"Select Flight Option {i}", key=f"flight_{i}"):
                st.success(f"✅ Flight Option {i} selected!")


def display_hotel_options(hotels):
    """Display hotel options"""
    st.markdown("### Hotel Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🕋 Makkah Hotels")
        for i, hotel in enumerate(hotels['makkah'], 1):
            with st.expander(f"{hotel['name']} - {hotel['stars']}⭐", expanded=(i==1)):
                st.write(f"**Distance:** {hotel['distance']}")
                st.write(f"**Price per night:** {hotel['currency']} {hotel['price_per_night']}")
                st.write(f"**Total:** {hotel['currency']} {hotel['total_price']:,}")
                st.write(f"**Amenities:** {', '.join(hotel['amenities'])}")
                st.write(f"**Rating:** {hotel['rating']}/10")
                
                if st.button(f"Select Makkah Hotel {i}", key=f"makkah_hotel_{i}"):
                    st.success(f"✅ {hotel['name']} selected!")
    
    with col2:
        st.markdown("#### 🕌 Madinah Hotels")
        for i, hotel in enumerate(hotels['madinah'], 1):
            with st.expander(f"{hotel['name']} - {hotel['stars']}⭐", expanded=(i==1)):
                st.write(f"**Distance:** {hotel['distance']}")
                st.write(f"**Price per night:** {hotel['currency']} {hotel['price_per_night']}")
                st.write(f"**Total:** {hotel['currency']} {hotel['total_price']:,}")
                st.write(f"**Amenities:** {', '.join(hotel['amenities'])}")
                st.write(f"**Rating:** {hotel['rating']}/10")
                
                if st.button(f"Select Madinah Hotel {i}", key=f"madinah_hotel_{i}"):
                    st.success(f"✅ {hotel['name']} selected!")


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
    """Display booking and payment section"""
    st.markdown("### Complete Your Booking")
    
    st.markdown("#### 📊 Cost Breakdown")
    
    breakdown = plan['cost_breakdown']
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write(f"Flights (all travelers)")
        st.write(f"Hotels (Makkah + Madinah)")
        st.write(f"Visa Fees (all travelers)")
        st.write(f"Service Fee")
        st.write("---")
        st.write(f"**Subtotal**")
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
        st.write(f"-{breakdown['currency']} {breakdown['discount']:,}")
        st.write("---")
        st.markdown(f"### **{breakdown['currency']} {breakdown['total']:,}**")
    
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
            
            # Download options
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button("📄 Download Itinerary (PDF)", "itinerary.pdf", "application/pdf")
            with col2:
                st.download_button("📋 Download Booking Details", "booking.json", "application/json")
            with col3:
                st.download_button("📧 Download Visa Documents", "visa_docs.zip", "application/zip")


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


if __name__ == "__main__":
    main()
