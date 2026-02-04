"""
Amadeus API Tools for Hotel Search
Real-time hotel data integration
"""

import os
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class AmadeusHotelAPI:
    """Amadeus API client for hotel searches"""
    
    def __init__(self):
        self.api_key = os.getenv("AMADEUS_API_KEY")
        self.api_secret = os.getenv("AMADEUS_API_SECRET")
        self.base_url = "https://test.api.amadeus.com"
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
    
    def get_city_code(self, city_name: str) -> Optional[str]:
        """Get IATA city code for hotel search"""
        # Common city codes for Umrah destinations
        cities = {
            "makkah": "MEC",  # Mecca
            "mecca": "MEC",
            "medina": "MED",
            "madinah": "MED",
            "jeddah": "JED",
            "riyadh": "RUH"
        }
        
        city_lower = city_name.lower().strip()
        return cities.get(city_lower)
    
    def search_hotels_by_city(
        self,
        city_code: str,
        check_in: str,
        check_out: str,
        adults: int = 2,
        radius: int = 5,
        radius_unit: str = "KM",
        ratings: Optional[List[int]] = None,
        amenities: Optional[List[str]] = None,
        max_results: int = 10
    ) -> Dict[str, Any]:
        """
        Search for hotels by city using Amadeus Hotel List API
        
        Args:
            city_code: IATA city code (e.g., 'MEC' for Makkah, 'MED' for Medina)
            check_in: Check-in date in YYYY-MM-DD format
            check_out: Check-out date in YYYY-MM-DD format
            adults: Number of adult guests
            radius: Search radius
            radius_unit: KM or MILE
            ratings: List of hotel ratings (1-5)
            amenities: List of amenity codes
            max_results: Maximum number of results
        
        Returns:
            Dict with hotel offers or error message
        """
        token = self._get_access_token()
        if not token:
            return {"error": "Failed to authenticate with Amadeus API"}
        
        # First, get hotel IDs in the city
        url = f"{self.base_url}/v1/reference-data/locations/hotels/by-city"
        headers = {"Authorization": f"Bearer {token}"}
        
        params = {
            "cityCode": city_code,
            "radius": radius,
            "radiusUnit": radius_unit,
            "hotelSource": "ALL"
        }
        
        if ratings:
            params["ratings"] = ",".join(str(r) for r in ratings)
        
        if amenities:
            params["amenities"] = ",".join(amenities)
        
        try:
            # Get hotel IDs
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if "data" not in data or len(data["data"]) == 0:
                return {
                    "error": "No hotels found",
                    "message": f"No hotels available in city code {city_code}"
                }
            
            # Get hotel IDs (limit to max_results)
            hotel_ids = [hotel["hotelId"] for hotel in data["data"][:max_results]]
            
            # Now get hotel offers with pricing
            return self.get_hotel_offers(hotel_ids, check_in, check_out, adults)
            
        except requests.exceptions.RequestException as e:
            return {
                "error": "API request failed",
                "message": str(e)
            }
        except Exception as e:
            return {
                "error": "Failed to search hotels",
                "message": str(e)
            }
    
    def get_hotel_offers(
        self,
        hotel_ids: List[str],
        check_in: str,
        check_out: str,
        adults: int = 2,
        room_quantity: int = 1,
        currency: str = "USD"
    ) -> Dict[str, Any]:
        """
        Get hotel offers with pricing
        
        Args:
            hotel_ids: List of Amadeus hotel IDs
            check_in: Check-in date in YYYY-MM-DD format
            check_out: Check-out date in YYYY-MM-DD format
            adults: Number of adults
            room_quantity: Number of rooms
            currency: Currency code
        
        Returns:
            Dict with hotel offers including prices
        """
        token = self._get_access_token()
        if not token:
            return {"error": "Failed to authenticate with Amadeus API"}
        
        url = f"{self.base_url}/v3/shopping/hotel-offers"
        headers = {"Authorization": f"Bearer {token}"}
        
        params = {
            "hotelIds": ",".join(hotel_ids[:50]),  # API limit is 50 hotels per request
            "checkInDate": check_in,
            "checkOutDate": check_out,
            "adults": adults,
            "roomQuantity": room_quantity,
            "currency": currency,
            "bestRateOnly": "true"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if "data" not in data or len(data["data"]) == 0:
                return {
                    "error": "No hotel offers found",
                    "message": "No availability for the selected dates"
                }
            
            # Parse hotel offers
            hotels = []
            for hotel_data in data["data"]:
                hotel_info = self._parse_hotel_offer(hotel_data, check_in, check_out)
                if hotel_info:
                    hotels.append(hotel_info)
            
            return {
                "success": True,
                "hotels": hotels,
                "count": len(hotels),
                "check_in": check_in,
                "check_out": check_out
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "error": "API request failed",
                "message": str(e)
            }
        except Exception as e:
            return {
                "error": "Failed to get hotel offers",
                "message": str(e)
            }
    
    def _parse_hotel_offer(self, hotel_data: Dict, check_in: str, check_out: str) -> Optional[Dict[str, Any]]:
        """Parse Amadeus hotel offer into simplified format"""
        try:
            hotel = hotel_data.get("hotel", {})
            offers = hotel_data.get("offers", [])
            
            if not offers:
                return None
            
            # Get best offer (first one since we requested bestRateOnly)
            best_offer = offers[0]
            price = best_offer.get("price", {})
            room = best_offer.get("room", {})
            
            # Calculate number of nights
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
            nights = (check_out_date - check_in_date).days
            
            # Get hotel details
            hotel_info = {
                "hotel_id": hotel.get("hotelId"),
                "name": hotel.get("name", "Unknown Hotel"),
                "rating": hotel.get("rating"),
                "latitude": hotel.get("latitude"),
                "longitude": hotel.get("longitude"),
                "address": {
                    "lines": hotel.get("address", {}).get("lines", []),
                    "city": hotel.get("address", {}).get("cityName"),
                    "country": hotel.get("address", {}).get("countryCode")
                },
                "contact": hotel.get("contact", {}),
                "amenities": hotel.get("amenities", []),
                "price": {
                    "total": price.get("total"),
                    "currency": price.get("currency", "USD"),
                    "per_night": float(price.get("total", 0)) / nights if nights > 0 else 0,
                    "nights": nights,
                    "base": price.get("base"),
                    "taxes": price.get("taxes", [])
                },
                "room": {
                    "type": room.get("type"),
                    "type_estimated": room.get("typeEstimated", {}).get("category"),
                    "description": room.get("description", {}).get("text"),
                    "beds": room.get("description", {}).get("beds")
                },
                "policies": {
                    "cancellation": best_offer.get("policies", {}).get("cancellation"),
                    "payment_type": best_offer.get("policies", {}).get("paymentType")
                },
                "check_in": check_in,
                "check_out": check_out
            }
            
            return hotel_info
            
        except Exception as e:
            print(f"Error parsing hotel offer: {e}")
            return None
    
    def search_hotels_near_landmark(
        self,
        latitude: float,
        longitude: float,
        check_in: str,
        check_out: str,
        adults: int = 2,
        radius: int = 1,
        radius_unit: str = "KM",
        ratings: Optional[List[int]] = None,
        max_results: int = 10
    ) -> Dict[str, Any]:
        """
        Search for hotels near a specific landmark (e.g., Haram)
        
        Args:
            latitude: Latitude of the landmark
            longitude: Longitude of the landmark
            check_in: Check-in date
            check_out: Check-out date
            adults: Number of adults
            radius: Search radius
            radius_unit: KM or MILE
            ratings: List of hotel ratings
            max_results: Maximum results
        
        Returns:
            Dict with hotel offers
        """
        token = self._get_access_token()
        if not token:
            return {"error": "Failed to authenticate with Amadeus API"}
        
        # Get hotels by geocode
        url = f"{self.base_url}/v1/reference-data/locations/hotels/by-geocode"
        headers = {"Authorization": f"Bearer {token}"}
        
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "radius": radius,
            "radiusUnit": radius_unit,
            "hotelSource": "ALL"
        }
        
        if ratings:
            params["ratings"] = ",".join(str(r) for r in ratings)
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if "data" not in data or len(data["data"]) == 0:
                return {
                    "error": "No hotels found",
                    "message": f"No hotels near coordinates ({latitude}, {longitude})"
                }
            
            # Get hotel IDs with distance information
            hotels_with_distance = []
            for hotel in data["data"][:max_results]:
                hotels_with_distance.append({
                    "hotel_id": hotel["hotelId"],
                    "name": hotel.get("name"),
                    "distance": hotel.get("distance", {}).get("value"),
                    "distance_unit": hotel.get("distance", {}).get("unit")
                })
            
            hotel_ids = [h["hotel_id"] for h in hotels_with_distance]
            
            # Get offers with pricing
            offers_result = self.get_hotel_offers(hotel_ids, check_in, check_out, adults)
            
            # Add distance information to results
            if offers_result.get("success") and offers_result.get("hotels"):
                distance_map = {h["hotel_id"]: h for h in hotels_with_distance}
                for hotel in offers_result["hotels"]:
                    hotel_id = hotel.get("hotel_id")
                    if hotel_id in distance_map:
                        hotel["distance_to_landmark"] = {
                            "value": distance_map[hotel_id]["distance"],
                            "unit": distance_map[hotel_id]["distance_unit"]
                        }
            
            return offers_result
            
        except requests.exceptions.RequestException as e:
            return {
                "error": "API request failed",
                "message": str(e)
            }
        except Exception as e:
            return {
                "error": "Failed to search hotels",
                "message": str(e)
            }


# Landmark coordinates for Umrah destinations
LANDMARKS = {
    "masjid_al_haram": {
        "name": "Masjid al-Haram (Kaaba)",
        "latitude": 21.4225,
        "longitude": 39.8262,
        "city": "Makkah"
    },
    "masjid_nabawi": {
        "name": "Masjid an-Nabawi",
        "latitude": 24.4672,
        "longitude": 39.6111,
        "city": "Medina"
    }
}


# Create singleton instance
_amadeus_hotel_api = None

def get_amadeus_hotel_api() -> AmadeusHotelAPI:
    """Get or create Amadeus Hotel API instance"""
    global _amadeus_hotel_api
    if _amadeus_hotel_api is None:
        _amadeus_hotel_api = AmadeusHotelAPI()
    return _amadeus_hotel_api
