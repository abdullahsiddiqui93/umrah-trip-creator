# Interactive Flight and Hotel Selection Update ✅

## Summary

Updated the Umrah Trip Creator frontend to provide an **interactive selection experience** where users can choose their preferred flight and hotel options through radio buttons, with real-time cost calculations based on their selections.

## Changes Made

### 1. Session State Management

Added new session state variables to track user selections:
```python
if 'selected_flight' not in st.session_state:
    st.session_state.selected_flight = None
if 'selected_makkah_hotel' not in st.session_state:
    st.session_state.selected_makkah_hotel = None
if 'selected_madinah_hotel' not in st.session_state:
    st.session_state.selected_madinah_hotel = None
```

### 2. Interactive Flight Selection

**Before:** Flights displayed in expandable sections with individual "Select" buttons
**After:** Radio button selection with detailed view of chosen option

**Features:**
- Radio buttons for easy selection
- Displays all flight options with key info (airline, price, stops)
- Shows detailed breakdown of selected flight
- Highlights outbound and return flight details
- Displays price per person and total cost
- Shows baggage allowance and cabin class
- Visual confirmation of selection

**User Experience:**
```
○ Option 1: Saudi Airlines - USD 850 per person | Direct
● Option 2: Emirates - USD 920 per person | 1 stop (DXB)  ← Selected
○ Option 3: Turkish Airlines - USD 880 per person | 1 stop (IST)

[Detailed view of selected flight appears below]
```

### 3. Interactive Hotel Selection

**Before:** Hotels displayed in expandable sections with individual "Select" buttons
**After:** Side-by-side radio button selection for Makkah and Madinah hotels

**Features:**
- Separate radio button groups for Makkah and Madinah
- Shows hotel name, star rating, distance, and price per night
- Displays detailed information for selected hotels
- Shows total cost for entire stay
- Lists amenities and ratings
- Visual confirmation of selections

**User Experience:**
```
Makkah Hotel                          Madinah Hotel
○ Swissotel (5⭐) - 200m | $180/night  ○ Pullman (5⭐) - 100m | $150/night
● Hilton (5⭐) - 150m | $220/night     ● Oberoi (5⭐) - 50m | $200/night
```

### 4. Dynamic Cost Calculation

**Before:** Fixed cost breakdown from mock data
**After:** Real-time calculation based on user selections

**Features:**
- Calculates flight cost: `selected_flight_price × num_travelers`
- Calculates hotel costs: `makkah_hotel_total + madinah_hotel_total`
- Adds visa fees and service charges
- Applies discount for bookings over $2000
- Updates total dynamically as selections change

**Cost Breakdown Display:**
```
Flights (2 travelers)          USD 1,840
Hotels (Makkah + Madinah)      USD 1,700
Visa Fees (2 travelers)        USD 300
Service Fee                    USD 100
---
Subtotal                       USD 3,940
Discount                       -USD 200
---
Total                          USD 3,740
```

### 5. Selection Validation

**Features:**
- Checks if all required selections are made (flight, Makkah hotel, Madinah hotel)
- Displays warning if any selection is missing
- Disables booking until all selections are complete
- Shows clear status for each selection

**Validation Message:**
```
⚠️ Please select your preferred flight and hotels from the tabs above before proceeding to payment.
```

### 6. Booking Confirmation Enhancement

**Features:**
- Shows summary of selected options at top of booking section
- Displays selected flight airline and price
- Shows selected hotel names and locations
- Confirms total amount to be paid
- Includes all selections in booking confirmation

**Confirmation Display:**
```
Your Selected Options
✈️ Flight: Emirates - USD 920 per person
🕋 Makkah Hotel: Hilton Makkah (5⭐) - 150m from Haram
🕌 Madinah Hotel: Oberoi Madinah (5⭐) - 50m from Haram
```

## User Flow

### Step 1: View Trip Options
User navigates to "Trip Options" tab after AI generates the plan

### Step 2: Select Flight
1. User sees all available flight options with radio buttons
2. User clicks on preferred flight option
3. Detailed flight information appears
4. Selection is stored in session state
5. Visual confirmation shown

### Step 3: Select Hotels
1. User sees Makkah hotel options with radio buttons
2. User selects preferred Makkah hotel
3. User sees Madinah hotel options with radio buttons
4. User selects preferred Madinah hotel
5. Both selections stored and confirmed

### Step 4: Review Booking
1. User navigates to "Booking" tab
2. System shows summary of all selections
3. System calculates total cost based on selections
4. User reviews cost breakdown
5. User proceeds to payment if satisfied

### Step 5: Complete Booking
1. User enters payment and contact information
2. User agrees to terms and conditions
3. User clicks "Confirm Booking"
4. System shows booking confirmation with all selected items
5. User receives confirmation number and download options

## Technical Implementation

### Radio Button Selection
```python
selected_index = st.radio(
    "Choose your flight:",
    range(len(flights)),
    format_func=lambda x: flight_options[x],
    key="flight_selection"
)
st.session_state.selected_flight = selected_index
```

### Dynamic Cost Calculation
```python
flight_cost = plan['flights'][st.session_state.selected_flight]['price'] * plan['num_travelers']
makkah_hotel_cost = plan['hotels']['makkah'][st.session_state.selected_makkah_hotel]['total_price']
madinah_hotel_cost = plan['hotels']['madinah'][st.session_state.selected_madinah_hotel]['total_price']
total = flight_cost + makkah_hotel_cost + madinah_hotel_cost + visa_cost + service_fee - discount
```

### Selection Validation
```python
all_selected = (
    st.session_state.selected_flight is not None and
    st.session_state.selected_makkah_hotel is not None and
    st.session_state.selected_madinah_hotel is not None
)

if not all_selected:
    st.warning("⚠️ Please select your preferred options...")
    return
```

## Benefits

### For Users
1. **Clear Selection Process** - Radio buttons make it obvious which option is selected
2. **Easy Comparison** - All options visible at once for easy comparison
3. **Accurate Pricing** - Total cost reflects actual selections, not estimates
4. **Visual Feedback** - Immediate confirmation of selections
5. **Flexible Choice** - Can change selections before booking
6. **Transparent Costs** - See exactly what you're paying for

### For System
1. **State Management** - Selections stored in session state
2. **Data Integrity** - Only selected items used in calculations
3. **Validation** - Ensures all required selections made
4. **Scalability** - Easy to add more options or categories
5. **Maintainability** - Clean separation of selection and display logic

## UI/UX Improvements

### Before
- Multiple expandable sections
- Separate "Select" buttons for each option
- Unclear which option was selected
- Fixed cost breakdown
- No validation of selections

### After
- Clean radio button interface
- Single selection per category
- Clear visual indication of selection
- Dynamic cost calculation
- Validation before booking
- Summary of selections in booking section

## Example User Journey

**Scenario:** Sarah is planning an Umrah trip for 2 people

1. **Flight Selection:**
   - Sees 3 flight options
   - Compares prices and routes
   - Selects Emirates (1 stop via Dubai) for $920/person
   - Sees total flight cost: $1,840

2. **Hotel Selection:**
   - **Makkah:** Compares 2 hotels
     - Selects Hilton (5⭐, 150m from Haram) at $220/night
     - Total: $1,100 for 5 nights
   - **Madinah:** Compares 2 hotels
     - Selects Oberoi (5⭐, 50m from Haram) at $200/night
     - Total: $600 for 3 nights

3. **Review:**
   - Sees summary: Emirates + Hilton + Oberoi
   - Total cost: $3,740 (including visa and fees)
   - Discount applied: $200 off

4. **Booking:**
   - Enters payment information
   - Confirms booking
   - Receives confirmation: UMRAH-123456

## Testing Checklist

- [x] Flight selection works with radio buttons
- [x] Hotel selection works for both Makkah and Madinah
- [x] Selections stored in session state
- [x] Cost calculation updates based on selections
- [x] Validation prevents booking without selections
- [x] Booking confirmation shows selected items
- [x] Visual feedback for all selections
- [x] Works with both demo and production modes

## Files Modified

- `frontend/streamlit_app.py` - Updated flight and hotel selection UI

## Next Steps

### Potential Enhancements
1. **Comparison View** - Side-by-side comparison of options
2. **Filters** - Filter flights by price, duration, stops
3. **Sorting** - Sort hotels by price, distance, rating
4. **Favorites** - Save preferred options for later
5. **Price Alerts** - Notify when prices drop
6. **Reviews** - Show user reviews for hotels
7. **Photos** - Display hotel and airline photos
8. **Maps** - Show hotel locations on map
9. **Calendar View** - Visual date selection
10. **Multi-currency** - Display prices in user's currency

### Integration with Real Data
When using AgentCore agents with real API data:
1. Parse AI responses to extract structured flight/hotel data
2. Create proper data structures from API responses
3. Handle varying numbers of options (2-5 flights, 3-10 hotels)
4. Display real prices, availability, and details
5. Update cost calculations with actual API data

## Conclusion

The interactive selection feature provides a **professional, user-friendly booking experience** that:
- Makes it easy to compare and select options
- Provides accurate pricing based on selections
- Validates selections before booking
- Gives clear visual feedback
- Calculates costs dynamically
- Enhances the overall user experience

Users can now confidently select their preferred flight and hotel options and see exactly what they're paying for before completing their booking! ✨
