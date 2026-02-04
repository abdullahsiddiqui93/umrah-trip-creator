#!/usr/bin/env python3
"""
Test Amadeus API directly to see actual errors
"""

import sys
sys.path.append('agents/flight_agent')
sys.path.append('agents/hotel_agent')

from amadeus_tools import get_amadeus_api
from amadeus_hotel_tools import get_amadeus_hotel_api

print("="*60)
print("DIRECT API TEST")
print("="*60)

# Test Flight API
print("\n1. Testing Flight Search...")
flight_api = get_amadeus_api()
result = flight_api.search_flights(
    origin="JFK",
    destination="JED",
    departure_date="2026-03-15",
    return_date="2026-03-25",
    adults=2,
    max_results=3
)

print("Flight Result:")
if "error" in result:
    print(f"❌ Error: {result['error']}")
    print(f"Message: {result.get('message', 'N/A')}")
else:
    print(f"✅ Success! Found {result.get('count', 0)} flights")
    if result.get('flights'):
        first = result['flights'][0]
        print(f"Example: ${first['price']['total']} {first['price']['currency']}")

# Test Hotel API
print("\n2. Testing Hotel Search...")
hotel_api = get_amadeus_hotel_api()
result = hotel_api.search_hotels_near_landmark(
    latitude=21.4225,  # Masjid al-Haram
    longitude=39.8262,
    check_in="2026-03-15",
    check_out="2026-03-20",
    adults=2,
    radius=2,
    radius_unit="KM",
    max_results=3
)

print("Hotel Result:")
if "error" in result:
    print(f"❌ Error: {result['error']}")
    print(f"Message: {result.get('message', 'N/A')}")
else:
    print(f"✅ Success! Found {result.get('count', 0)} hotels")
    if result.get('hotels'):
        first = result['hotels'][0]
        print(f"Example: {first.get('name', 'N/A')}")

print("\n" + "="*60)
