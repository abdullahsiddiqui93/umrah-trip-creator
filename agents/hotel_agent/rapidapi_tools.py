"""
RapidAPI Tools for Hotel Search
Real-time hotel data integration using Booking.com API
"""

import os
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime


class RapidAPIHotels:
    """RapidAPI client for hotel searches using Booking.com"""
    
    def __init__(self):
        self.api_key = os.getenv("RAPIDAPI_KEY")
        self.base_url = "https://booking-com.p.rapidapi.com/v1"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
        }
    
    def search_hotels(
        self,
        city: str,
        check_in: str,
        check_out: str,
        adults: int = 2,
        rooms: int = 1,
        currency: str = "USD",
        locale: str = "en-us",
        order_by: str = "popularity",
        filter_by_star: Optional[List[int]] = None,
        max_results: int = 10
    ) -> Dict[str, Any]:
        """
        Search for hotels in a city
        
        Args:
            city: City name (e.g., 'Makkah', 'Medina')
            check_in: Check-in date in YYYY-MM-DD format
            check_out: Check-out date in YYYY-MM-DD format
            adults: Number of adults
            rooms: Number of rooms
            currency: Currency code (USD, SAR, etc.)
            locale: Locale for results
            order_by: Sort order (popularity, price, distance, etc.)
            filter_by_star: List of star ratings to filter (e.g., [4, 5])
            max_results: Maximum number of results
        
        Returns:
            Dict with hotel results or error message
        """
        if not self.api_key:
            return {"error": "RapidAPI key not configured"}
        
        # First, get destination ID for the city
        dest_id = self._get_destination_id(city)
        if not dest_id:
            return {
                "error": "City not found",
                "message": f"Could not find destination ID for {city}"
            }
        
        # Search for hotels
        url = f"{self.base_url}/hotels/search"
        
        params = {
            "dest_id": dest_id,
            "dest_type": "city",
            "checkin_date": check_in,
            "checkout_date": check_out,
            "adults_number": adults,
            "room_number": rooms,
            "order_by": order_by,
            "filter_by_currency": currency,
            "locale": locale,
            "units": "metric",
            "page_number": 0
        }
        
        if filter_by_star:
            params["categories_filter_ids"] = ",".join([f"class::{star}" for star in filter_by_star])
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if "result" not in data or len(data["result"]) == 0:
                return {
                    "error": "No hotels found",
                    "message": f"No hotels available in {city} for the selected dates"
                }
            
            # Parse and format hotel results
            hotels = []
            for hotel in data["result"][:max_results]:
                hotel_info = self._parse_hotel_result(hotel, city)
                hotels.append(hotel_info)
            
            return {
                "success": True,
                "hotels": hotels,
                "count": len(hotels),
                "city": city
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "error": "API request failed",
                "message": str(e)
            }
        except Exception as e:
            return {
                "error": "Failed to parse hotel data",
                "message": str(e)
            }
    
    def _get_destination_id(self, city: str) -> Optional[str]:
        """Get Booking.com destination ID for a city"""
        # Known destination IDs for Umrah cities
        destinations = {
            "makkah": "-2092611",
            "mecca": "-2092611",
            "medina": "-2096394",
            "madinah": "-2096394",
            "jeddah": "-2094342",
            "riyadh": "-2092174"
        }
        
        city_lower = city.lower().strip()
        dest_id = destinations.get(city_lower)
        
        if dest_id:
            return dest_id
        
        # If not in our list, try to search for it
        try:
            url = f"{self.base_url}/hotels/locations"
            params = {
                "name": city,
                "locale": "en-us"
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                return str(data[0].get("dest_id"))
        except Exception as e:
            print(f"Error searching for destination: {e}")
        
        return None
    
    def _parse_hotel_result(self, hotel: Dict, city: str) -> Dict[str, Any]:
        """Parse hotel result into simplified format"""
        try:
            # Calculate distance to Haram (for Makkah/Medina)
            distance_to_haram = None
            if city.lower() in ["makkah", "mecca", "medina", "madinah"]:
                # Try to extract distance from hotel data
                distance = hotel.get("distance", "")
                if distance:
                    distance_to_haram = distance
            
            # Get price information
            price_breakdown = hotel.get("price_breakdown", {})
            composite_price = hotel.get("composite_price_breakdown", {})
            
            total_price = (
                price_breakdown.get("all_inclusive_price") or
                composite_price.get("all_inclusive_amount", {}).get("value") or
                hotel.get("min_total_price", 0)
            )
            
            currency = (
                price_breakdown.get("currency") or
                composite_price.get("all_inclusive_amount", {}).get("currency") or
                "USD"
            )
            
            return {
                "id": hotel.get("hotel_id"),
                "name": hotel.get("hotel_name", "Unknown Hotel"),
                "star_rating": hotel.get("class", 0),
                "address": hotel.get("address", ""),
                "city": hotel.get("city", city),
                "distance_to_center": hotel.get("distance", ""),
                "distance_to_haram": distance_to_haram,
                "price": {
                    "total": total_price,
                    "currency": currency,
                    "per_night": total_price / max(1, hotel.get("nights", 1)) if hotel.get("nights") else total_price
                },
                "rating": {
                    "score": hotel.get("review_score", 0),
                    "text": hotel.get("review_score_word", ""),
                    "count": hotel.get("review_nr", 0)
                },
                "amenities": hotel.get("hotel_facilities", "").split(", ") if hotel.get("hotel_facilities") else [],
                "room_type": hotel.get("unit_configuration_label", "Standard Room"),
                "photos": [
                    hotel.get("main_photo_url", "")
                ] if hotel.get("main_photo_url") else [],
                "url": hotel.get("url", ""),
                "is_free_cancellable": hotel.get("is_free_cancellable", 0) == 1,
                "latitude": hotel.get("latitude"),
                "longitude": hotel.get("longitude")
            }
        except Exception as e:
            print(f"Error parsing hotel result: {e}")
            return {
                "error": "Failed to parse hotel",
                "name": hotel.get("hotel_name", "Unknown"),
                "raw_data": hotel
            }
    
    def get_hotel_details(self, hotel_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific hotel"""
        url = f"{self.base_url}/hotels/data"
        
        params = {
            "hotel_id": hotel_id,
            "locale": "en-us"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "hotel": data
            }
        except Exception as e:
            return {
                "error": "Failed to get hotel details",
                "message": str(e)
            }


# Create singleton instance
_rapidapi_hotels = None

def get_rapidapi_hotels() -> RapidAPIHotels:
    """Get or create RapidAPI Hotels instance"""
    global _rapidapi_hotels
    if _rapidapi_hotels is None:
        _rapidapi_hotels = RapidAPIHotels()
    return _rapidapi_hotels
