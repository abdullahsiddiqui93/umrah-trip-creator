"""
Amadeus API Tools for Flight Search
Real-time flight data integration
"""

import os
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class AmadeusAPI:
    """Amadeus API client for flight searches"""
    
    def __init__(self):
        self.api_key = os.getenv("AMADEUS_API_KEY")
        self.api_secret = os.getenv("AMADEUS_API_SECRET")
        self.base_url = "https://test.api.amadeus.com/v2"
        self.token = None
        self.token_expires = None
    
    def _get_access_token(self) -> str:
        """Get OAuth access token"""
        if self.token and self.token_expires and datetime.now() < self.token_expires:
            return self.token
        
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }
        
        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            self.token = result["access_token"]
            # Token expires in seconds, set expiry time
            expires_in = result.get("expires_in", 1799)
            self.token_expires = datetime.now() + timedelta(seconds=expires_in - 60)
            
            return self.token
        except Exception as e:
            print(f"Error getting Amadeus token: {e}")
            return None
    
    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str] = None,
        adults: int = 1,
        travel_class: str = "ECONOMY",
        non_stop: bool = False,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """
        Search for flights using Amadeus API
        
        Args:
            origin: IATA airport code (e.g., 'JFK')
            destination: IATA airport code (e.g., 'JED' for Jeddah, 'MED' for Medina)
            departure_date: Date in YYYY-MM-DD format
            return_date: Return date in YYYY-MM-DD format (optional for one-way)
            adults: Number of adult passengers
            travel_class: ECONOMY, PREMIUM_ECONOMY, BUSINESS, or FIRST
            non_stop: True for direct flights only
            max_results: Maximum number of results to return
        
        Returns:
            Dict with flight offers or error message
        """
        token = self._get_access_token()
        if not token:
            return {"error": "Failed to authenticate with Amadeus API"}
        
        url = f"{self.base_url}/shopping/flight-offers"
        headers = {"Authorization": f"Bearer {token}"}
        
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "adults": adults,
            "travelClass": travel_class,
            "nonStop": str(non_stop).lower(),
            "max": max_results,
            "currencyCode": "USD"
        }
        
        if return_date:
            params["returnDate"] = return_date
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if "data" not in data or len(data["data"]) == 0:
                return {
                    "error": "No flights found",
                    "message": f"No flights available from {origin} to {destination} on {departure_date}"
                }
            
            # Parse and format flight offers
            flights = []
            for offer in data["data"][:max_results]:
                flight_info = self._parse_flight_offer(offer)
                flights.append(flight_info)
            
            return {
                "success": True,
                "flights": flights,
                "count": len(flights)
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "error": "API request failed",
                "message": str(e)
            }
        except Exception as e:
            return {
                "error": "Failed to parse flight data",
                "message": str(e)
            }
    
    def _parse_flight_offer(self, offer: Dict) -> Dict[str, Any]:
        """Parse Amadeus flight offer into simplified format"""
        try:
            itineraries = offer.get("itineraries", [])
            price = offer.get("price", {})
            
            # Get outbound flight details
            outbound = itineraries[0] if len(itineraries) > 0 else {}
            segments = outbound.get("segments", [])
            
            # Get return flight details if available
            return_flight = None
            if len(itineraries) > 1:
                return_segments = itineraries[1].get("segments", [])
                if return_segments:
                    return_flight = {
                        "departure": return_segments[0].get("departure", {}),
                        "arrival": return_segments[-1].get("arrival", {}),
                        "duration": itineraries[1].get("duration", ""),
                        "stops": len(return_segments) - 1
                    }
            
            return {
                "id": offer.get("id"),
                "price": {
                    "total": price.get("total"),
                    "currency": price.get("currency", "USD"),
                    "per_person": price.get("total")
                },
                "outbound": {
                    "departure": segments[0].get("departure", {}) if segments else {},
                    "arrival": segments[-1].get("arrival", {}) if segments else {},
                    "duration": outbound.get("duration", ""),
                    "stops": len(segments) - 1,
                    "segments": [
                        {
                            "airline": seg.get("carrierCode"),
                            "flight_number": f"{seg.get('carrierCode')}{seg.get('number')}",
                            "departure": seg.get("departure", {}),
                            "arrival": seg.get("arrival", {}),
                            "duration": seg.get("duration", ""),
                            "aircraft": seg.get("aircraft", {}).get("code")
                        }
                        for seg in segments
                    ]
                },
                "return": return_flight,
                "seats_available": offer.get("numberOfBookableSeats", "Unknown"),
                "cabin_class": segments[0].get("cabin", "ECONOMY") if segments else "ECONOMY",
                "validating_airline": offer.get("validatingAirlineCodes", [""])[0]
            }
        except Exception as e:
            print(f"Error parsing flight offer: {e}")
            return {
                "error": "Failed to parse flight",
                "raw_data": offer
            }
    
    def get_airport_code(self, city_name: str) -> Optional[str]:
        """Get IATA airport code for a city"""
        # Common airports for Umrah
        airports = {
            "jeddah": "JED",
            "medina": "MED",
            "madinah": "MED",
            "riyadh": "RUH",
            "dammam": "DMM",
            "new york": "JFK",
            "los angeles": "LAX",
            "london": "LHR",
            "dubai": "DXB",
            "istanbul": "IST",
            "cairo": "CAI",
            "chicago": "ORD",
            "houston": "IAH",
            "washington": "IAD",
            "atlanta": "ATL",
            "dallas": "DFW",
            "miami": "MIA",
            "toronto": "YYZ",
            "paris": "CDG",
            "frankfurt": "FRA"
        }
        
        city_lower = city_name.lower().strip()
        return airports.get(city_lower)


# Create singleton instance
_amadeus_api = None

def get_amadeus_api() -> AmadeusAPI:
    """Get or create Amadeus API instance"""
    global _amadeus_api
    if _amadeus_api is None:
        _amadeus_api = AmadeusAPI()
    return _amadeus_api
