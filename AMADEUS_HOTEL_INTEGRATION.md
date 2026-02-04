# Amadeus Hotel API Integration - Complete

## Summary
Successfully replaced the Booking.com API (via RapidAPI) with the Amadeus Hotel API for more reliable hotel search functionality.

## Why the Change?
The Booking.com API via RapidAPI had significant limitations:
- Only provided data for bookings within 3-6 months
- Frequent rate limiting issues
- Inconsistent availability data
- Required separate RapidAPI subscription

## Amadeus Hotel API Benefits
✅ **Same credentials as flight API** - No additional API keys needed
✅ **Better advance booking data** - More reliable for future dates
✅ **Comprehensive hotel information** - Detailed room descriptions, amenities, policies
✅ **Distance calculations** - Automatic distance from landmarks (Haram)
✅ **Real-time pricing** - Actual prices in multiple currencies
✅ **Professional API** - Industry-standard travel API used by major booking platforms

## Implementation

### New File Created
- `agents/hotel_agent/amadeus_hotel_tools.py` - Complete Amadeus Hotel API client

### Features Implemented

1. **Search Hotels by City**
   - Search by IATA city code (MEC for Makkah, MED for Medina)
   - Filter by star rating (4-5 stars)
   - Radius-based search

2. **Search Hotels Near Landmark**
   - Search within specific radius of Masjid al-Haram or Masjid an-Nabawi
   - Automatic distance calculation from landmark
   - Ideal for finding hotels with walking distance to Haram

3. **Get Hotel Offers with Pricing**
   - Real-time availability and pricing
   - Detailed room information
   - Cancellation policies
   - Tax breakdowns

### Landmark Coordinates
```python
LANDMARKS = {
    "masjid_al_haram": {
        "latitude": 21.4225,
        "longitude": 39.8262,
        "city": "Makkah"
    },
    "masjid_nabawi": {
        "latitude": 24.4672,
        "longitude": 39.6111,
        "city": "Medina"
    }
}
```

## Updated Hotel Agent

### New Tools
1. `search_hotels()` - Search with Amadeus API
   - Supports city-wide or landmark-based search
   - Filters by star rating
   - Returns real prices and availability

2. `get_city_code()` - Get IATA city codes
   - MEC for Makkah
   - MED for Medina

### Removed Tools
- `get_hotel_details()` - No longer needed (details included in search results)

## Test Results

### Test Query
```
Find hotels in Makkah near Haram for February 20-25, 2026 for 2 adults, prefer 4-5 star hotels
```

### Real Result from Amadeus API
```
HILTON SUITES MAKKAH ★★★★★

Location:
- 490 meters from Masjid al-Haram
- Prime location in Makkah

Room:
- King Guest Room with City View
- 28 square meters
- WiFi, HD TV, Coffee/tea facilities

Pricing:
- Base rate: 11,279.00 SAR
- Taxes: 2,340.39 SAR
- Total: 13,619.39 SAR (~$3,632 USD)
- Per night: ~$726 USD
- 5 nights stay
```

## API Endpoints Used

1. **OAuth Token**
   ```
   POST https://test.api.amadeus.com/v1/security/oauth2/token
   ```

2. **Hotel List by City**
   ```
   GET https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city
   ```

3. **Hotel List by Geocode**
   ```
   GET https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-geocode
   ```

4. **Hotel Offers**
   ```
   GET https://test.api.amadeus.com/v3/shopping/hotel-offers
   ```

## Deployment

### Environment Variables
```bash
AMADEUS_API_KEY=2GPz8TnKFAbvAzBzaDyPQmCZEb4WP3Gv
AMADEUS_API_SECRET=rdAvLZyigXGwxJnH
```

### Deploy Command
```bash
cd agents/hotel_agent
agentcore deploy --agent umrah_hotel_agent --auto-update-on-conflict \
  --env AMADEUS_API_KEY=2GPz8TnKFAbvAzBzaDyPQmCZEb4WP3Gv \
  --env AMADEUS_API_SECRET=rdAvLZyigXGwxJnH
```

## Known Limitations

1. **Advance Booking Window**
   - Hotels may not be available for dates too far in the future
   - Typically works best for dates within 12-18 months
   - This is a hotel industry limitation, not an API limitation

2. **Test API**
   - Currently using Amadeus Test API
   - For production, upgrade to Production API for:
     - More hotel inventory
     - Better availability data
     - Higher rate limits

3. **Search Radius**
   - Currently set to 2km from Haram
   - Can be adjusted based on user preferences

## Comparison: RapidAPI vs Amadeus

| Feature | RapidAPI (Booking.com) | Amadeus Hotel API |
|---------|------------------------|-------------------|
| **Advance Booking** | 3-6 months | 12-18 months |
| **API Credentials** | Separate RapidAPI key | Same as flights |
| **Rate Limits** | Restrictive (free tier) | More generous |
| **Data Quality** | Inconsistent | Professional |
| **Distance Calc** | Manual | Automatic |
| **Pricing** | Sometimes missing | Always included |
| **Room Details** | Limited | Comprehensive |
| **Status** | ⚠️ Deprecated | ✅ Active |

## Integration with Orchestrator

The orchestrator agent automatically calls the hotel agent, which now uses Amadeus:

```
User Request
    ↓
Orchestrator Agent
    ↓
Hotel Agent (Amadeus API)
    ↓
Real Hotel Data
    ↓
Comprehensive Trip Plan
```

## Next Steps

### For Production Use

1. **Upgrade to Production API**
   - Register for Amadeus Production API
   - Update credentials in .env
   - Change base URL from `test.api.amadeus.com` to `api.amadeus.com`

2. **Implement Caching**
   - Cache hotel search results for popular routes
   - Reduce API calls and costs
   - Improve response time

3. **Add More Features**
   - Hotel photos (available in Amadeus API)
   - Guest reviews and ratings
   - Amenity filtering (pool, spa, etc.)
   - Price comparison across dates

4. **Error Handling**
   - Retry logic for API failures
   - Fallback to general recommendations
   - Better user feedback for date limitations

## Status
✅ **COMPLETE AND WORKING**

The hotel agent now uses the Amadeus Hotel API and returns real hotel data with:
- Actual prices in SAR and USD
- Real hotel names and locations
- Accurate distances from Haram
- Detailed room information
- Availability for dates within booking window

🎉 **Both flight and hotel agents now use the same reliable Amadeus API!** 🎉
