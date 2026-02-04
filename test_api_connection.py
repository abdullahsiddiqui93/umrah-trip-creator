#!/usr/bin/env python3
"""
Diagnostic script to test Amadeus API connection and credentials
"""

import os
import requests
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def test_authentication():
    """Test Amadeus API authentication"""
    print("=" * 60)
    print("AMADEUS API CONNECTION TEST")
    print("=" * 60)
    
    api_key = os.getenv("AMADEUS_API_KEY")
    api_secret = os.getenv("AMADEUS_API_SECRET")
    
    print("\n1. Checking Credentials...")
    if api_key:
        print(f"   ✅ API Key: {api_key[:10]}...{api_key[-4:]}")
    else:
        print("   ❌ API Key: NOT SET")
        return False
    
    if api_secret:
        print(f"   ✅ API Secret: {api_secret[:10]}...{api_secret[-4:]}")
    else:
        print("   ❌ API Secret: NOT SET")
        return False
    
    print("\n2. Testing Authentication...")
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": api_secret
    }
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        print(f"   ✅ Authentication successful!")
        print(f"   Token: {result['access_token'][:30]}...")
        print(f"   Expires in: {result.get('expires_in', 'unknown')} seconds")
        
        return result['access_token']
    except requests.exceptions.HTTPError as e:
        print(f"   ❌ Authentication failed: HTTP {e.response.status_code}")
        print(f"   Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"   ❌ Authentication failed: {e}")
        return None


def test_flight_search(token):
    """Test flight search API"""
    print("\n3. Testing Flight Search API...")
    
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {token}"}
    
    params = {
        "originLocationCode": "JFK",
        "destinationLocationCode": "JED",
        "departureDate": "2026-03-15",
        "returnDate": "2026-03-25",
        "adults": 2,
        "max": 3,
        "currencyCode": "USD"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if "data" in data and len(data["data"]) > 0:
            print(f"   ✅ Flight search successful!")
            print(f"   Found {len(data['data'])} flight options")
            
            # Show first flight
            first_flight = data["data"][0]
            price = first_flight.get("price", {})
            print(f"   Example: ${price.get('total', 'N/A')} {price.get('currency', 'USD')}")
            
            return True
        else:
            print(f"   ⚠️  No flights found (this may be normal for test data)")
            return True
            
    except requests.exceptions.HTTPError as e:
        print(f"   ❌ Flight search failed: HTTP {e.response.status_code}")
        print(f"   Response: {e.response.text[:200]}")
        return False
    except Exception as e:
        print(f"   ❌ Flight search failed: {e}")
        return False


def test_hotel_search(token):
    """Test hotel search API"""
    print("\n4. Testing Hotel Search API...")
    
    # First get hotel IDs
    url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
    headers = {"Authorization": f"Bearer {token}"}
    
    params = {
        "cityCode": "MEC",  # Makkah
        "radius": 5,
        "radiusUnit": "KM",
        "hotelSource": "ALL"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if "data" in data and len(data["data"]) > 0:
            print(f"   ✅ Hotel search successful!")
            print(f"   Found {len(data['data'])} hotels in Makkah")
            
            # Show first hotel
            first_hotel = data["data"][0]
            print(f"   Example: {first_hotel.get('name', 'N/A')}")
            
            return True
        else:
            print(f"   ⚠️  No hotels found (this may be normal for test data)")
            return True
            
    except requests.exceptions.HTTPError as e:
        print(f"   ❌ Hotel search failed: HTTP {e.response.status_code}")
        print(f"   Response: {e.response.text[:200]}")
        return False
    except Exception as e:
        print(f"   ❌ Hotel search failed: {e}")
        return False


def main():
    """Run all diagnostic tests"""
    
    # Test authentication
    token = test_authentication()
    if not token:
        print("\n" + "=" * 60)
        print("RESULT: Authentication failed. Check your API credentials.")
        print("=" * 60)
        return
    
    # Test flight search
    flight_ok = test_flight_search(token)
    
    # Test hotel search
    hotel_ok = test_hotel_search(token)
    
    # Summary
    print("\n" + "=" * 60)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 60)
    print(f"Authentication: {'✅ PASS' if token else '❌ FAIL'}")
    print(f"Flight Search:  {'✅ PASS' if flight_ok else '❌ FAIL'}")
    print(f"Hotel Search:   {'✅ PASS' if hotel_ok else '❌ FAIL'}")
    
    if token and flight_ok and hotel_ok:
        print("\n✅ All tests passed! API connection is working.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
